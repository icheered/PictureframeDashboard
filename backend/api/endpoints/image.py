import os
import random

from fastapi import APIRouter, status
from fastapi.responses import FileResponse

router = APIRouter()

directory = '/home/tjbakker/STACK_TEST/Photography_Videography/Photography'

def get_paths(path: str):
    retlist = []
    for item in os.listdir(path):
        if os.path.isdir(f"{path}/{item}"):
            if item == "Edited" or item == "Editted":
                retlist.append(f"{path}/{item}")
            else:
                retlist.extend(get_paths(f"{path}/{item}"))
    return retlist

@router.get("/")
def get_image():
    files = None
    with open(os.environ.get('filelist_name'), 'r') as reader:
        files = reader.read().splitlines()
    
    blacklist = None
    with open(os.environ.get('blacklist_name'), 'r') as reader:
        blacklist = reader.read().splitlines()
    
    choice = random.choice(files)
    while choice in blacklist:
        print("Picture was on blacklist")
        choice = random.choice(files)

    return FileResponse(choice)

filename = "image_dirlist.txt"

@router.get("/files")
def get_files():
    ret = None
    with open(os.environ.get('filelist_name'), 'r') as reader:
        ret = reader.read().splitlines()
    if ret is not None:
        return ret
    else:
        return 0

@router.get("/blacklist")
def get_blacklist_files():
    ret = None
    with open(os.environ.get('blacklist_name'), 'r') as reader:
        ret = reader.read().splitlines()
    if ret is not None:
        return ret
    else:
        return 0


@router.patch("/files")
def update_files():
    base_dir = os.environ.get('base_dir')
    dirlist = get_paths(base_dir)
    filelist = []
    for d in dirlist:
        for f in os.listdir(d):
            if f.endswith(('.jpg', '.jpeg')):
                filelist.append(os.path.join(d, f))
    
    with open(os.environ.get('filelist_name'), 'w') as writer:
        writer.write("\n".join(filelist))
    
    return f"Photos detected: {len(filelist)}"

