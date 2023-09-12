import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, Toplevel, Listbox, Scrollbar, Button, MULTIPLE, END
import secrets
import string
import pyperclip
import os
import random
import tkinter.filedialog
from modules.password_strength_tester import test_password
from tkinter import ttk
from ttkthemes import ThemedStyle


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
]

def generate_passphrase(num_words, add_numbers, add_special_chars, min_digits=None, max_digits=None, capitalize_percentage=60, include_spaces=True):
    words = []

    for _ in range(num_words):
        selected_word = secrets.choice(wordlist)
        words.append(selected_word.capitalize())

    if add_numbers:
        if not min_digits:
            min_digits = secrets.randbelow(3) + 1
        if not max_digits:
            max_digits = secrets.randbelow(4) + 1

    num_digits = secrets.randbelow(max(1, max_digits - min_digits + 1)) + min_digits
    for _ in range(num_digits):
        # Ensure that the upper bound for insertion is positive
        insert_pos = secrets.randbelow(max(1, len(words) + 1))
        words.insert(insert_pos, secrets.choice(string.digits))


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
    generate_button_clicked()

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
        num_words_str = num_words_entry.get()
        num_words = int(num_words_str)


        if num_words <= 0:
            raise ValueError("Number of words must be a positive integer")

        add_numbers = numbers_var.get()
        add_special_chars = special_chars_var.get()
        include_spaces_value = include_spaces.get()

        passphrase = generate_passphrase(num_words, add_numbers, add_special_chars, capitalize_percentage=100, include_spaces=include_spaces_value)

        sentence = "Your new password is: " + passphrase
        passphrase_label.config(text=sentence)
        copy_button.config(state=tk.NORMAL)

        strength_result = test_password(passphrase)
        strength_label.config(text=f"Password Strength: {strength_result['score']}/4")
        feedback_label.config(text="\n".join(strength_result['feedback']))

    except ValueError as e:
        messagebox.showerror("Error", f"An error occurred while generating the passphrase:\n{e}")


def copy_to_clipboard():
    passphrase = passphrase_label.cget("text").replace("Your new password is: ", "")
    pyperclip.copy(passphrase)



app = tk.Tk()
app.title("Memorable Password Generator")
app.resizable(width=False, height=False)
style = ttk.Style()
style.theme_use("xpnative") 


num_words_label = ttk.Label(app, text="Enter the number of words in the passphrase:")
num_words_label.pack()


num_words_entry = ttk.Entry(app)
num_words_entry.pack()

# Checkbox for including numbers
numbers_var = tk.BooleanVar()
numbers_check = ttk.Checkbutton(app, text="Include a number", variable=numbers_var)
numbers_check.pack()

# Checkbox for including special characters
special_chars_var = tk.BooleanVar(value=True)
special_chars_check = ttk.Checkbutton(app, text="Include a special character", variable=special_chars_var)
special_chars_check.pack()


passphrase_label = ttk.Label(app, text="", wraplength=300)
passphrase_label.pack()


copy_button = ttk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard, state=tk.DISABLED)
copy_button.pack()


load_custom_wordlists = ttk.Button(app, text="Load Custom Wordlist", command=load_custom_wordlist)
load_custom_wordlists.pack()

# Checkbox for including spaces
include_spaces = tk.BooleanVar(value=True)  # Include spaces by default
spaces_check = ttk.Checkbutton(app, text="Include Spaces", variable=include_spaces)
spaces_check.pack()


generate_button = ttk.Button(app, text="Generate Memorable Passphrase", command=generate_button_clicked)
generate_button.pack()

strength_label = ttk.Label(app, text="", wraplength=300)
strength_label.pack()


feedback_label = ttk.Label(app, text="", wraplength=300)
feedback_label.pack()



app.mainloop()