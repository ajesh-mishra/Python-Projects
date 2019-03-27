import os
import fnmatch
import sys
    
file_pattern = "*.py"

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
	
def check_variables(all_files):
    pass
    for file in all_files:
        if not file.startswith("variable"):
            with open(file) as f:
                data = f.read()
            
            data

        
	
all_files = get_all_files(get_directory())
print(all_files)

check_variables(all_files)







# Comments Section for future code developments
# for file in all_files:
#     with open(file) as f:  
#         data = f.read()
    
#     if data.startswith("ignore"):
#             all_files.remove(file)

# print(f'\n {all_files}')