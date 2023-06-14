from ciphercaesar import encrypt, decrypt
from os.path import exists
import os
import sys
import json

files = sys.argv[1:]


toread = os.getcwd()

home = os.path.expanduser('~')
tochange = home + "/bin/stuff/"
if not os.path.isdir(tochange):
    os.mkdir(tochange)
os.chdir(tochange)


def getInfo(what):
    while True:
        out = input(f"Enter Your {what}:\n-->").strip()
        if out != "":
            break
        else:
            print(f"Your {what} must have at least one character")
    return out

def initJson(name=None, pw=None, settings=None):
    if (name is None or pw is None) and settings is None:
        print("Setting up the User and Password")
        name = getInfo("Name")
        pw = getInfo("Password")
    if settings is None:
        settings = {
        "user": name,
        "pw": pw
            }
    # Serializing json
    json_object = json.dumps(settings, indent=4)

    # Writing to sample.json
    with open("settings.json", "w") as outfile:
        outfile.write(json_object)


def init():
    if not exists("enc.txt"):
        with open("enc.txt", "w"):
            pass
    if not exists("settings.json"):
        initJson()


def load_settings():
    with open("settings.json", "r") as file:
        settings = json.load(file)
    return settings


def readfile(file, decipher=False, toreadfrom=tochange):
    filepath = toreadfrom+"/"+file
    with open(filepath, 'r') as f:
        data = f.readlines()
    if decipher:
        data = decrypt(data, 5, multi=True)
    return data

def entry(text, file=None, mode="a"):
    data = text
    if file is not None:
        data = readfile(file)
    enc = encrypt(data, 5, multi=True)
    with open("enc.txt", mode) as file:
        file.writelines(enc)

# Functions for each command in the cli
def r(show_line_number=False):
    x = 1
    for i in readfile("enc.txt", decipher=True):
        if not show_line_number:
            print(i)
        else:
            print(x, i)
        x += 1


def a():
    text = input("Enter file name (with extension) or text:\n-->")
    if exists(toread+"/"+text):
        text = readfile(text, toreadfrom=toread)
    entry(text)

def s():
    for i in readfile("enc.txt"):
        print(i)

def h():
    output = """
    MyNotes User Manual:

    r: show all the notes
    a: add something
    s: show the encrypted form
    h: show this msg
    p: change password
    d: delete some or all entries
    """
    print(output)


def p():
    print("Trying to change your password. Please comply with the following...")
    pw = getInfo("Password")
    new = getInfo("New Password")
    global envi
    envi["pw"] = new
    initJson(settings=envi)

def d():
    print("Which of the following lines would you like to delete...")
    r(True)
    lines = input("Enter Line Numbers: format --> <n1>-<n2> (includes <n2>)\n-->").split("-")
    if lines[0] == "q":
        return
    if len(lines) == 1:
        lines += lines
    lines = [int(i) for i in lines]
    if not lines[0] <= lines[1]:
        print("ERROR: FIRST ARGUMENT MUST BE LESS THAN THE SECOND!")
        return
    data = readfile("enc.txt", decipher=True)
    data = data[:lines[0]-1] + data[lines[1]:]
    entry(data, mode="w")
    print(f"Success! Deleted lines {lines[0]} to {lines[1]}")



def main():
    print("Hello and Welcome to this m-names store made for bookmarking ms")
    while True:
        pw = getInfo("Password")
        if pw != envi["pw"]:
            print("Wrong password. Try Again")
        else:
            break
    print()
    x = input("Enter Command:\n--> ").strip()
    commandMap = {'r': r, 'a': a, 's': s, 'h': h, 'p': p, 'd': d}
    while x != 'q':
        try:
            commandMap[x]()
        except KeyError:
            print("No such command... type h for the list of commands")
        x = input("Enter Command:\n--> ")


def add_arguments():
    if files:
        print("Adding data from files...")
        for i in files:
            if exists(toread+"/"+i):
                print(f"Reading file {i}...", end='')
                d = readfile(i, toreadfrom=toread)
                print(f"Success!\nAdding data...", end='')
                entry(d)
                print("Success!")
            else:
                entry(i)


if __name__ == "__main__":
    init()
    envi = load_settings()
    add_arguments()
    main()






