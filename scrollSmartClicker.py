import pyautogui
import cv2
import numpy as np
import time


class ImageAutomation:
    def __init__(self, target_image_path, scroll_region):
        self.target_image = cv2.imread(target_image_path, cv2.IMREAD_COLOR)
        self.scroll_region = scroll_region  # (x, y, width, height)
        self.clicked_targets = []  # List of (x, y) relative to scroll_region
        self.total_scroll = 0
        self.scroll_limit_reached = False

    def find_and_click_target(self):
        while not self.scroll_limit_reached:
            screenshot = np.array(pyautogui.screenshot())
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

            clicked_new = self.process_targets(screenshot)

            if not clicked_new:
                self.scroll_down(screenshot)

    def process_targets(self, screenshot):
        result = cv2.matchTemplate(screenshot, self.target_image, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.8)

        print(result.max())

        clicked_new = False
        for pt in zip(*locations[::-1]):
            x, y = pt
            relative_x = x - self.scroll_region[0]
            relative_y = y - self.scroll_region[1] + self.total_scroll

            if not self.is_clicked_target(relative_x, relative_y):
                pyautogui.click(
                    x + self.target_image.shape[1] // 2,
                    y + self.target_image.shape[0] // 2,
                )
                self.clicked_targets.append((relative_x, relative_y))
                clicked_new = True
                print(f"Clicked on {x}, {y} (relative: {relative_x}, {relative_y})")
                time.sleep(0.5)

        return clicked_new

    def is_clicked_target(self, x, y):
        for cx, cy in self.clicked_targets:
            if abs(x - cx) < 5 and abs(y - cy) < 5:  # 5 픽셀 오차 허용
                return True
        return False

    def scroll_down(self, before_scroll):
        x, y, width, height = self.scroll_region
        pyautogui.moveTo(x + width // 2, y + height // 2)
        pyautogui.scroll(-300)  # Adjust scroll amount as needed
        self.total_scroll += 300
        time.sleep(1)

        after_scroll = np.array(pyautogui.screenshot())
        after_scroll = cv2.cvtColor(after_scroll, cv2.COLOR_RGB2BGR)

        before_region = before_scroll[y : y + height, x : x + width]
        after_region = after_scroll[y : y + height, x : x + width]

        if np.array_equal(before_region, after_region):
            self.scroll_limit_reached = True
            print("Reached the bottom of the page, stopping program.")
        else:
            print(f"Scrolled down, total scroll: {self.total_scroll}")


if __name__ == "__main__":
    target_image_path = "target.png"  # Replace with your target image path
    scroll_region = (
        100,
        100,
        500,
        500,
    )  # Replace with your desired scroll region (x, y, width, height)

    automation = ImageAutomation(target_image_path, scroll_region)
    automation.find_and_click_target()
