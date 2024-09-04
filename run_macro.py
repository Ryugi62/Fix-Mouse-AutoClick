# run_macro.py
import sys
from macro_core import AutomationMacro
from macro_gui import main as gui_main


def run_macro_with_gui():
    # GUI를 띄우는 메인 함수 호출
    gui_main()


def run_macro_without_gui(file_path="recorded_actions.json"):
    # GUI 없이 매크로 실행
    macro = AutomationMacro()
    try:
        macro.load_actions(file_path)
        macro.play_recording()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # 인자에 따라 GUI를 띄울지 여부를 선택
    if len(sys.argv) > 1 and sys.argv[1] == "--no-gui":
        run_macro_without_gui()
    else:
        run_macro_with_gui()
