import pyperclip
import threading

clear_duration = 5  # seconds
clipboard_clear_flag = threading.Event()  
clipboard_clear_thread = None  


def clear_clipboard():
    global clipboard_clear_flag
    while True:
        clipboard_clear_flag.wait(clear_duration)
        if clipboard_clear_flag.is_set():
            pyperclip.copy("")
            clipboard_clear_flag.clear()
        else:
            # If the flag is not set, break out of the loop (otherwise it crashes, software dev moment)
            break 

def start_clipboard_clear_thread():
    global clipboard_clear_thread
    clipboard_clear_thread = threading.Thread(target=clear_clipboard)
    clipboard_clear_thread.daemon = True
    clipboard_clear_thread.start()

def stop_clipboard_clear_thread(force=False):
    global clipboard_clear_thread
    if clipboard_clear_thread and clipboard_clear_thread.is_alive():
        # Clear the flag to stop clipboard clearing
        clipboard_clear_flag.clear()  
        clipboard_clear_thread.join()  
        # Wait for the thread to finish before exiting
        if force:
            clipboard_clear_thread = None  
        # Reset the clipboard clear thread if forced (need a revamp, works for now)
def toggle_clipboard_clearing(state):
    global clipboard_clear_flag
    if state:
        # Set the flag to signal clipboard clearing
        clipboard_clear_flag.set()  
    else:
        # Clear the flag to stop clipboard clearing
        clipboard_clear_flag.clear()  