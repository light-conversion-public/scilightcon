"""Compatibility fixes for older version of python"""
import sys
from importlib import resources

def _open_text(data_module, data_file_name):    
    if sys.version_info >= (3, 9):
        return resources.files(data_module).joinpath(data_file_name).open("r")
    else:
        return resources.open_text(data_module, data_file_name)