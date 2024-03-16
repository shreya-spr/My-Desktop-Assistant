# Contains various system related functions
# For now: Calculator, notion, cmd

import os
import subprocess as sp

paths = {
    'notion': "C:\\Users\\Admin\\AppData\\Local\\Programs\\Notion\\Notion.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_notion():
    os.startfile(paths['notion'])

def open_cmd():
    os.system('start cmd')

def open_calculator():
    sp.Popen(paths['calculator'])

