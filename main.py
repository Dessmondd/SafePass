import tkinter as tk
from tkinter import messagebox, ttk
import secrets
import string
import pyperclip
import threading
from ttkthemes import ThemedTk
from modules.password_strength_tester import test_password
from modules.wordlist import wordlist
from modules.clipboard_manager import clear_duration, clear_clipboard
from modules.leakedornot import check_pwned


class PasswordGenerator:
    def __init__(self):
        self.app = ThemedTk(theme="arc")
        self.app.title("SafePass - Password Generator")
        self.app.resizable(width=False, height=False)
        self.style = ttk.Style()

        self.include_spaces = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar()
        self.special_chars_var = tk.BooleanVar(value=True)
        self.test_button = tk.Button(text="Test")
        self.passphrases = []  # store the passphrases separately
        self.passphrase_labels = []  # store the labels separately
        self.create_widgets()

    def toggle_multiple_passphrases(self):
        if self.multiple_passphrases_var.get():
            self.num_passphrases_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
            self.num_passphrases_spinbox.grid(row=3, column=1, padx=10, pady=5)
            self.num_passphrases_spinbox.config(state="normal")
        else:
            self.num_passphrases_label.grid_forget()
            self.num_passphrases_spinbox.grid_forget()
            self.num_passphrases_spinbox.config(state="disabled")

    def create_widgets(self):
        self.create_num_words_widget()
        self.create_check_buttons()
        self.create_generate_button()
        self.create_feedback_labels()
        self.toggle_multiple_passphrases()
        self.create_dark_white_mode_button()

    def create_num_words_widget(self):
        num_words_label = ttk.Label(self.app, text="Number of words:")
        num_words_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.num_words_entry = ttk.Entry(self.app, validate="key", validatecommand=(self.app.register(self.validate_num_words), '%P'))
        self.num_words_entry.grid(row=0, column=1, padx=10, pady=5)

    def create_check_buttons(self):
        numbers_check = ttk.Checkbutton(self.app, text="Include a number", variable=self.numbers_var)
        numbers_check.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        special_chars_check = ttk.Checkbutton(self.app, text="Include a special character", variable=self.special_chars_var)
        special_chars_check.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        spaces_check = ttk.Checkbutton(self.app, text="Include Spaces", variable=self.include_spaces)
        spaces_check.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.multiple_passphrases_var = tk.BooleanVar(value=False)
        self.multiple_passphrases_check = ttk.Checkbutton(self.app, text="Generate multiple passphrases", variable=self.multiple_passphrases_var, command=self.toggle_multiple_passphrases)
        self.multiple_passphrases_check.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.num_passphrases_label = ttk.Label(self.app, text="Number of passphrases:")
        self.num_passphrases_spinbox = ttk.Spinbox(self.app, from_=1, to=5, state="disabled", validate="key", validatecommand=(self.app.register(self.validate_num_passphrases), '%P'))

    def create_generate_button(self):
        generate_button = ttk.Button(self.app, text="Generate", command=self.generate_button_clicked_thread)
        generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def create_feedback_labels(self):
        self.strength_label = ttk.Label(self.app, text="", wraplength=300)
        self.strength_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        self.feedback_label = ttk.Label(self.app, text="", wraplength=300)
        self.feedback_label.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

        self.feedback_crack_time = ttk.Label(self.app, text="", wraplength=300)
        self.feedback_crack_time.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

    def create_dark_white_mode_button(self):
        self.dark_toggle = ttk.Button(self.app, text="Dark/White Mode", command=self.dark_white_mode_toggle)
        self.dark_toggle.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    def validate_num_words(self, input):
        if input.isdigit() and 3 <= int(input) <= 9 or input == "":
            return True
        else:
            return False

    def dark_white_mode_toggle(self):
        self.status = True if self.app["background"] == "#2d2d30" else False
        if not self.status:
            self.style.configure("TLabel", background="#2d2d30", foreground="white")
            self.style.configure("TButton", background="#2d2d30")
            self.style.configure("TCheckbutton", background="#2d2d30", foreground="white")
            self.dark_toggle.configure(style="Gray.TButton")
            self.style.configure("Gray.TButton", background="#2d2d30")
            self.app.configure(background="#2d2d30")
        else:
            self.style.configure("TLabel", background="white", foreground="black")
            self.style.configure("TButton", background="white", foreground="black")
            self.style.configure("TCheckbutton", background="white", foreground="black")
            self.app.configure(background="white")

    def generate_passphrase(self, num_words, add_numbers, add_special_chars, min_digits=1, max_digits=4, capitalize_percentage=60, include_spaces=True):
        for _ in range(20000):  # limit the number of attempts to 100
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

            if not check_pwned(passphrase) and test_password(passphrase)['score'] == 4:
                return passphrase

        raise RuntimeError(f'Unable to generate a secure passphrase after 100 attempts')

    def generate_button_clicked_thread(self):
        threading.Thread(target=self.generate_button_clicked).start()

    def validate_num_passphrases(self, input):
        if input.isdigit() and 2 <= int(input) <= 4 or input == "":
            return True
        else:
            return False
        
    def generate_button_clicked(self):
        num_words = self.num_words_entry.get()
        if num_words is None or num_words == "":
            messagebox.showerror("Error", "Please enter a number of words")
            return
        try:
            num_words = int(num_words)
            if num_words <= 0:
                raise ValueError("Number of words must be a positive integer")
            if num_words > 10:
                num_words = 10
            if self.multiple_passphrases_var.get():
                num_passphrases = int(self.num_passphrases_spinbox.get())
                if num_passphrases > 5:
                    num_passphrases = 5
            else:
                num_passphrases = 1
            passphrases = []

            for i in range(num_passphrases):
                passphrases.append(self.generate_passphrase(num_words, self.numbers_var.get(), self.special_chars_var.get(), include_spaces=self.include_spaces.get()))
            # Destroy previous labels, so it does not overlap.
            for label in self.passphrase_labels:
                label.destroy()

            self.passphrases = passphrases  # store the passphrases
            self.passphrase_labels = []  # clear the old labels
            for i, passphrase in enumerate(passphrases):
                label = ttk.Label(self.app, text=f"Passphrase {i + 1}: {passphrase}", wraplength=300)
                label.grid(row=5 + i, column=0, columnspan=2, padx=10, pady=5)
                label.bind("<Button-1>", self.copy_to_clipboard)  # bind click event
                self.passphrase_labels.append(label)  # store the label

            strength_result = test_password(passphrases[0])
            self.strength_label.config(text=f"Password Strength: {strength_result['score']}/4")
            self.feedback_label.config(text="\n".join(strength_result['feedback']))
            self.feedback_crack_time.config(text="Time needed to crack password: " + strength_result['crack_time'])

        except ValueError as e:
            messagebox.showerror("Error", f"An error occurred while generating the passphrase:\n{e}")

    def copy_to_clipboard(self, event=None):
        # get the index of the clicked label
        label_index = self.passphrase_labels.index(event.widget)
        # get the corresponding passphrase
        passphrase = self.passphrases[label_index]
        pyperclip.copy(passphrase)
        threading.Timer(clear_duration, clear_clipboard).start()

        # provide visual feedback
        event.widget.config(foreground="green")
        self.app.after(2000, lambda: event.widget.config(foreground="black"))  # change color back after 2 seconds

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    PasswordGenerator().run()
