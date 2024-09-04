# macro_gui.py
import tkinter as tk
from tkinter import messagebox, filedialog
from macro_core import AutomationMacro


class MacroApp:
    def __init__(self, root):
        self.root = root
        self.macro = AutomationMacro()

        # Tkinter GUI setup
        self.root.title("Automation Macro")

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

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

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

        # Save recorded actions to file
        self.macro.save_actions()
        messagebox.showinfo("Recording", "Recording saved to recorded_actions.json")

    def load_recording(self):
        # Open file dialog to select a .json file
        file_path = filedialog.askopenfilename(
            title="Select Recorded File", filetypes=[("JSON Files", "*.json")]
        )
        if file_path:
            try:
                self.macro.load_actions(file_path)
                messagebox.showinfo("Load Recording", "Recording loaded successfully.")
                self.play_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def play_recording(self):
        try:
            self.macro.play_recording()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during playback: {e}")

    def on_close(self):
        # Safely close listeners and exit application
        self.macro.stop_recording()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
