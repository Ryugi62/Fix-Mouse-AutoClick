# run_macro.py

import os
import sys
import time
import pyperclip
from macro_core import AutomationMacro
from macro_gui import main as gui_main
from excel_processor import create_temp_excel, set_clipboard_from_excel
from map_fetcher import fetch_and_save_static_map


def run_macro_with_gui():
    # GUI를 띄우는 메인 함수 호출
    gui_main()


def run_macro_without_gui(mode=None):
    # 현재 파일의 디렉토리 경로를 가져옴
    path = os.path.dirname(__file__)

    # 각 모드에 따른 파일 리스트
    solar_files = [
        "close_notice.json",
        "display.json",
        "calculate.json",
        "reset_zoom.json",
        "open_code_checking.json",
        "copy_code_checking.json",
        "save_code_checking.json",
        "reset_zoom.json",
        "open_cold_code_checking.json",
        "copy_cold_code_checking.json",
        "save_cold_code_checking.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "copy_section_table_data.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_inactive_dummy.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_boundaries_supports.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load1.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load2.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load3.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load4.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load5.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load6.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load7.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load8.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load9.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load10.json",
        "reset_zoom.json",
        "open_reaction_forces_moments.json",
        "save_reaction_forces_moments.json",
        "reset_zoom.json",
        "open_displacement_contour.json",
        "save_displacement_contour.json",
        "reset_zoom.json",
        "open_beam_diagrams_max_myz.json",
        "save_beam_diagrams_max_myz.json",
        "reset_zoom.json",
        "open_beam_diagrams_min_myz.json",
        "save_beam_diagrams_min_myz.json",
        "reset_zoom.json",
        "open_beam_diagrams_max_fyz.json",
        "save_beam_diagrams_max_fyz.json",
        "reset_zoom.json",
        "open_beam_diagrams_min_fyz.json",
        "save_beam_diagrams_min_fyz.json",
        "reset_zoom.json",
        "open_mode1.json",
        "save_mode1.json",
        "reset_zoom.json",
        "open_mode2.json",
        "save_mode2.json",
        "reset_zoom.json",
        "open_mode3.json",
        "save_mode3.json",
        "reset_zoom.json",
        "open_mode4.json",
        "save_mode4.json",
        "reset_zoom.json",
        "open_mode5.json",
        "save_mode5.json",
        "reset_zoom.json",
        "open_mode6.json",
        "save_mode6.json",
        "reset_zoom.json",
        "open_mode7.json",
        "save_mode7.json",
        "reset_zoom.json",
        "open_mode8.json",
        "save_mode8.json",
        "reset_zoom.json",
        "open_mode9.json",
        "save_mode9.json",
        "reset_zoom.json",
        "open_mode10.json",
        "save_mode10.json",
        "reset_zoom.json",
        "open_mode11.json",
        "save_mode11.json",
        "reset_zoom.json",
        "open_mode12.json",
        "save_mode12.json",
        "reset_zoom.json",
        "open_mode13.json",
        "save_mode13.json",
        "reset_zoom.json",
        "open_mode14.json",
        "save_mode14.json",
        "reset_zoom.json",
        "open_mode15.json",
        "save_mode15.json",
        "reset_zoom.json",
        "x_displacement.json",
        "save_x_displacement.json",
    ]

    building_files = [
        "close_notice.json",
        "display.json",
        "calculate.json",
        "reset_zoom.json",
        "open_code_checking.json",
        "copy_code_checking.json",
        "save_code_checking.json",
        "reset_zoom.json",
        "open_cold_code_checking.json",
        "copy_cold_code_checking.json",
        "save_cold_code_checking.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "copy_section_table_data.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_inactive_dummy.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_boundaries_supports.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load1.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load2.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load3.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load4.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load5.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load6.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load7.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load8.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load9.json",
        "reset_zoom.json",
        "go_top_tree_menu.json",
        "save_load10.json",
        "reset_zoom.json",
        "open_reaction_forces_moments.json",
        "save_reaction_forces_moments.json",
        "reset_zoom.json",
        "open_displacement_contour.json",
        "save_displacement_contour.json",
        "reset_zoom.json",
        "open_beam_diagrams_max_myz.json",
        "save_beam_diagrams_max_myz.json",
        "reset_zoom.json",
        "open_beam_diagrams_min_myz.json",
        "save_beam_diagrams_min_myz.json",
        "reset_zoom.json",
        "open_beam_diagrams_max_fyz.json",
        "save_beam_diagrams_max_fyz.json",
        "reset_zoom.json",
        "open_beam_diagrams_min_fyz.json",
        "save_beam_diagrams_min_fyz.json",
        "reset_zoom.json",
        "x_displacement.json",
        "save_x_displacement.json",
    ]

    design_files = [
        "close_notice.json",
        "design.json",
    ]

    files = []

    if mode == "solar":
        files = solar_files
    elif mode == "building":
        files = building_files
    elif mode == "design":
        files = design_files

    # 파일 경로 생성
    file_paths = [os.path.join(path, "json", file) for file in files]

    # path, results 폴더가 있다면 그 안에 있는 모든 파일을 삭제
    path = os.path.join(os.path.dirname(__file__), "results")
    if os.path.exists(path):
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
    else:
        os.mkdir(path)

    # GUI 없이 매크로 실행, app 인자로 None 전달
    macro = AutomationMacro(app=None)  # 수정된 부분
    for file_path in file_paths:
        try:
            macro.load_actions(file_path)
            macro.play_recording()
        except FileNotFoundError:
            print(f"파일 '{file_path}'을(를) 찾을 수 없습니다.")
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
        finally:
            time.sleep(5)

    # 결과 폴더 이름 변경

    changed_dir = (
        "results_solar"
        if mode == "solar"
        else "results_building" if mode == "building" else "results_design"
    )

    os.rename(
        os.path.join(os.path.dirname(__file__), "results"),
        os.path.join(os.path.dirname(__file__), changed_dir),
    )

    # Example usage of create_temp_excel function
    data1_path = os.path.join(
        os.path.dirname(__file__), changed_dir, "copy_code_checking.txt"
    )
    data2_path = os.path.join(
        os.path.dirname(__file__), changed_dir, "copy_cold_code_checking.txt"
    )
    data3_path = os.path.join(
        os.path.dirname(__file__), changed_dir, "copy_section_table_data.txt"
    )

    excel_path = os.path.join(os.path.dirname(__file__), "template.xlsm")
    result_excel_path = os.path.join(
        os.path.dirname(__file__), changed_dir, f"result.xlsm"
    )

    # Creates a temporary Excel file by processing data
    create_temp_excel(data1_path, data2_path, data3_path, excel_path, result_excel_path)

    # Copies data from the created Excel file to the clipboard
    set_clipboard_from_excel(result_excel_path)

    # 클립보드 내용 출력

    print(f"클립보드 내용: {pyperclip.paste()}")

    # Fetches and saves a satellite image of the specified location
    fetch_and_save_static_map(
        latitude,
        location,
        os.path.join(os.path.dirname(__file__), changed_dir, "map.jpg"),
    )


if __name__ == "__main__":
    # 인자에 따라 GUI를 띄울지 여부를 선택
    if len(sys.argv) > 1 and sys.argv[1] == "--no-gui":
        run_macro_without_gui()
    else:
        run_macro_with_gui()
