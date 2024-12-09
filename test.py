from pynput import keyboard
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import threading
import time

class BarcodeDetector:
    def __init__(self):
        self.current_barcode = []
        self.barcode_buffer_time = 0.5  # Time window to collect barcode digits
        self.last_key_time = None
        self.dialog_open = False  # Flag to track if the dialog is open

    def show_warning(self):
        # Create a new thread for the popup to avoid blocking the keyboard listener
        def show_popup():
            self.dialog_open = True  # Set the flag to indicate the dialog is open
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning(
                "Barcode Warning",
                "WARNING: Barcode already present on part!\n\nPart should NOT be marked again!"
            )
            root.destroy()
            self.dialog_open = False  # Reset the flag when the dialog is closed

        threading.Thread(target=show_popup, daemon=True).start()

        # Exit on Esc
        if key == keyboard.Key.esc:
            return False

def main():
    detector = BarcodeDetector()
    print("Starting barcode detection... Press ESC to exit")
    print("Waiting for barcode scans...")

    with keyboard.Listener(on_press=detector.on_press) as listener:
        listener.join()

    print("\nProgram ended.")

if __name__ == "__main__":
    main()
