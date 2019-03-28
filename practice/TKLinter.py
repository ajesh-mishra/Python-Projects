import os
import fnmatch
import sys
    
file_pattern = "*.py"
key_word = "print"

def get_directory():
    try:
        directory = sys.argv[1]
    except IndexError:
        directory = "."
        print("No directory was given, working with PWD")

    return directory

def get_all_files(directory = "."):
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, file_pattern):
                full_file_name = os.path.abspath(os.path.join(root, file))
                all_files.append(full_file_name)
                # print(full_file_name)

    return all_files

def find_all(data, key_word):
    pointer = 0
    while True:
        pointer = data.find(key_word, pointer)
        if pointer == -1: return
        yield pointer
        pointer += len(key_word)

def validate_all_files(all_files):
	for file in all_files:
		with open(file, 'r', encoding='utf-8') as f:
			data = f.read()
		
		position = list(find_all(data, key_word))
		if position:
			print(f'"{key_word}" found in {file} at {len(position)} place[s]: {position}')
		else:
			print(f'"{key_word}" not found in {file}')
		
all_files = get_all_files(get_directory())
validate_all_files(all_files)
