import pyperclip 
import time 
import threading 

clear_duration = 30 # seconds 

def clear_clipboard():
    pyperclip.copy("")

    while True:
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            time.sleep(clear_duration)
            clear_clipboard()

clear_clipboard_thread = threading.Thread(target=clear_clipboard)
clear_clipboard_thread.daemon = True
clear_clipboard_thread.start()

