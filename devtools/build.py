
# Only working on Windows and Linux

import platform
import os
import shutil
import time

def parent_dir(dir):
    dir = dir.replace('\\', '/').split('/')
    out_dir = str()
    for i in range(len(dir) - 1): out_dir += f"{dir[i]}/"
    return out_dir[0: len(out_dir) - 1]

def cut_file(file, to = 1):
    file = file.replace('\\', '/').split('/')
    out_file = str()
    for i in range(len(file)):
        if len(file) - to <= i:
            out_file += f"{file[i]}/"
    return out_file[0: len(out_file) - 1]

DIR = parent_dir(os.getcwd())
SYSTEM = platform.system()
COMPILER = "javac"
JAVA_VERSION = 8

def set_title(val):
    if SYSTEM == "Windows":
        os.system(f"title {val}")

def pause(msg):
    if SYSTEM == "Windows":
        print(msg)
        os.system("pause > NUL")
    else:
        os.system(f"read -n1 -r -p \"{msg}\" key")

# Recursive function to find all files and folders of a directory
def find_files(dir, n = 0, log = True):
    directories = []
    files = []
    if log and n <= 0: print(f"-START- Filecrawling -START-")
    for file in os.listdir(dir):
        file = f"{dir}/{file}"
        if log: print(f"Crawling: {file}")
        if os.path.isdir(file): directories.append(file)
        else: files.append(file)
    for dir in directories:
        sub_files = find_files(dir, n + 1, log)
        for file in sub_files: files.append(file)
    if log and n <= 0: print(f"-FINISH- Filecrawling -FINISH-")
    return files

# Compiles all the Javacode-Files
def compile_files(files):
    print(f"-START- Compiler -START-")
    for file in files:
        if file.endswith(".java"):
            print(f"Valid Java-File: {file}")
            os.system(f"{COMPILER} -source {JAVA_VERSION} -target {JAVA_VERSION} {file}")
            time.sleep(3)
    print(f"-FINISH- Compiler -FINISH-")

# Transpheres all files into the Result-Folder
def transpher_files(files):
    print(f"-START- Transpher -START-")
    out_dir = f"{DIR}/production"
    src_parts = len(f"{DIR}/source".split('/'))
    for file in files:
        out_file = cut_file(file, len(file.split('/')) - src_parts)
        out_path = f"{out_dir}/{out_file}"
        out_type = None
        if file.endswith(".class"): out_type = "Bytecode"
        else: out_type = "Asset"
        if not (file.endswith(".java") or file.endswith("manifest")):
            print(f"Moving {out_type}: {out_file}")
            laydown_path(out_path)
            if out_type == "Bytecode": os.rename(file, out_path)
            else: shutil.copy(file, out_path)
    print(f"-FINISH- Transpher -FINISH-")

# Creates a Folder-Path, if it's not already existing
def laydown_path(file):
    file = parent_dir(file)
    if not os.path.isdir(file): os.makedirs(file)

# Cleares the Production-Directory
def clear_cache():
    print(f"-START- Clearing -START-")
    cache = find_files(f"{DIR}/production", log = False)
    for file in cache:
        print(f"Clearing: {file}")
        os.remove(file)
    if len(cache) <= 0: print("Nothing to clear.")
    print(f"-FINISH- Clearing -FINISH-")

# Packs all data into the JAR-File
def pack_data():
    print(f"-START- Packing -START-")
    cache = find_files(f"{DIR}/production", log = False)
    os.system(f"jar cmvf \"{DIR}/source/manifest\" \"{DIR}/EnhancedDesktop.jar\" -C \"{DIR}/production\" .")
    print(f"-FINISH- Packing -FINISH-")

def main():
    print("Initializing Compiler...")
    set_title("ESRC-Compiler Build-Host")
    print(f"Current System: {SYSTEM}")
    print(f"Current Directory: {DIR}")
    clear_cache()
    files = find_files(f"{DIR}/source")
    compile_files(files)
    transpher_files(files)
    pack_data()
    pause("Press enter to finish.")

if __name__ == "__main__": main()
