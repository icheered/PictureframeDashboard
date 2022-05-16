import os
import random

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from tinydb import Query, TinyDB

db = TinyDB("db.json")

router = APIRouter()

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
    files = db.search(Query().files.exists())
    if not len(files):
        raise HTTPException(status_code=404, detail="No files found")
    else:
        files = files[0]['files']

    blacklist = db.search(Query().blacklist.exists())
    blacklist = blacklist if not len(blacklist) else blacklist[0]['blacklist']

    recent = db.search(Query().recent.exists())
    recent = recent if not len(recent) else recent[0]['recent']
    
    while len(recent) > int(os.environ.get('repeat_limit')):
        recent.pop(0)
    
    available = set(files) - set(blacklist) - set(recent)
    if len(available) == 0:
        raise HTTPException(status_code=400, detail="All available files are on the recent list or on blacklist. Try reducing the repeat_limit value.")

    choice = random.choice(list(available))
    recent.append(choice)
    db.upsert({'recent': recent}, Query().recent.exists())
    return FileResponse(choice)

@router.get("/single")
def get_single_image(filename: str):
    files = db.search(Query().files.exists())
    if not len(files):
        raise HTTPException(status_code=404, detail="No files found")
    else:
        files = files[0]['files']

    if filename in files:
        return FileResponse(filename)
    else:
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")
    

@router.get("/files")
def get_files():
    files = db.search(Query().files.exists())
    return files if not len(files) else files[0]['files']

@router.patch("/files")
def update_files():
    base_dir = os.environ.get('base_dir')
    dirlist = get_paths(base_dir)
    filelist = []
    for d in dirlist:
        for f in os.listdir(d):
            if f.endswith(('.jpg', '.jpeg')):
                filelist.append(os.path.join(d, f))

    db.upsert({'files': filelist}, Query().files.exists())
    
    return f"Photos detected: {len(filelist)}"

@router.get("/blacklist")
def get_blacklist():
    blacklist = db.search(Query().blacklist.exists())
    return blacklist if not len(blacklist) else blacklist[0]['blacklist']

@router.post("/blacklist")
def add_blacklist(filename: str):
    blacklist = db.search(Query().blacklist.exists())
    blacklist = blacklist if not len(blacklist) else blacklist[0]['blacklist']
    if filename not in blacklist:
        blacklist.append(filename)
    db.upsert({'blacklist': blacklist}, Query().blacklist.exists())

    return f"Adding file to blacklist: {filename}"

@router.delete("/blacklist")
def remove_blacklist(filename: str):
    blacklist = db.search(Query().blacklist.exists())
    blacklist = blacklist if not len(blacklist) else blacklist[0]['blacklist']
    if filename in blacklist:
        blacklist.remove(filename)
    db.upsert({'blacklist': blacklist}, Query().blacklist.exists())
    
    return f"Removing file from blacklist: {filename}"



@router.get("/recent")
def get_recent():
    recent = db.search(Query().recent.exists())
    return recent if not len(recent) else recent[0]['recent']
