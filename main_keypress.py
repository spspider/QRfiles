import pyautogui
import keyboard
import time
import re
import chardet
def simulate_typing(text):
    # Loop over each line in the text
    for line in text.splitlines():
        # Loop over each character in the line
        for char in line:
            # Check if the character is a lowercase letter
            if re.match(r"[a-z0-9 ]", char):
                # Simulate typing the character using keyboard
                keyboard.press_and_release(char)

            else:
                # Simulate typing the character using pyautogui
                pyautogui.press(char)
                print(char, end='')
            # Wait for a brief moment before pressing the next key
        # Simulate pressing the 'enter' key using keyboard
        keyboard.press('enter')
        # keyboard.press('home')
        # keyboard.press_and_release('home')

# Get the file name from the user
filename = "text.txt"
# Print the countdown from 3 to 1
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

# Open the file and read its contents
# Detect the file encoding
# with open(filename, 'rb') as file:
#     result = chardet.detect(file.read())

# Open the file and read its contents with the detected encoding
with open(filename, 'r', encoding='utf-8') as file:
    file_contents = file.read()

# Simulate typing out the file contents
simulate_typing(file_contents)