import os
import time
import subprocess
import win32gui
import win32process
import psutil
import run_macro


class MidasFileCreator:
    def __init__(self):
        self.macro = run_macro

    def create_midas_data(self, solar_path, building_path, design_path):
        for path in [solar_path, building_path, design_path]:
            mode = (
                "solar"
                if solar_path == path
                else "building" if building_path == path else "design"
            )

            if path is None:
                print("Path is not specified!")
                return

            process = self.open_midas(path)

            if process is None:
                print("Failed to open Midas Gen.")
                return

            self.macro.run_macro_without_gui(mode=mode)

            process.terminate()

        print(
            f"Creating MIDAS data with {solar_path}, {building_path}, {design_path}..."
        )

    def open_midas(self, file):
        program_name = "MidasGen.exe" if file.endswith(".mgb") else "Design+.exe"
        mode = "Gen" if file.endswith(".mgb") else "Design"
        midas_exe = self.find_midas_exe(program_name)

        if midas_exe is None:
            print(f"{program_name} not found!")
            return

        try:
            command = [midas_exe, file]
            print(f"Executing command: {' '.join(command)}")
            process = subprocess.Popen(command)

            # 해당 마이다스의 창 이름을 알아내서 self에 저장해야됨
            self.midas_gen_hwnd = None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return

        if not self.wait_for_midas_gen_open(file):
            print("Failed to open Midas Gen within the expected time.")
            return

        return process

    def find_midas_exe(self, program_name):
        search_paths = ["C:\\Program Files", "C:\\Program Files (x86)"]
        for search_path in search_paths:
            for root, dirs, files in os.walk(search_path):
                if program_name in files:
                    return os.path.join(root, program_name)
        return None

    def wait_for_midas_gen_open(self, file_path, timeout=60):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_midas_gen_open(file_path):

                print("Midas Gen opened successfully.")
                time.sleep(15)

                self.set_midas_window_size(mode)

                return True
            print("Waiting for Midas Gen to open...")
            time.sleep(5)
        return False

    def set_midas_window_size(self, mode="Gen"):
        midas_layout_manager = os.path.join(
            os.path.dirname(__file__), "WindowLayoutManager.exe"
        )
        set_file = "midas_gen.ini" if mode == "Gen" else "midas_design.ini"
        command = [midas_layout_manager, "Midas Gen", set_file]

        try:
            print(f"Executing command: {' '.join(command)}")
            # 실행결과
            result = subprocess.run(command, capture_output=True)
            print(result.stdout.decode("utf-8"))
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            pass

    def is_midas_gen_open(self, file_path):
        hwnds = self._get_hwnds_by_filepath(file_path)

        # 해당 hwnds의 창 이름 출력
        if hwnds:
            print(win32gui.GetWindowText(hwnds[0]))

        return bool(hwnds)

    def _get_hwnds_by_filepath(self, file_path):
        hwnds = []

        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    process = psutil.Process(pid)
                    if any(
                        file_path.lower() in cmd.lower() for cmd in process.cmdline()
                    ):
                        hwnds.append(hwnd)
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass
            return True

        win32gui.EnumWindows(callback, hwnds)
        return hwnds
