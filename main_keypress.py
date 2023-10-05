import pyautogui
import keyboard
import time

def simulate_typing(text):
    # Loop over each line in the text
    for line in text.splitlines():
        # Loop over each character in the line
        for char in line:
            # Check if the character is a letter
            # if char.isalpha():
            #     # Simulate typing the character using keyboard
            #     keyboard.press_and_release(char)
            # else:
            #     # Simulate typing the character using pyautogui
            pyautogui.press(char)
            # Wait for a brief moment before pressing the next key
        # Simulate pressing the 'enter' key using keyboard
        keyboard.press_and_release('enter')
        keyboard.press_and_release('home')
        # keyboard.press_and_release('home')

# Get the file name from the user
filename = "text.txt"
# Print the countdown from 3 to 1
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

# Open the file and read its contents
with open(filename, 'r') as file:
    file_contents = file.read()

# Simulate typing out the file contents
simulate_typing(file_contents)