import os
import time
import subprocess
import win32gui
import win32process
import psutil
import run_macro


def create_midas_data(solar_path, building_path, design_path):
    macro = run_macro
    
    for path in [solar_path, building_path, design_path]:
        if path is None:
            print("Path is not specified!")
            return

        process = open_midas(path)

        if process is None:
            print("Failed to open Midas Gen.")
            return
        
        # 자동 클릭
        macro.run_macro_without_gui()

        # 프로세스가 종료
        process.terminate()  # 프로세스 종료

    print(f"Creating MIDAS data with {solar_path}, {building_path}, {design_path}...")


def open_midas(file):
    # 파일 확장자에 따라 프로그램 이름을 결정합니다.
    program_name = "MidasGen.exe" if file.endswith(".mgb") else "Design+.exe"
    midas_exe = find_midas_exe(program_name)

    if midas_exe is None:
        print(f"{program_name} not found!")
        return

    try:
        # subprocess.Popen을 사용하여 명령을 비동기로 실행
        command = [midas_exe, file]
        print(f"Executing command: {' '.join(command)}")
        process = subprocess.Popen(command)  # 비동기 실행으로 전환
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # 프로그램이 열릴 때까지 대기
    if not wait_for_midas_gen_open(file):
        print("Failed to open Midas Gen within the expected time.")
        return

    return process


def find_midas_exe(program_name):
    # 특정 경로가 아닌, MidasGen.exe가 있는지 찾기 위한 로직을 단순화
    search_paths = ["C:\\Program Files", "C:\\Program Files (x86)"]
    for search_path in search_paths:
        for root, dirs, files in os.walk(search_path):
            if program_name in files:
                return os.path.join(root, program_name)
    return None


def wait_for_midas_gen_open(file_path, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_midas_gen_open(file_path):
            # 클릭을 할 수 있을정도로 제대로 열릴때 까지 대기
            print("Midas Gen opened successfully.")
            time.sleep(15)
            
            return True
        print("Waiting for Midas Gen to open...")
        time.sleep(5)
    return False


def is_midas_gen_open(file_path):
    hwnds = _get_hwnds_by_filepath(file_path)
    return bool(hwnds)


def _get_hwnds_by_filepath(file_path):
    hwnds = []

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                if any(file_path.lower() in cmd.lower() for cmd in process.cmdline()):
                    hwnds.append(hwnd)
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
        return True

    win32gui.EnumWindows(callback, hwnds)
    return hwnds
