import nuke
from .._internal import *
import os

def check_dir(path):
    """
    Check if a given path exists.
    
    Args:
    path (str or nuke.Node): A file path as a string or a Nuke node with a 'file' knob.
    
    Returns:
    str or None: The directory path if it exists, None otherwise.
    """
    if isinstance(path, nuke.Node):
        if 'file' not in path.knobs():
            print("Node does not have a 'file' knob")
            return None
        path_str = path['file'].getValue()
    elif isinstance(path, str):
        path_str = path
    else:
        print(f"Unsupported type: {type(path)}. Expected str or nuke.Node")
        return None
    
    dir_path = os.path.dirname(path_str)
    
    if os.path.exists(dir_path):
        return dir_path
    else:
        print(f"Path does not exist: {dir_path}")
        return None
    
