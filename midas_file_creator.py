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
        # 결과 폴더 삭제
        for folder in ["results_solar", "results_building", "results_design"]:
            path = os.path.join(os.path.dirname(__file__), folder)
            if os.path.exists(path):
                for file in os.listdir(path):
                    os.remove(os.path.join(path, file))
                os.rmdir(path)

        # 각 경로에 대해 MIDAS 데이터 생성
        # for path in [solar_path, building_path, design_path]:
        for path in [solar_path]:
            mode = (
                "solar"
                if solar_path == path
                else "building" if building_path == path else "design"
            )

            if path is None:
                print("경로가 지정되지 않았습니다!")
                return

            process = self.open_midas(path)

            if process is None:
                print("Midas Gen을 열지 못했습니다.")
                return

            self.macro.run_macro_without_gui(mode=mode)

            process.terminate()

        print(f"{solar_path}, {building_path}, {design_path}로 MIDAS 데이터 생성 중...")

    def open_midas(self, file):
        program_name = "MidasGen.exe" if file.endswith(".mgb") else "Design+.exe"
        mode = "Gen" if file.endswith(".mgb") else "Design"
        midas_exe = self.find_midas_exe(program_name)

        if midas_exe is None:
            print(f"{program_name}을 찾을 수 없습니다!")
            return

        try:
            command = [midas_exe, file]
            print(f"명령 실행: {' '.join(command)}")
            process = subprocess.Popen(command)

            # 해당 마이다스 창의 핸들을 저장해야 함
            self.midas_gen_hwnd = None
        except Exception as e:
            print(f"예기치 않은 오류가 발생했습니다: {e}")
            return

        if not self.wait_for_midas_gen_open(file, timeout=60, mode=mode):
            print("예상 시간 내에 Midas Gen을 열지 못했습니다.")
            return

        return process

    def find_midas_exe(self, program_name):
        search_paths = ["C:\\Program Files", "C:\\Program Files (x86)"]
        for search_path in search_paths:
            for root, dirs, files in os.walk(search_path):
                if program_name in files:
                    return os.path.join(root, program_name)
        return None

    def wait_for_midas_gen_open(self, file_path, timeout=60, mode="Gen"):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_midas_gen_open(file_path):

                print("Midas Gen이 성공적으로 열렸습니다.")
                time.sleep(15)

                self.set_midas_window_size(mode)

                return True
            print("Midas Gen이 열릴 때까지 대기 중...")
            time.sleep(5)
        return False

    def set_midas_window_size(self, mode="Gen"):
        midas_layout_manager = os.path.join(
            os.path.dirname(__file__), "WindowLayoutManager.exe"
        )
        set_file = "midas_gen.ini" if mode == "Gen" else "midas_design.ini"
        command = [midas_layout_manager, "Midas Gen", set_file]

        try:
            print(f"명령 실행: {' '.join(command)}")
            # 실행 결과
            result = subprocess.run(command, capture_output=True)
            print(result.stdout.decode("utf-8"))
        except Exception as e:
            print(f"예기치 않은 오류가 발생했습니다: {e}")
        finally:
            pass

    def is_midas_gen_open(self, file_path):
        hwnds = self._get_hwnds_by_filepath(file_path)

        # 해당 핸들의 창 이름 출력
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
