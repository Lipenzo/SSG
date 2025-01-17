from os.path import exists, join, isfile
from os import listdir, mkdir, remove
from shutil import copy, rmtree

def main():
    # need to clear public directory and then copy everything from static to public
    destination = "public"
    if not exists(destination):
        mkdir(destination)
    else:
        if isfile(destination):
            remove(destination)
        else:
            rmtree(destination)
        mkdir(destination)
    path = "static"
    recursive_copy(destination, path)
    
def recursive_copy(destination, current_folder):
    files = listdir(current_folder)
    for file in files:
        path = join(current_folder, file)
        if isfile(path):
            copy(path, destination)
            print(f"file copied: {join(current_folder, file)}  ->  {join(destination, file)}")
        else:
            new_destination = join(destination, file)
            new_path = join(current_folder, file)
            mkdir(new_destination)
            print(f"directory made: {new_destination}")
            recursive_copy(new_destination, new_path)

main()