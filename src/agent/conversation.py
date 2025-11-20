from __future__ import annotations

import json
from typing import List

from openai import OpenAI

from ..config import Config
from ..utils.logging_utils import setup_logging
from .prompts import SYSTEM_PROMPT
from .tool_schemas import tool_schemas
from .tools_registry import FIX_TOOL_NAMES, get_tools_registry


class ConversationRunner:
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logging()
        self.tools_registry = get_tools_registry(config)
        self.client = OpenAI(api_key=config.openai_api_key)

    def _call_model(self, history: List[dict]):
        return self.client.chat.completions.create(
            model=self.config.model_name, messages=history, tools=tool_schemas
        )

    def _append_tool_message(self, history: List[dict], tool_name: str, tool_result):
        history.append(
            {
                "role": "tool",
                "name": tool_name,
                "content": json.dumps(tool_result.__dict__),
            }
        )

    def _handle_tool_call(self, message, history: List[dict]):
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments or "{}")
            tool = self.tools_registry.get(tool_name)
            if not tool:
                self.logger.warning("Unknown tool requested: %s", tool_name)
                continue

            if tool_name in FIX_TOOL_NAMES:
                print("Assistant proposes a fix:")
                print(f"- Tool: {tool_name}")
                print(f"- Parameters: {tool_args}")
                confirmation = input("Run this action? (yes/no): ").strip().lower()
                if confirmation not in {"yes", "y"}:
                    self._append_tool_message(
                        history,
                        tool_name,
                        type("Decline", (), {"__dict__": {"success": False, "data": {}, "error": "User declined"}})(),
                    )
                    continue

            self.logger.info("Running tool %s with args %s", tool_name, tool_args)
            result = tool.run(**tool_args)
            self._append_tool_message(history, tool_name, result)

    def run_conversation(self):
        if not self.config.openai_api_key:
            print("OPENAI_API_KEY is not set. Please configure it in your environment or .env file.")
            return

        print("ai-system-diagnoser (experimental)")
        print(f"Mode: {'Allow fixes' if self.config.allow_fixes else 'Diagnostic only'}")
        print("Type 'exit' or 'quit' to end the session.\n")

        history: List[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

        while True:
            user_input = input("You: ")
            if user_input.strip().lower() in {"exit", "quit"}:
                break

            history.append({"role": "user", "content": user_input})
            response = self._call_model(history)
            message = response.choices[0].message

            if message.tool_calls:
                assistant_msg = {
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [tc.model_dump() for tc in message.tool_calls],
                }
                history.append(assistant_msg)
                self._handle_tool_call(message, history)
                # Call the model again with tool outputs
                response = self._call_model(history)
                message = response.choices[0].message

            history.append({"role": "assistant", "content": message.content or ""})
            print(f"Assistant: {message.content}\n")
