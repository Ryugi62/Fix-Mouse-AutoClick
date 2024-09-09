# run_macro.py
import os
import sys
import time
from macro_core import AutomationMacro
from macro_gui import main as gui_main


def run_macro_with_gui():
    # GUI를 띄우는 메인 함수 호출
    gui_main()


def run_macro_without_gui(file_path="recorded_actions.json"):
    path = os.path.dirname(__file__)
    files = [
        "display.json",
        "calculate.json",
        "open_code_checking.json",
        "copy_code_checking.json",
        "save_code_checking.json",
        "open_cold_code_checking.json",
        "copy_cold_code_checking.json",
        "save_cold_code_checking.json",
        "go_top_tree_menu.json",
        "copy_section_table_data.json",
        "go_top_tree_menu.json",
        "save_inactive_dummy.json",
        "go_top_tree_menu.json",
        "save_boundaries_supports.json",
        "go_top_tree_menu.json",
        "save_load1.json",
        "go_top_tree_menu.json",
        "save_load2.json",
        "go_top_tree_menu.json",
        "save_load3.json",
        "go_top_tree_menu.json",
        "save_load4.json",
        "go_top_tree_menu.json",
        "save_load5.json",
        "go_top_tree_menu.json",
        "save_load6.json",
        "go_top_tree_menu.json",
        "save_load7.json",
        "go_top_tree_menu.json",
        "save_load8.json",
        "go_top_tree_menu.json",
        "save_load9.json",
        "go_top_tree_menu.json",
        "save_load10.json",
        "open_reaction_forces_moments.json",
        "save_reaction_forces_moments.json",
        "open_displacement_contour.json",
        "save_displacement_contour.json",
        "open_beam_diagrams_max_myz.json",
        "save_beam_diagrams_max_myz.json",
        "open_beam_diagrams_min_myz.json",
        "save_beam_diagrams_min_myz.json",
        "open_beam_diagrams_max_fyz.json",
        "save_beam_diagrams_max_fyz.json",
        "open_beam_diagrams_min_fyz.json",
        "save_beam_diagrams_min_fyz.json",
        "open_mode1.json",
        "save_mode1.json",
        "open_mode2.json",
        "save_mode2.json",
        "open_mode3.json",
        "save_mode3.json",
        "open_mode4.json",
        "save_mode4.json",
        "open_mode5.json",
        "save_mode5.json",
        "open_mode6.json",
        "save_mode6.json",
        "open_mode7.json",
        "save_mode7.json",
        "open_mode8.json",
        "save_mode8.json",
        "open_mode9.json",
        "save_mode9.json",
        "open_mode10.json",
        "save_mode10.json",
        "open_mode11.json",
        "save_mode11.json",
        "open_mode12.json",
        "save_mode12.json",
        "open_mode13.json",
        "save_mode13.json",
        "open_mode14.json",
        "save_mode14.json",
        "open_mode15.json",
        "save_mode15.json",
        "x_displacement.json",
        "save_x_displacement.json",
    ]

    file_paths = [os.path.join(path, "json", file) for file in files]

    # path, results 폴더가 있다면 그 안에 있는 모든 파일을 삭제한다.
    path = os.path.join(os.path.dirname(__file__), "results")
    if os.path.exists(path):
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))

    # GUI 없이 매크로 실행, app 인자로 None 전달
    macro = AutomationMacro(app=None)  # 수정된 부분
    for file_path in file_paths:
        try:
            macro.load_actions(file_path)
            macro.play_recording()
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            time.sleep(5)


if __name__ == "__main__":
    # 인자에 따라 GUI를 띄울지 여부를 선택
    if len(sys.argv) > 1 and sys.argv[1] == "--no-gui":
        run_macro_without_gui()
    else:
        run_macro_with_gui()
