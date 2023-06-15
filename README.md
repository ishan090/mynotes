# A Project That Keeps Your Personal Notes

Sometimes you might have felt the need to write something that you would like no one else to read. A diary, for instance. Or just some simple notes.<br>
This program helps with just that.
And by its data encryption (using caesar cipher for now, for testing purposes,) you can rest assured knowing what you write is in safe hands or in this case, files.<br><br/>


## Running the program

After downloading/pulling the files, simply go the terminal or command prompt and type `python app.py` (do make sure you are in the same directory as the file).
That's it! The program will run you through what's required and make you set up a password which you will be required to enter every time you try to access your notes.
Then what's next is simpy for you to write away! Use the `a` command for this.<br><br/>


## Commands

Here's a list of all the commands, as given by the h command:
```
r: show all the notes
a: add something
s: show the encrypted form
h: show this msg
p: change password
d: delete some or all entries
q: exit
```
The function of each command is given alongside. <br><br/>

## Other functionalities

Now, you can also pass in files as command prompt arguments,
e.g., `python app.py blah.txt`.
This will read the file and after authenticating the action, directly add its content without first entering the main interphase.
Multiple arguments can be passed this way and they need not only be text files.

