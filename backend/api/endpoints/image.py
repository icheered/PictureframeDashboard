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
    dirs = None
    with open(filename, 'r') as reader:
        dirs = reader.read().splitlines()
    if dirs is None:
        return 404
    chosendir = random.choice(dirs)
    print(f"{chosendir}")
    ret = random.choice(os.listdir(chosendir))
    while not os.path.isfile(f"{chosendir}/{ret}"):
        ret = random.choice(os.listdir(chosendir))
    print(f"{chosendir}/{ret}")
    return FileResponse(f"{chosendir}/{ret}")

filename = "image_dirlist.txt"

@router.get("/dirs")
def get_directories():
    ret = None
    with open(filename, 'r') as reader:
        ret = reader.read().splitlines()
    if ret is not None:
        return ret
    else:
        return 0

@router.patch("/dirs")
def update_directories():
    dirlist = get_paths(directory)
    with open(filename, 'w') as writer:
        writer.write("\n".join(dirlist))

