
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

    def process_barcode(self):
        if self.current_barcode:
            barcode = ''.join(self.current_barcode)
            print(f"\nBarcode detected: {barcode}")
            self.show_warning()
            self.current_barcode = []

    def on_press(self, key):
        # Block the F2 key if the dialog is open
        if self.dialog_open and key == keyboard.Key.f2:
            print("F2 key press blocked while warning dialog is open.")
            return

        try:
            current_time = time.time()

            # Initialize last_key_time if it's the first key
            if self.last_key_time is None:
                self.last_key_time = current_time

            # Check if this is a new barcode scan based on time gap
            if current_time - self.last_key_time > self.barcode_buffer_time:
                self.process_barcode()
                self.current_barcode = []

            # Update last key time
            self.last_key_time = current_time

            # Add character to current barcode
            if hasattr(key, 'char') and key.char:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] {key.char}")
                self.current_barcode.append(key.char)

            # Process barcode if Enter is pressed
            if key == keyboard.Key.enter:
                self.process_barcode()

        except AttributeError:
            pass

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
