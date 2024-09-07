import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from macro_core import AutomationMacro


class MacroApp:
    def __init__(self, root):
        self.root = root
        self.macro = AutomationMacro(self)
        self.actions = []

        self.root.title("Automation Macro")

        # 버튼 설정
        self.record_button = tk.Button(
            self.root, text="Start Recording", command=self.start_recording
        )
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(
            self.root,
            text="Stop Recording",
            command=self.stop_recording,
            state=tk.DISABLED,
        )
        self.stop_button.pack(pady=10)

        self.play_button = tk.Button(
            self.root,
            text="Play Recording",
            command=self.play_recording,
            state=tk.DISABLED,
        )
        self.play_button.pack(pady=10)

        self.load_button = tk.Button(
            self.root, text="Load Recording", command=self.load_recording
        )
        self.load_button.pack(pady=10)

        self.save_button = tk.Button(
            self.root,
            text="Save Recording",
            command=self.save_recording,
            state=tk.DISABLED,
        )
        self.save_button.pack(pady=10)

        # 클릭 로그 리스트박스
        self.action_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.action_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 리스트박스 컨트롤 버튼
        self.edit_button = tk.Button(
            self.root, text="Edit Selected", command=self.edit_action, state=tk.DISABLED
        )
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(
            self.root,
            text="Delete Selected",
            command=self.delete_action,
            state=tk.DISABLED,
        )
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.up_button = tk.Button(
            self.root, text="Move Up", command=self.move_up, state=tk.DISABLED
        )
        self.up_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.down_button = tk.Button(
            self.root, text="Move Down", command=self.move_down, state=tk.DISABLED
        )
        self.down_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.action_listbox.bind("<<ListboxSelect>>", self.on_action_select)

    def start_recording(self):
        self.macro.start_recording()
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.DISABLED)

    def stop_recording(self):
        self.macro.stop_recording()
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)

        self.macro.save_actions()
        self.load_actions()
        messagebox.showinfo("Recording", "Recording saved to recorded_actions.json")

    def load_recording(self):
        file_path = filedialog.askopenfilename(
            title="Select Recorded File", filetypes=[("JSON Files", "*.json")]
        )
        if file_path:
            try:
                self.macro.load_actions(file_path)
                self.load_actions()
                messagebox.showinfo("Load Recording", "Recording loaded successfully.")
                self.play_button.config(state=tk.NORMAL)
                self.save_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def play_recording(self):
        try:
            self.macro.play_recording()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during playback: {e}")

    def save_recording(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Recorded File",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
        )
        if file_path:
            try:
                self.macro.save_actions(file_path)
                messagebox.showinfo("Save Recording", "Recording saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def load_actions(self):
        self.actions = self.macro.get_actions()
        self.action_listbox.delete(0, tk.END)
        for action in self.actions:
            self.action_listbox.insert(tk.END, str(action))

    def on_action_select(self, event):
        if self.action_listbox.curselection():
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            self.up_button.config(state=tk.NORMAL)
            self.down_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.up_button.config(state=tk.DISABLED)
            self.down_button.config(state=tk.DISABLED)

    def edit_action(self):
        selected_index = self.action_listbox.curselection()
        if not selected_index:
            return
        index = selected_index[0]
        action = self.actions[index]

        # 새로운 편집창 열기
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Action")

        # 클릭 액션에 대한 필드
        tk.Label(edit_window, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        action_type = tk.StringVar(value=action["type"])
        type_entry = ttk.Combobox(edit_window, textvariable=action_type)
        type_entry["values"] = ["click", "keypress"]
        type_entry.grid(row=0, column=1, padx=5, pady=5)

        # 키 입력에 대한 필드 (keypress 타입인 경우만 활성화)
        tk.Label(edit_window, text="Key:").grid(row=1, column=0, padx=5, pady=5)
        key_entry = tk.Entry(edit_window)
        key_entry.grid(row=1, column=1, padx=5, pady=5)
        key_entry.insert(0, action.get("key", ""))
        key_entry.config(
            state=tk.NORMAL if action["type"] == "keypress" else tk.DISABLED
        )

        # 클릭 좌표와 가감 필드 추가
        tk.Label(edit_window, text="X:").grid(row=2, column=0, padx=5, pady=5)
        x_entry = tk.Entry(edit_window)
        x_entry.grid(row=2, column=1, padx=5, pady=5)
        x_entry.insert(0, action.get("x", ""))

        tk.Label(edit_window, text="Y:").grid(row=3, column=0, padx=5, pady=5)
        y_entry = tk.Entry(edit_window)
        y_entry.grid(row=3, column=1, padx=5, pady=5)
        y_entry.insert(0, action.get("y", ""))

        # X, Y 가감 필드 추가
        tk.Label(edit_window, text="X Offset:").grid(row=4, column=0, padx=5, pady=5)
        x_offset_entry = tk.Entry(edit_window)
        x_offset_entry.grid(row=4, column=1, padx=5, pady=5)
        x_offset_entry.insert(0, str(action.get("x_offset", 0)))  # 기본값 0

        tk.Label(edit_window, text="Y Offset:").grid(row=5, column=0, padx=5, pady=5)
        y_offset_entry = tk.Entry(edit_window)
        y_offset_entry.grid(row=5, column=1, padx=5, pady=5)
        y_offset_entry.insert(0, str(action.get("y_offset", 0)))  # 기본값 0

        # 이미지 검색 체크박스 추가
        use_image_search = tk.BooleanVar(value=action.get("use_image_search", False))
        tk.Checkbutton(
            edit_window, text="Use Image Search", variable=use_image_search
        ).grid(row=6, column=0, padx=5, pady=5, columnspan=2)

        # 이미지 파일 선택 필드 추가
        tk.Label(edit_window, text="Image Path:").grid(row=7, column=0, padx=5, pady=5)
        image_path_entry = tk.Entry(edit_window, width=40)
        image_path_entry.grid(row=7, column=1, padx=5, pady=5)
        image_path_entry.insert(0, action.get("image_path", ""))

        def select_image_file():
            file_path = filedialog.askopenfilename(
                title="Select Image File",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")],
            )
            image_path_entry.delete(0, tk.END)
            image_path_entry.insert(0, file_path)

        select_image_button = tk.Button(
            edit_window, text="Select Image", command=select_image_file
        )
        select_image_button.grid(row=7, column=2, padx=5, pady=5)

        # 이미지 비교 임계값 설정 필드 추가
        tk.Label(edit_window, text="Match Threshold (0.0 - 1.0):").grid(
            row=8, column=0, padx=5, pady=5
        )
        threshold_entry = tk.Entry(edit_window)
        threshold_entry.grid(row=8, column=1, padx=5, pady=5)
        threshold_entry.insert(0, str(action.get("match_threshold", 0.8)))  # 기본값 0.8

        # Pre-click 조건 설정 필드 추가
        tk.Label(edit_window, text="Pre-click Condition:").grid(
            row=9, column=0, padx=5, pady=5
        )
        pre_click_condition = tk.StringVar(
            value=action.get("pre_click_condition", "None")
        )
        pre_click_condition_entry = ttk.Combobox(
            edit_window, textvariable=pre_click_condition
        )
        pre_click_condition_entry["values"] = [
            "None",
            "이미지가 있으면 생략",
            "이미지가 없으면 생략",
            "이미지 찾을때 까지 대기",
        ]
        pre_click_condition_entry.grid(row=9, column=1, padx=5, pady=5)

        # 이미지 입력 필드 추가
        tk.Label(edit_window, text="Pre-click Images:").grid(
            row=10, column=0, padx=5, pady=5
        )
        pre_click_images_entry = tk.Entry(edit_window, width=40)
        pre_click_images_entry.grid(row=10, column=1, padx=5, pady=5)
        pre_click_images_entry.insert(0, ",".join(action.get("pre_click_images", [])))

        def select_pre_click_images():
            files = filedialog.askopenfilenames(
                title="Select Pre-click Images",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")],
            )
            pre_click_images_entry.delete(0, tk.END)
            pre_click_images_entry.insert(0, ",".join(files))

        select_pre_click_images_button = tk.Button(
            edit_window, text="Select Images", command=select_pre_click_images
        )
        select_pre_click_images_button.grid(row=10, column=2, padx=5, pady=5)

        def save_edits():
            action["type"] = action_type.get()
            action["key"] = (
                key_entry.get()
                if action["type"] == "keypress"
                else action.get("key", "")
            )

            # 좌표와 오프셋 값 가져오기
            action["x"] = int(x_entry.get()) if x_entry.get() else 0
            action["x_offset"] = (
                int(x_offset_entry.get()) if x_offset_entry.get() else 0
            )
            action["y"] = int(y_entry.get()) if y_entry.get() else 0
            action["y_offset"] = (
                int(y_offset_entry.get()) if y_offset_entry.get() else 0
            )

            # 최종 좌표 계산
            action["x"] += action["x_offset"]
            action["y"] += action["y_offset"]

            action["button"] = action.get("button", "Button.left")
            action["delay"] = float(action.get("delay", 0))
            action["use_image_search"] = use_image_search.get()
            action["image_path"] = image_path_entry.get()

            # 임계값 저장
            try:
                threshold_value = float(threshold_entry.get())
                if 0.0 <= threshold_value <= 1.0:
                    action["match_threshold"] = threshold_value
                else:
                    messagebox.showerror(
                        "Error", "Threshold must be between 0.0 and 1.0"
                    )
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid threshold value")
                return

            action["pre_click_condition"] = pre_click_condition.get()
            action["pre_click_images"] = pre_click_images_entry.get().split(",")

            # 수정된 액션 리스트에 업데이트
            self.actions[index] = action
            self.action_listbox.delete(index)
            self.action_listbox.insert(index, str(action))
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save", command=save_edits)
        save_button.grid(row=11, column=0, columnspan=3, pady=10)  # Save 버튼 위치 수정

    def delete_action(self):
        selected_index = self.action_listbox.curselection()
        if not selected_index:
            return
        index = selected_index[0]
        del self.actions[index]
        self.action_listbox.delete(index)

    def move_up(self):
        selected_index = self.action_listbox.curselection()
        if not selected_index or selected_index[0] == 0:
            return
        index = selected_index[0]
        self.actions[index], self.actions[index - 1] = (
            self.actions[index - 1],
            self.actions[index],
        )
        self.load_actions()
        self.action_listbox.select_set(index - 1)

    def move_down(self):
        selected_index = self.action_listbox.curselection()
        if not selected_index or selected_index[0] == len(self.actions) - 1:
            return
        index = selected_index[0]
        self.actions[index], self.actions[index + 1] = (
            self.actions[index + 1],
            self.actions[index],
        )
        self.load_actions()
        self.action_listbox.select_set(index + 1)

    def on_close(self):
        self.macro.stop_recording()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
