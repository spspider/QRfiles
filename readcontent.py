import os
import pyperclip


def iterate_folders_and_print_content(target_folder):
    all_output = []  # List to store all output
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, target_folder)
            with open(file_path, 'r') as f:
                file_content = f.read()
            output = f"file: {relative_path}, content: \"\"\"{file_content}\"\"\""
            print(output)
            all_output.append(output)  # Append the output to the list

    # Combine all output into a single string and copy to clipboard
    combined_output = "\n".join(all_output)
    pyperclip.copy(combined_output)
    print("\nAll output has been copied to the clipboard.")


# Specify the folder to run the script in
target_folder = "recieved/project"

# Call the function
iterate_folders_and_print_content(target_folder)