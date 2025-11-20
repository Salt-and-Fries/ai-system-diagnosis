tool_schemas = [
    {
        "type": "function",
        "function": {
            "name": "get_system_overview",
            "description": "Get summary of OS, CPU, RAM, GPU, and disk usage.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_process_snapshot",
            "description": "List top processes by resource usage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Max number of processes to return.",
                        "default": 20,
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_disk_health",
            "description": "Check SMART/health status for disks.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_system_errors",
            "description": "Fetch recent error-level events from system logs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of events to return",
                        "default": 50,
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_network_diagnostics",
            "description": "Run ping and DNS checks against a target.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target host or IP to test",
                        "default": "8.8.8.8",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_temperature_readings",
            "description": "Read temperature sensors if available.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "restart_service",
            "description": "Restart a Windows service by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service to restart",
                    }
                },
                "required": ["service_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_system_file_check",
            "description": "Run Windows System File Checker (sfc /scannow).",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "disable_startup_item",
            "description": "Disable a startup item by name or identifier.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Display name of the startup entry to disable",
                    }
                },
                "required": ["name"],
            },
        },
    },
]
