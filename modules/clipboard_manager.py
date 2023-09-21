import pyperclip 
import time 
import threading 

def clear_clipboard():
    clear_duration = 30 # seconds 
    pyperclip.copy("")

clear_clipboard_thread = threading.Thread(target=clear_clipboard)
clear_clipboard_thread.daemon = True


