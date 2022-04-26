import json
import os

def file_list(path):
    """
    In: path to a folder
    Out: list of elements in the folder
    """
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

def read_RNDWs_from_JSONs(path):
    """
    In: path to folder
    Out: List of Dictionairies from JSON-files in the folder
    """
    rndws = []
    for filename in file_list(path):
        with open(filename, 'r') as f:
            rndw = json.loads(f.read())
        rndws.append(rndw)
    return rndws
