import os

def iterate_folders_and_print_content(target_folder):
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, target_folder)
            with open(file_path, 'r') as f:
                file_content = f.read()
            print(f"file: {relative_path}, content: \"\"\"{file_content}\"\"\"")

# Specify the folder to run the script in
target_folder = "recieved/mlr_serhiipaukovmicro"

# Call the function
iterate_folders_and_print_content(target_folder)
