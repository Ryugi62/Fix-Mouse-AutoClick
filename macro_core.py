import json
import time
import pyautogui
from pynput import mouse, keyboard


class AutomationMacro:
    def __init__(self, app):
        self.app = app  # MacroApp의 인스턴스를 저장하여 GUI 관련 정보를 사용
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
                if action.get("use_image_search") and action.get("image_path"):
                    # 이미지 검색을 사용해 클릭 위치 탐색
                    location = pyautogui.locateOnScreen(action["image_path"])
                    if location:
                        x, y = pyautogui.center(location)
                        self.simulate_click(x, y, action["button"])
                    else:
                        print(f"Image not found on screen: {action['image_path']}")
                else:
                    # 기존 클릭 실행
                    x, y, button = action["x"], action["y"], action["button"]
                    self.simulate_click(x, y, button)
            elif action["type"] == "keypress":
                # Re-execute key presses
                key = action["key"]
                self.simulate_keypress(key)

    def on_click(self, x, y, button, pressed):
        try:
            if self.is_recording and pressed:
                # GUI 영역 클릭 시 기록 방지
                if self.is_click_inside_gui(x, y):
                    return

                # Calculate the time delay since the last action
                current_time = time.time()
                delay = current_time - self.last_action_time
                self.last_action_time = current_time

                # Record mouse click with delay
                self.actions.append(
                    {
                        "type": "click",
                        "x": x,
                        "y": y,
                        "button": str(button),
                        "delay": delay,
                        "use_image_search": False,  # 기본값으로 이미지 검색 비활성화
                        "image_path": "",  # 기본 이미지 경로 설정
                    }
                )
                # UI에 바로 반영
                self.app.load_actions()
        except NotImplementedError:
            # pynput에서 발생할 수 있는 예외 처리
            print("An unsupported action was attempted.")

    def on_press(self, key):
        try:
            if self.is_recording:
                # Calculate the time delay since the last action
                current_time = time.time()
                delay = current_time - self.last_action_time
                self.last_action_time = current_time

                # Record key press with delay
                self.actions.append(
                    {"type": "keypress", "key": str(key), "delay": delay}
                )
                # UI에 바로 반영
                self.app.load_actions()
        except NotImplementedError:
            # pynput에서 발생할 수 있는 예외 처리
            print("An unsupported action was attempted.")

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

    def is_click_inside_gui(self, x, y):
        # GUI의 영역을 얻어와 클릭 위치와 비교하여 GUI 클릭인지 판단
        gui_x = self.app.root.winfo_rootx()
        gui_y = self.app.root.winfo_rooty()
        gui_width = self.app.root.winfo_width()
        gui_height = self.app.root.winfo_height()

        return gui_x <= x <= gui_x + gui_width and gui_y <= y <= gui_y + gui_height

    def get_actions(self):
        # 액션 리스트 반환 메서드 추가
        return self.actions
