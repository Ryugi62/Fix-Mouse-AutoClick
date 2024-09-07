import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
from macro_core import AutomationMacro


class MacroApp:
    def __init__(self, root):
        self.root = root
        self.macro = AutomationMacro(self)
        self.actions = []  # 클릭된 액션을 저장하는 리스트

        # Tkinter GUI setup
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

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # 리스트박스 클릭 시 이벤트
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

        # 녹화된 액션 저장 및 리스트박스 업데이트
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
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def play_recording(self):
        try:
            self.macro.play_recording()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during playback: {e}")

    def load_actions(self):
        # 녹화된 액션을 리스트박스에 로드
        self.actions = self.macro.get_actions()  # 매크로에서 액션 가져오기
        self.action_listbox.delete(0, tk.END)  # 기존 항목 제거
        for action in self.actions:
            self.action_listbox.insert(tk.END, str(action))

    def on_action_select(self, event):
        # 리스트박스 항목이 선택되었을 때 버튼 활성화
        if self.action_listbox.curselection():
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

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

        tk.Label(edit_window, text="X:").grid(row=1, column=0, padx=5, pady=5)
        x_entry = tk.Entry(edit_window)
        x_entry.grid(row=1, column=1, padx=5, pady=5)
        x_entry.insert(0, action.get("x", ""))

        tk.Label(edit_window, text="Y:").grid(row=2, column=0, padx=5, pady=5)
        y_entry = tk.Entry(edit_window)
        y_entry.grid(row=2, column=1, padx=5, pady=5)
        y_entry.insert(0, action.get("y", ""))

        tk.Label(edit_window, text="Button:").grid(row=3, column=0, padx=5, pady=5)
        button_entry = ttk.Combobox(edit_window)
        button_entry["values"] = ["Button.left", "Button.right"]
        button_entry.grid(row=3, column=1, padx=5, pady=5)
        button_entry.set(action.get("button", "Button.left"))

        tk.Label(edit_window, text="Delay:").grid(row=4, column=0, padx=5, pady=5)
        delay_entry = tk.Entry(edit_window)
        delay_entry.grid(row=4, column=1, padx=5, pady=5)
        delay_entry.insert(0, str(action.get("delay", 0)))

        # 이미지 검색 체크박스 추가
        use_image_search = tk.BooleanVar(value=action.get("use_image_search", False))
        tk.Checkbutton(
            edit_window, text="Use Image Search", variable=use_image_search
        ).grid(row=5, column=0, padx=5, pady=5, columnspan=2)

        # 이미지 파일 선택 필드 추가
        tk.Label(edit_window, text="Image Path:").grid(row=6, column=0, padx=5, pady=5)
        image_path_entry = tk.Entry(edit_window, width=40)
        image_path_entry.grid(row=6, column=1, padx=5, pady=5)
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
        select_image_button.grid(row=6, column=2, padx=5, pady=5)

        def save_edits():
            # 각 필드의 값을 가져와 수정된 액션으로 업데이트
            action["type"] = action_type.get()
            action["x"] = int(x_entry.get()) if x_entry.get().isdigit() else 0
            action["y"] = int(y_entry.get()) if y_entry.get().isdigit() else 0
            action["button"] = button_entry.get()
            action["delay"] = float(delay_entry.get())
            action["use_image_search"] = use_image_search.get()
            action["image_path"] = image_path_entry.get()

            self.actions[index] = action
            self.action_listbox.delete(index)
            self.action_listbox.insert(index, str(action))
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save", command=save_edits)
        save_button.grid(row=7, column=0, columnspan=3, pady=10)

    def delete_action(self):
        selected_index = self.action_listbox.curselection()
        if not selected_index:
            return
        index = selected_index[0]
        del self.actions[index]
        self.action_listbox.delete(index)

    def on_close(self):
        self.macro.stop_recording()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
