import json
import time
import cv2
import numpy as np
import pyautogui
from pynput import mouse, keyboard
from tkinter import messagebox


class AutomationMacro:
    def __init__(self, app):
        self.app = app
        self.actions = []
        self.is_recording = False
        self.mouse_listener = None
        self.keyboard_listener = None
        self.last_action_time = None

    def start_recording(self):
        self.actions = []
        self.is_recording = True
        self.last_action_time = time.time()

        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)

        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_recording(self):
        self.is_recording = False

        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def save_actions(self, file_path="recorded_actions.json"):
        with open(file_path, "w") as file:
            json.dump(self.actions, file, indent=4)

    def load_actions(self, file_path):
        with open(file_path, "r") as file:
            self.actions = json.load(file)

    def play_recording(self):
        try:
            for action in self.actions:
                if not self.check_pre_click_conditions(action):
                    continue  # 조건이 만족되지 않으면 클릭 생략
                time.sleep(action["delay"])
                if action["type"] == "click":
                    self.execute_click_action(action)
                elif action["type"] == "keypress":
                    self.simulate_keypress(action["key"])
        except Exception as e:
            print(f"Error during playback: {e}")
            messagebox.showerror("Error", f"An error occurred during playback: {e}")

    def execute_click_action(self, action):
        try:
            x, y = action["x"], action["y"]

            # 이미지 검색 기능이 활성화된 경우
            if action.get("use_image_search") and action.get("image_path"):
                location = self.find_image_on_screen(action["image_path"])
                if location is not None:
                    x, y = location  # 이미지의 중앙 좌표로 설정
                    # x_offset과 y_offset 값을 추가 또는 감소
                    x += action.get("x_offset", 0)
                    y += action.get("y_offset", 0)
                else:
                    print(f"Image not found on screen: {action['image_path']}")
                    return

            # 최종 클릭 실행
            self.simulate_click(x, y, action["button"])
        except Exception as e:
            print(f"Error executing click action: {e}")
            raise

    def check_pre_click_conditions(self, action):
        try:
            condition = action.get("pre_click_condition", "None")
            images = action.get("pre_click_images", [])

            print(f"Checking condition: {condition} with images: {images}")

            if condition == "None":
                return True
            elif condition == "이미지가 있으면 생략":
                for image in images:
                    if self.find_image_on_screen(image) is not None:
                        print(f"Skipping click because {image} is present.")
                        return False
            elif condition == "이미지가 없으면 생략":
                for image in images:
                    if self.find_image_on_screen(image) is None:
                        print(f"Skipping click because {image} is missing.")
                        return False
            elif condition == "이미지 찾을때 까지 대기":
                start_time = time.time()
                while time.time() - start_time < 300:  # 최대 5분 대기
                    try:
                        found = all(
                            self.find_image_on_screen(image) is not None
                            for image in images
                        )
                        if found:
                            print("All images found on screen.")
                            return True
                        else:
                            print("Waiting for images to appear...")
                    except Exception as e:
                        print(f"Unexpected error while locating image: {e}")
                    time.sleep(1)
                print("Timeout waiting for images.")
                return False
            return True
        except Exception as e:
            print(f"Error checking pre-click conditions: {e}")
            messagebox.showerror("Error", f"Error checking pre-click conditions: {e}")
            return False

    def find_image_on_screen(self, image_path):
        try:
            # 화면의 스크린샷을 캡처하여 numpy 배열로 변환
            screen = pyautogui.screenshot()
            screen_np = np.array(screen)
            screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

            # 대상 이미지를 읽어서 회색조로 변환
            target_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if target_image is None:
                print(f"Failed to load image: {image_path}")
                return None

            # 이미지 매칭을 통해 위치를 찾음
            result = cv2.matchTemplate(screen_gray, target_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # 매칭 결과가 일정 임계값 이상일 때 위치 반환
            threshold = 0.8
            if max_val >= threshold:
                target_height, target_width = target_image.shape
                center_x = max_loc[0] + target_width // 2
                center_y = max_loc[1] + target_height // 2
                return center_x, center_y
            else:
                return None
        except Exception as e:
            print(f"Error finding image on screen: {e}")
            return None

    def on_click(self, x, y, button, pressed):
        try:
            if self.is_recording and pressed:
                if self.is_click_inside_gui(x, y):
                    return

                current_time = time.time()
                delay = current_time - self.last_action_time
                self.last_action_time = current_time

                self.actions.append(
                    {
                        "type": "click",
                        "x": x,
                        "y": y,
                        "button": str(button),
                        "delay": delay,
                        "use_image_search": False,
                        "image_path": "",
                        "x_offset": 0,
                        "y_offset": 0,
                        "pre_click_condition": "None",
                        "pre_click_images": [],
                    }
                )
                self.app.load_actions()
        except Exception as e:
            print(f"Error recording click: {e}")

    def on_press(self, key):
        try:
            if self.is_recording:
                current_time = time.time()
                delay = current_time - self.last_action_time
                self.last_action_time = current_time

                self.actions.append(
                    {"type": "keypress", "key": str(key), "delay": delay}
                )
                self.app.load_actions()
        except Exception as e:
            print(f"Error recording key press: {e}")

    def simulate_click(self, x, y, button):
        try:
            pyautogui.moveTo(x, y)
            if button == "Button.left":
                pyautogui.click()
            elif button == "Button.right":
                pyautogui.click(button="right")
        except Exception as e:
            print(f"Error simulating click: {e}")

    def simulate_keypress(self, key):
        from pynput.keyboard import Controller, Key

        keyboard_controller = Controller()
        try:
            # 문자열이 'Key.'로 시작하면 평가하여 특수 키로 처리, 아니면 일반 문자열로 처리
            if "Key." in key:
                key = eval(key)  # 'Key.enter'와 같은 특수 키 처리
                keyboard_controller.press(key)
                keyboard_controller.release(key)
            else:
                # 문자열로 입력된 키를 각각 입력
                key_str = key.strip("'")

                # .jpg 로 끝나면 프로그램의 위치를 더해준다.
                path = os.path.dirname(os.path.abspath(__file__))
                if key_str.endswith(".jpg"):
                    key_str = os.path.join(path, key_str)

                for char in key_str:
                    keyboard_controller.press(char)
                    keyboard_controller.release(char)

        except Exception as e:
            print(f"Error simulating key press: {e}")

    def is_click_inside_gui(self, x, y):
        gui_x = self.app.root.winfo_rootx()
        gui_y = self.app.root.winfo_rooty()
        gui_width = self.app.root.winfo_width()
        gui_height = self.app.root.winfo_height()

        return gui_x <= x <= gui_x + gui_width and gui_y <= y <= gui_y + gui_height

    def get_actions(self):
        return self.actions
