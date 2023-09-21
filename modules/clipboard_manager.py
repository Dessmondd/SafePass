import pyperclip 
import time 
import threading 
clear_duration = 30 # seconds 

def clear_clipboard():
    pyperclip.copy("")

clear_clipboard_thread = threading.Thread(target=clear_clipboard)
clear_clipboard_thread.daemon = True


