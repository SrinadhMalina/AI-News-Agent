import json
import os
from datetime import date
import customtkinter as ctk
from tkinter import messagebox

# Configuration
DATA_FILE = "daily_tracker/daily_data.json"
TASKS = [
    "Supplement Intake",
    "Water Intake (4L-5L)",
    "Exercise/Gym",
    "Learning German",
    "Games",
    "AI Learning",
    "1 Code",
    "10 Min Meditation"
]

# Appearance settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class HustleTracker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🚀 Daily Hustle Tracker")
        self.geometry("450x700")
        self.resizable(True, True)
        self.after(0, lambda: self.state('zoomed')) # Start maximized on Windows

        # Data state
        self.data = self.load_data()
        self.checkboxes = {}

        # UI Layout
        self.setup_ui()

    def load_data(self):
        today = str(date.today())
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                try:
                    data = json.load(f)
                    if data.get("date") != today:
                        return {"date": today, "tasks": {task: False for task in TASKS}}
                    return data
                except json.JSONDecodeError:
                    pass
        return {"date": today, "tasks": {task: False for task in TASKS}}

    def save_data(self):
        for task, var in self.checkboxes.items():
            self.data["tasks"][task] = var.get()

        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def setup_ui(self):
        # Configure grid for responsiveness
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkLabel(
            self,
            text="DAILY GROWTH ENGINE",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#00FFF7"
        )
        self.header.grid(row=0, column=0, pady=(30, 10), sticky="n")

        self.date_label = ctk.CTkLabel(
            self,
            text=f"Date: {self.data['date']}",
            font=ctk.CTkFont(size=14)
        )
        self.date_label.grid(row=0, column=0, pady=(60, 20), sticky="n")

        # MAIN CONTENT FRAME (Task List)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.tasks_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.tasks_frame.grid(row=0, column=0, sticky="nsew")

        for task in TASKS:
            var = ctk.BooleanVar(value=self.data["tasks"].get(task, False))
            self.checkboxes[task] = var
            cb = ctk.CTkCheckBox(
                self.tasks_frame,
                text=task,
                variable=var,
                font=ctk.CTkFont(size=16),
                checkbox_width=24,
                checkbox_height=24,
                command=self.save_data
            )
            cb.pack(anchor="w", padx=20, pady=12)

        # Bottom Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, pady=30)

        self.report_btn = ctk.CTkButton(
            self.button_frame,
            text="FINALIZE DAY",
            command=self.run_report,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#B22222",
            hover_color="#8B0000",
            width=200,
            height=45
        )
        self.report_btn.grid(row=0, column=0, padx=10)

        self.reset_btn = ctk.CTkButton(
            self.button_frame,
            text="RESET",
            command=self.reset_day,
            font=ctk.CTkFont(size=14),
            fg_color="gray",
            hover_color="#444",
            width=80,
            height=45
        )
        self.reset_btn.grid(row=0, column=1, padx=10)

        # REPORT OVERLAY FRAME (Hidden by default)
        self.report_frame = ctk.CTkFrame(self)
        self.report_frame.grid_columnconfigure(0, weight=1)
        self.report_frame.grid_rowconfigure(0, weight=1)

        self.report_text = ctk.CTkLabel(
            self.report_frame,
            text="",
            font=ctk.CTkFont(size=18, weight="bold"),
            wraplength=350
        )
        self.report_text.grid(row=0, column=0, pady=40, padx=20, sticky="nsew")

        self.timer_label = ctk.CTkLabel(
            self.report_frame,
            text="",
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.timer_label.grid(row=1, column=0, pady=10)

        self.close_report_btn = ctk.CTkButton(
            self.report_frame,
            text="I GOT IT!",
            command=self.close_report,
            width=120
        )
        self.close_report_btn.grid(row=2, column=0, pady=20)

    def reset_day(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset today's progress?"):
            for var in self.checkboxes.values():
                var.set(False)
            self.save_data()

    def run_report(self):
        completed_count = sum(var.get() for var in self.checkboxes.values())
        total_tasks = len(TASKS)

        if completed_count == total_tasks:
            msg = f"🌟 GOOD FULL-FLEDGED DAY! 🌟\n\nScore: {completed_count}/{total_tasks}\n\nYou've conquered everything. Keep this momentum!"
            color = "#00FF00"
        else:
            msg = f"❌ THIS IS NOT ENOUGH! ❌\n\nScore: {completed_count}/{total_tasks}\n\nHustle more to achieve your goals. Tomorrow is a new chance to dominate!"
            color = "#FF0000"

        self.report_text.configure(text=msg, text_color=color)

        # Switch visibility: Hide main content, show report overlay
        self.main_frame.grid_forget()
        self.button_frame.grid_forget()
        self.report_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Timer logic
        self.remaining_time = 10
        self.update_timer()

    def update_timer(self):
        if self.report_frame.winfo_exists():
            if self.remaining_time > 0:
                self.timer_label.configure(text=f"Closing in {self.remaining_time}s...")
                self.remaining_time -= 1
                self.after(1000, self.update_timer)
            else:
                self.close_report()

    def close_report(self):
        # Switch visibility back: Hide report, show main content
        self.report_frame.grid_forget()
        self.main_frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        self.button_frame.grid(row=2, column=0, pady=30)
        self.remaining_time = 0

if __name__ == "__main__":
    try:
        app = HustleTracker()
        app.mainloop()
    except Exception as e:
        print(f"Error launching GUI: {e}")
