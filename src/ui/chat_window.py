from __future__ import annotations

import re
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from tkhtmlview import HTMLLabel

from ..agent.conversation import ConversationRunner
from ..utils.logging_utils import setup_logging


class ChatWindow:
    """Tkinter-based chat UI with a split view for text and HTML visuals."""

    def __init__(self, runner: ConversationRunner):
        self.runner = runner
        self.logger = setup_logging()
        self.root = tk.Tk()
        self.root.title("AI System Diagnoser")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)
        self.busy = False
        self.runner.confirm_callback = self._confirm_fix

        self._build_layout()

    def _build_layout(self):
        paned = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        chat_frame = ttk.Frame(paned, padding=10)
        visuals_frame = ttk.Frame(paned, padding=10)
        paned.add(chat_frame, weight=3)
        paned.add(visuals_frame, weight=2)

        chat_label = ttk.Label(chat_frame, text="Conversation")
        chat_label.pack(anchor="w")
        self.chat_text = tk.Text(
            chat_frame,
            wrap="word",
            state="disabled",
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
        )
        chat_scroll = ttk.Scrollbar(chat_frame, command=self.chat_text.yview)
        self.chat_text.configure(yscrollcommand=chat_scroll.set)
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        visuals_label = ttk.Label(visuals_frame, text="Visuals")
        visuals_label.pack(anchor="w")
        self.html_label = HTMLLabel(
            visuals_frame,
            html="<i>Visual responses will appear here when requested.</i>",
            background="white",
        )
        self.html_label.pack(fill=tk.BOTH, expand=True, padx=(0, 5))

        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill=tk.X)
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.input_entry.bind("<Return>", self._on_send)

        self.send_button = ttk.Button(input_frame, text="Send", command=self._on_send)
        self.send_button.pack(side=tk.RIGHT)

        self.status_label = ttk.Label(self.root, text="Ready")
        self.status_label.pack(anchor="w", padx=10, pady=(0, 6))

        self.input_entry.focus_set()

    def _append_chat(self, speaker: str, content: str):
        self.chat_text.configure(state="normal")
        self.chat_text.insert(tk.END, f"{speaker}: {content}\n\n")
        self.chat_text.configure(state="disabled")
        self.chat_text.see(tk.END)

    def _set_busy(self, busy: bool):
        self.busy = busy
        state = "disabled" if busy else "normal"
        self.input_entry.configure(state=state)
        self.send_button.configure(state=state)
        self.status_label.configure(text="Assistant is thinking..." if busy else "Ready")

    def _on_send(self, event=None):
        if self.busy:
            return "break"
        user_input = self.input_var.get().strip()
        if not user_input:
            return "break"

        self.input_var.set("")
        self._append_chat("You", user_input)
        self._set_busy(True)

        threading.Thread(target=self._process_user_input, args=(user_input,), daemon=True).start()
        return "break"

    def _process_user_input(self, user_input: str):
        try:
            response = self.runner.process_turn(user_input)
        except Exception as exc:  # pragma: no cover - UI surface
            self.logger.exception("Error processing conversation turn")
            response = f"An error occurred: {exc}"
            html_content = None
        else:
            html_content = self._extract_html(response)

        self.root.after(0, lambda: self._render_response(response, html_content))

    def _render_response(self, response: str, html_content: str | None):
        text_only = self._strip_html_from_message(response, html_content)
        self._append_chat("Assistant", text_only)

        if html_content:
            self.html_label.set_html(html_content)
        else:
            self.html_label.set_html("<i>No visual requested for this response.</i>")

        self._set_busy(False)

    def _confirm_fix(self, tool_name: str, tool_args: dict) -> bool:
        summary = f"Run tool '{tool_name}' with arguments:\n{tool_args}\n\nProceed?"
        return messagebox.askyesno("Confirm fix", summary)

    def _extract_html(self, message: str) -> str | None:
        code_block = re.search(r"```html\s*(.*?)```", message, re.DOTALL | re.IGNORECASE)
        if code_block:
            return code_block.group(1).strip()
        if "<html" in message.lower():
            return message
        return None

    def _strip_html_from_message(self, message: str, html_content: str | None) -> str:
        if not html_content:
            return message
        if "```html" in message:
            return re.sub(r"```html\s*.*?```", "", message, flags=re.DOTALL).strip()
        return message.replace(html_content, "").strip()

    def run(self):
        self.root.mainloop()
