import os

testdir = '/home/tjbakker/Documents/dev/vscode/webdev/pictureframe_dashboard/testfiles'

def get_paths(path: str):
    retlist = []
    for item in os.listdir(path):
        if os.path.isdir(f"{path}/{item}"):
            if item == "Edited":
                retlist.append(f"{path}/{item}")
            else:
                retlist.extend(get_paths(f"{path}/{item}"))
    return retlist

r = get_paths(testdir)
for i in r:
    print(i)