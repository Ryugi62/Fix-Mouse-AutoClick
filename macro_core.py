# macro_core.py
import json
import time
import pyautogui
from pynput import mouse, keyboard


class AutomationMacro:
    def __init__(self):
        self.actions = []  # Recorded actions
        self.is_recording = False
        self.mouse_listener = None
        self.keyboard_listener = None
        self.last_action_time = None  # To calculate time between actions

    def start_recording(self):
        self.actions = []
        self.is_recording = True
        self.last_action_time = time.time()  # Initialize the last action time

        # Start mouse and keyboard listeners in separate threads
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)

        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_recording(self):
        self.is_recording = False

        # Stop listeners
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def save_actions(self, file_path="recorded_actions.json"):
        # Save recorded actions to .json file
        with open(file_path, "w") as file:
            json.dump(self.actions, file, indent=4)

    def load_actions(self, file_path):
        # Load recorded actions from .json file
        with open(file_path, "r") as file:
            self.actions = json.load(file)

    def play_recording(self):
        for action in self.actions:
            time.sleep(action["delay"])  # Wait for the recorded delay time
            if action["type"] == "click":
                # Re-execute mouse clicks
                x, y, button = action["x"], action["y"], action["button"]
                self.simulate_click(x, y, button)
            elif action["type"] == "keypress":
                # Re-execute key presses
                key = action["key"]
                self.simulate_keypress(key)

    def on_click(self, x, y, button, pressed):
        if self.is_recording and pressed:
            # Calculate the time delay since the last action
            current_time = time.time()
            delay = current_time - self.last_action_time
            self.last_action_time = current_time

            # Record mouse click with delay
            self.actions.append(
                {"type": "click", "x": x, "y": y, "button": str(button), "delay": delay}
            )

    def on_press(self, key):
        if self.is_recording:
            # Calculate the time delay since the last action
            current_time = time.time()
            delay = current_time - self.last_action_time
            self.last_action_time = current_time

            # Record key press with delay
            self.actions.append({"type": "keypress", "key": str(key), "delay": delay})

    def simulate_click(self, x, y, button):
        # Use pyautogui to simulate a mouse click at (x, y) with a specific button
        pyautogui.moveTo(x, y)
        if button == "Button.left":
            pyautogui.click()
        elif button == "Button.right":
            pyautogui.click(button="right")

    def simulate_keypress(self, key):
        # Function to simulate a key press
        from pynput.keyboard import Controller, Key

        keyboard_controller = Controller()
        try:
            # Handle special keys like Key.enter, Key.space, etc.
            key = eval(key) if "Key." in key else key.replace("'", "")
            keyboard_controller.press(key)
            keyboard_controller.release(key)
        except Exception as e:
            print(f"Error simulating key press: {e}")
