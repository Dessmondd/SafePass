import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, Toplevel, Listbox, Scrollbar, Button, MULTIPLE, END
import secrets
import string
import pyperclip
import os
import random
import tkinter.filedialog

wordlist = [
    "apple", "banana", "cherry", "date", "elder", "fig",
    "grape", "honey", "kiwi", "lemon", "mango", "nectar",
    "orange", "pear", "quince", "raspberry", "strawberry", "tangerine",
    "watermelon", "blackberry", "blueberry", "cranberry", "grapefruit",
    "kiwifruit", "pomegranate", "pineapple", "apricot", "blackcurrant",
    "chocolate", "cinnamon", "vanilla", "ginger", "butterscotch",
    "caramel", "marshmallow", "stracciatella", "peach", "plum", "lime",
    "peppermint", "spearmint", "mango", "coconut", "passionfruit",
    "blueberry", "vanilla", "hazelnut", "almond", "caramel",
    "strawberry", "chocolate", "lemon", "cinnamon", "raspberry",
    # ... add more words to the list
]

def generate_passphrase(num_words,add_numbers, min_digits=None, max_digits=None, add_special_chars=True, capitalize_percentage=60, include_spaces=True):
    words = []

    for _ in range(num_words):
        selected_word = secrets.choice(wordlist)
        words.append(selected_word.capitalize())

    if add_numbers or (min_digits or max_digits):
        if not min_digits:
            min_digits = secrets.randbelow(3) + 1
        if not max_digits:
            max_digits = secrets.randbelow(4) +  1 

        num_digits = secrets.randbelow(max_digits - min_digits + 1) + min_digits
        for _ in range(num_digits):
            words.insert(secrets.randbelow(len(words) + 1), secrets.choice(string.digits))

    if add_special_chars:
        words.insert(secrets.randbelow(len(words) + 1), secrets.choice(string.punctuation))

    secrets.SystemRandom().shuffle(words)
    
    for _ in range(round(len(words) * (capitalize_percentage / 100))):
        random_word = secrets.randbelow(len(words))
        words[random_word] = words[random_word].capitalize()
    if include_spaces:
        passphrase = ' '.join(words)  
    else:
        passphrase = ''.join(words) 

    return passphrase

def toggle_spaces():
    include_spaces.set(not include_spaces.get())

def load_custom_wordlist():
    file_path = tkinter.filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                words = file.read().splitlines()
                wordlist.clear()
                wordlist.extend(words)
                messagebox.showinfo("Custom Wordlist", "Custom wordlist loaded successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the custom wordlist:\n{e}")


def generate_button_clicked():
    try:
        num_words = int(num_words_entry.get())
        add_numbers = numbers_var.get()
        add_special_chars = special_chars_var.get()

        passphrase = generate_passphrase(num_words, add_numbers, add_special_chars,capitalize_percentage=100, include_spaces=True)

        sentence = "Your new password is: " + passphrase
        passphrase_label.config(text=sentence)
        copy_button.config(state=tk.NORMAL)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")

def copy_to_clipboard():
    passphrase = passphrase_label.cget("text").replace("Your new password is: ", "")
    pyperclip.copy(passphrase)





app = tk.Tk()
app.title("Memorable Password Generator")

num_words_label = tk.Label(app, text="Enter the number of words in the passphrase:")
num_words_label.pack()

num_words_entry = tk.Entry(app)
num_words_entry.pack()

numbers_var = tk.BooleanVar()
numbers_check = tk.Checkbutton(app, text="Include a number", variable=numbers_var)
numbers_check.pack()

special_chars_var = tk.BooleanVar()
special_chars_check = tk.Checkbutton(app, text="Include a special character", variable=special_chars_var)
special_chars_check.pack()

passphrase_label = tk.Label(app, text="", wraplength=300)
passphrase_label.pack()

copy_button = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard, state=tk.DISABLED)
copy_button.pack()
load_custom_wordlists = tk.Button(app, text="Load Custom Wordlist", command=load_custom_wordlist)
load_custom_wordlists.pack()

include_spaces = tk.BooleanVar(value=True)  # Include spaces by default

spaces_check = tk.Checkbutton(app, text="Include Spaces", command=include_spaces)
spaces_check.pack()
generate_button = tk.Button(app, text="Generate Memorable Passphrase", command=generate_button_clicked)
generate_button.pack()


app.mainloop()
