import os
import subprocess
import platform

def open_file_browser(path):
    # Ensure the path exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path {path} does not exist.")

    # Normalize the path
    path = os.path.normpath(path)

    # Determine the operating system
    system = platform.system().lower()

    if system == 'windows':
        # Windows
        os.startfile(path)
    elif system == 'darwin':
        # macOS
        subprocess.call(['open', path])
    elif system == 'linux':
        # Linux
        subprocess.call(['xdg-open', path])
    else:
        raise OSError(f"Unsupported operating system: {system}")