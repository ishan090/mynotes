from ciphercaesar import encrypt, decrypt
from os.path import exists
import os
import sys
import json

# args passed in cli prompt
files = sys.argv[1:]

# CWD - the place the program was run from
toread = os.getcwd()

# store the path of encrypted files as a variable and change cwd to it
home = os.path.expanduser('~')
tochange = home + "/bin/stuff/"
if not os.path.isdir(tochange):
    os.mkdir(tochange)
os.chdir(tochange)


def getInfo(what):
    while True:
        out = input(f"Enter {what}:\n-->").strip()
        if out != "":
            break
        else:
            print(f"{what} must have at least one character")
    return out

def initJson(name=None, pw=None, settings=None):
    if (name is None or pw is None) and settings is None:
        print("Setting up the User and Password")
        name = getInfo("Name")
        pw = getInfo("Password")
    if settings is None:
        settings = {
        "user": name,
        "pw": pw,
        "used_nums": [],
        "notebases": {}
            }
    # Serializing json
    json_object = json.dumps(settings, indent=4)

    # Writing to sample.json
    with open("settings.json", "w") as outfile:
        outfile.write(json_object)


def init():
    # load the settings
    try:
        settings = load_settings()
    except FileNotFoundError:
        initJson()
        settings = load_settings()
    # now make sure the files corresponding to the notebases are in proper order
    for i in settings["notebases"].keys():  # for each notebase
        if not exists(f"enc{i}.txt"):  # if the corresponding file is missing
            with open(f"enc{i}.txt", "w"):  # create it
                pass
    return settings


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
    with open(session["enc"], mode) as file:
        file.writelines(enc)


def add_arguments():
    if files:
        print("Attempting to add data from files...")
        password = input("Authentication required. Please enter your password:\n--> ")
        if password != envi["pw"]:
            print("Incorrect password. Action failed...")
            return
        for i in files:
            if exists(toread+"/"+i):
                print(f"Reading file {i}...", end='')
                d = readfile(i, toreadfrom=toread)
                print(f"Success!\nAdding data...")
                entry(d)
                print("Success!")
            else:
                entry(i)
        print()


### CLI FUNCTIONS
# Read func
def r(show_line_number=False):
    x = 1
    for i in readfile(session["enc"], decipher=True):
        if not show_line_number:
            print(i)
        else:
            print(x, i)
        x += 1

# Append/Overwrite func
def a():
    text = input("Enter file name (with extension) or text:\n-->")
    if exists(toread+"/"+text):
        text = readfile(text, toreadfrom=toread)
    else:
        text += "\n"
    entry(text)

# Show encrypted func
def s():
    for i in readfile(session["enc"]):
        print(i)

# Show help
def h():
    output = """
    MyNotes User Manual:

    r: show all the notes
    a: add something
    s: show the encrypted form
    h: show this msg
    p: change password
    d: delete some or all entries
    q: exit
    n: notebase settings - change or create notebases
    """
    print(output)

# Change Password
def p():
    print("Trying to change your password. Please comply with the following...")
    pw = getInfo("Password")
    new = getInfo("New Password")
    global envi
    envi["pw"] = new
    initJson(settings=envi)

# Delete entries
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
    data = readfile(session["enc"], decipher=True)
    data = data[:lines[0]-1] + data[lines[1]:]
    entry(data, mode="w")
    print(f"Success! Deleted lines {lines[0]} to {lines[1]}")

def get_new_key():
    x = 0
    while x != 100:
        if str(x) not in list(envi["notebases"].keys()):
            return str(x)
        x += 1
    raise ValueError("Maximum limit for notebases reached: 100")


def create_notebase():
    """
    A notebase is a key in the settings dict which maps numbers to a notebase's name.
    Thus, this function will first add a new key to that dict and create a file corresponding to the new key added.
    """
    print("Creating new NoteBase...")
    # Find a key that hasn't already been used.
    new = get_new_key()
    nb_name = getInfo("NoteBase Name")
    nb_pw = getInfo("NoteBase Password")

    # register the notebase
    envi["notebases"][new] = [nb_name, nb_pw]
    initJson(settings=envi)

    # create a file for the notebase
    with open(f"enc{new}.txt", "w") as f:
        pass

    print("New notebase created!")
    return True


def del_nb():
    print("Which NoteBase would you like to delete?")
    showNBs()
    to_del = input("Enter only the number --> ")
    try:
        global envi
        pw = input(f"Trying to delete notebase {envi['notebases'][to_del][0]}, enter notebase password:\n--> ")
        if pw != envi['notebases'][to_del][1]:
            print("Wrong password. Try again.")
            return
        del envi["notebases"][to_del]
        envi["used_nums"] = list(envi["notebases"].keys())
        os.remove(f"enc{to_del}.txt")
        initJson(settings=envi)
        if session["cwnb"] not in envi["notebases"].keys():
            print("You just deleted the notebase you were working on... so...")
            compul(changeNB, "You must select a notebase to continue as you deleted the one you were working on.")
        elif envi["notebases"]:
            pass
        else:
            print("Your only working notebase was deleted!")
            create_notebase()
            session["cwnb"] = envi["notebases"][0]
            session["enc"] = "enc0.txt"
        return True
    except KeyError:
        print("error: please enter the correst notebase number")
    except Exception as e:
        print(str(e))
        return False


def showNBs():
    print("NoteBases Present:")
    for i, j in envi["notebases"].items():
        print(i, j[0])



def changeNB():
    print("Which NoteBase would you like to operate in?")
    showNBs()
    changeto = input("Enter only the number --> ")
    # print(envi)
    try:
        pw = input(f"Trying to change to notebase {envi['notebases'][changeto][0]}, enter notebase password:\n--> ")
        if pw != envi['notebases'][changeto][1]:
            print("Wrong password. Try again.")
            return False
        envi["notebases"][changeto]
        session["cwnb"] = changeto
        session["enc"] = f"enc{changeto}.txt"
        print(f"Entered NoteBase {envi['notebases'][session['cwnb']][0]}")
        return True
    except:
        print("No such NoteBase exists!")
        return False



def n():
    """
    A notebase is the place where the user's notes are stored. Like data is stored in a database.
    This function will allow a user to change their current working notebase or even create another one.
    """
    # print("Welcome to NoteBase Settings, what would you like to do?")
    operations = """
    Available options

    show: Display NoteBases
    change: Change Current Working NoteBase
    create or mk: Create a New NoteBase
    del, delete, rm: Delete a NoteBase
    """
    # print(operations)
    # task = input(operations+"\nEnter Number (1-3):\n--> ")
    # if task == "q" or not task in ["1", "2", "3"]:
    #     return
    tasks = {"show": showNBs, "change": changeNB, "create": create_notebase, "delete": del_nb, "del": del_nb, "rm": del_nb, "mk": create_notebase, "h": lambda: print(operations)}
    # print(prompt[1])
    try:
        tasks[prompt[1]]()
    except KeyError:
        print(f"Invalid command {prompt}. Type n h or help for available actions")
    except IndexError:
        print("command lacks additional argument. Type n h or n help for more info")


def compul(A, msg):
    while True:
        result = A()
        if result:
            break
        else:
            print(msg)


# Main function - CLI Loop
def main():
    print("Hello and Welcome to this program made for making secure, quick and easy notes.")
    while True:
        pw = getInfo("Password")
        if pw != envi["pw"]:
            print("Wrong password. Try Again")
        else:
            break
    print()
    # If there are no notebases
    if not envi["notebases"].keys():
        print("You currently do not have any NoteBases to write in. Please create a NoteBase.")
        create_notebase()
        session["cwnb"] = envi["notebases"][0]
        session["enc"] = "enc0.txt"
    else:
        print("Please select a NoteBase to continue...")
        compul(changeNB, "You must select a NoteBase to continue. Try again.")
    print()
    # After making the user select a notebase, move on to the prompts.
    global prompt
    prompt = input(f"Enter Command: (Current NoteBase - {envi['notebases'][session['cwnb']][0]})\n--> ").strip().split()
    commandMap = {'r': r, 'a': a, 's': s, 'h': h, 'p': p, 'd': d, 'n': n, 'status': lambda: print(envi["notebases"], session)}
    while prompt != ['q']:
        try:
            commandMap[prompt[0]]()
            print()
        except KeyError:
            print("No such command... type h for the list of commands")
        except IndexError:  # If nothing is typed, continue
            pass
        prompt = input(f"Enter Command: (Current NoteBase - {envi['notebases'][session['cwnb']][0]})\n--> ").strip().split()

if __name__ == "__main__":
    envi = init()
    # session["cwnb"] maps to a string -> the numberical key used for the notebase in the dict envi["notebases"]
    session = {}
    add_arguments()
    main()






