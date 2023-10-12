import os
import pyautogui
import keyboard
import pygetwindow as gw
from datetime import datetime

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def screenshot_active_window():
    """Capture a screenshot of the active window based on its title."""
    active_win = gw.getActiveWindow()
    if not active_win:
        print("No active window detected!")
        return

    # Capture screenshot of the active window
    screenshot = pyautogui.screenshot(region=(
        active_win.left, active_win.top, active_win.width, active_win.height))
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_filename = os.path.join(negatives_dir, f'screenshot_{timestamp}.png')
    screenshot.save(screenshot_filename)

    print(f"Screenshot of '{active_win.title}' saved to: {screenshot_filename}")

def main():
    # Define the shortcut key for capturing
    capture_keys = ['ctrl', 'alt', 'a']
    
    # Ensure the 'training_data/negatives' directory exists
    base_dir = os.path.join(os.getcwd(), 'training_data')
    global negatives_dir 
    negatives_dir = os.path.join(base_dir, 'negatives')
    ensure_directory_exists(negatives_dir)

    print(f"Press {' + '.join(capture_keys)} to capture the active window.")
    print("Press 'Ctrl+Shift+Q' to exit.")

    while True:
        if all([keyboard.is_pressed(key) for key in capture_keys]):
            screenshot_active_window()
            
            # Small delay to avoid multiple captures
            keyboard.read_event(suppress=True)  # wait for key release

        # Check if Ctrl + Shift + Q was pressed to exit
        if keyboard.is_pressed('ctrl+shift+q'):
            print("Exiting script.")
            break

if __name__ == "__main__":
    main()
