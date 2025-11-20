import platform


def is_windows() -> bool:
    return platform.system().lower() == "windows"


def is_linux() -> bool:
    return platform.system().lower() == "linux"


def is_mac() -> bool:
    return platform.system().lower() == "darwin"
