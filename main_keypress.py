import pyautogui
import keyboard
import time

def simulate_typing(text, delay=0.1):
    # Loop over each line in the text
    for line in text.splitlines():
        # Loop over each character in      d the line
        for char in line:
            # Simulate typing out the current character
            pyautogui.press(char)
            # Wait for a brief moment before pressing the next key
            # time.sleep(delay)
        # Simulate pressing the 'enter' key using keyboard
        keyboard.press_and_release('enter')

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