import subprocess

with open("modules.txt", "r") as file:
    modules = [line.strip() for line in file.readlines()]

for module in modules:
    print(f"Installing {module}...")
    subprocess.call(["pip3", "install", module])