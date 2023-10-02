**this program can copy your files from a virtual computer where you only see the screen and can interact with it to your computer (host)**



# Copy FROM virtual desktop:

### Windows virtual machine:

```
cd miniprog/  # cd to folder miniprog
python3 install_all_modules.py
```
### Linux virtual Machine:

```
sudo apt-get install libjpeg-dev -y
sudo apt install python3-pip
cd miniprog/  # cd to folder miniprog
python3 install_all_modules.py
```

after installation complete, insert files in folder "FilesToSend"
CTRL+C → CTRL+V

at local machine, run:
```commandline
python3 main_read.py
```
and now, point you mouse pointer to virtual Desktop window, it will hit button 'q' every time, when transmission of parts will be completed





