import tkinter as tk
from tkinter import messagebox, ttk
import secrets
import string
import pyperclip
import threading
import time
from modules.password_strength_tester import test_password
from modules.wordlist import wordlist
from modules.clipboard_manager import clear_duration, clear_clipboard
from modules.leakedornot import check_pwned

class PasswordGenerator:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Memorable Password Generator")
        self.app.resizable(width=False, height=False)
        self.style = ttk.Style()
        self.style.theme_use("xpnative")

        self.include_spaces = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar()
        self.special_chars_var = tk.BooleanVar(value=True)
        self.test_button = tk.Button(text="Test")
        self.create_widgets()

    def create_widgets(self):
        num_words_label = ttk.Label(self.app, text="Enter the number of words in the passphrase:")
        num_words_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.num_words_entry = ttk.Entry(self.app)
        self.num_words_entry.grid(row=0, column=2, padx=10, pady=5)

        numbers_check = ttk.Checkbutton(self.app, text="Include a number", variable=self.numbers_var)
        numbers_check.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        special_chars_check = ttk.Checkbutton(self.app, text="Include a special character", variable=self.special_chars_var)
        special_chars_check.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        spaces_check = ttk.Checkbutton(self.app, text="Include Spaces", variable=self.include_spaces)
        spaces_check.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        
        generate_button = ttk.Button(self.app, text="Generate Memorable Passphrase", command=self.generate_button_clicked)
        generate_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.passphrase_label = ttk.Label(self.app, text="", wraplength=300)
        self.passphrase_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        self.copy_button = ttk.Button(self.app, text="Copy to Clipboard", command=self.copy_to_clipboard, state=tk.DISABLED)
        self.copy_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

        self.strength_label = ttk.Label(self.app, text="", wraplength=300)
        self.strength_label.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

        self.feedback_label = ttk.Label(self.app, text="", wraplength=300)
        self.feedback_label.grid(row=7, column=0, columnspan=3, padx=10, pady=5)
        
        self.feedback_crack_time = ttk.Label(self.app, text="", wraplength=300)
        self.feedback_crack_time.grid(row=8, column=0, columnspan=3, padx=10, pady=5)

        self.feedback_warning = ttk.Label(self.app, text="", wraplength=300)
        self.feedback_warning.grid(row=9, column=0, columnspan=3, padx=10, pady=5)


    def generate_passphrase(self, num_words, add_numbers, add_special_chars, min_digits=1, max_digits=4, capitalize_percentage=60, include_spaces=True):
        words = [secrets.choice(wordlist).capitalize() for _ in range(num_words)]

        if add_numbers:
            num_digits = secrets.randbelow(max(max_digits - min_digits + 1, 1)) + min_digits
            for _ in range(num_digits):
                insert_pos = secrets.randbelow(max(1, len(words) + 1))
                words.insert(insert_pos, secrets.choice(string.digits))

        if add_special_chars:
            words.insert(secrets.randbelow(len(words) + 1), secrets.choice(string.punctuation))

        secrets.SystemRandom().shuffle(words)

        for _ in range(round(len(words) * (capitalize_percentage / 100))):
            random_word = secrets.randbelow(len(words))
            words[random_word] = words[random_word].capitalize()

        passphrase = ' '.join(words) if include_spaces else ''.join(words)
    
        if not check_pwned(passphrase):
            return passphrase
            
        raise RuntimeError(f'Unable to generate a secure passphrase after attempts')
     
    def generate_button_clicked(self):
        try:
            num_words = int(self.num_words_entry.get())
            if num_words <= 0:
                raise ValueError("Number of words must be a positive integer")

            passphrase = self.generate_passphrase(num_words, self.numbers_var.get(), self.special_chars_var.get(), include_spaces=self.include_spaces.get())

            self.passphrase_label.config(text=f"Your new password is: {passphrase}")
            self.copy_button.config(state=tk.NORMAL)

            strength_result = test_password(passphrase)
            self.strength_label.config(text=f"Password Strength: {strength_result['score']}/4")
            self.feedback_label.config(text="\n".join(strength_result['feedback']))
            self.feedback_crack_time.config(text="Time needed for crack the password: " + strength_result['crack_time'])
            
        except ValueError as e:
            messagebox.showerror("Error", f"An error occurred while generating the passphrase:\n{e}")

    def copy_to_clipboard(self):
        passphrase = self.passphrase_label.cget("text").replace("Your new password is: ", "")
        pyperclip.copy(passphrase)
        threading.Timer(clear_duration, clear_clipboard).start()

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    PasswordGenerator().run()
