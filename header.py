import customtkinter as ctk
import tkinter as tk

class Header:
    def __init__(self, app):
        self.app = app

    def header(self):
        #Header scroll_frame
        self.scroll_frame = ctk.CTkFrame(self.app)
        self.scroll_frame.grid(row=0,column=0, columnspan=21, sticky="nsew")

        #Menu Button
        self.menu_button = ctk.CTkButton(self.scroll_frame, text="Menu",width=165,height=85,corner_radius=10, command=lambda: None)
        self.menu_button.pack(side="left", padx=10)

        #Creating the topic label
        #Note: This is an entry acting as a label.I used this because labels don't have a border I think
        self.topic_selected = "None"
        self.subject_var = tk.StringVar(value = f"Topic: {self.topic_selected}")
        self.topic_label = ctk.CTkEntry(self.scroll_frame, textvariable=self.subject_var, width=250,height=65, corner_radius=100,border_width=3, justify="center",state="disabled")
        self.topic_label.pack(expand=True, side="left")

        #Creating the time label
        #Note: This is an entry acting as a label because labels don't have a border
        self.time = "00:00:00"
        self.time_var = tk.StringVar(value = f"Time: {self.time}")
        self.time_label= ctk.CTkEntry(self.scroll_frame, textvariable=self.time_var, width=250,height=65, corner_radius=100,border_width=3, justify="center",state="disabled")
        self.time_label.pack(expand=True, side="left")

        #Creating the marks label
        #Note: This is an entry acting as a label because labels don't have a border        
        self.marks = 0
        self.score_var = tk.StringVar(value = f"Marks: {self.marks}")
        self.marks_label= ctk.CTkEntry(self.scroll_frame, textvariable=self.score_var, width=250, height=65, corner_radius=100,border_width=3, justify="center",state="disabled")
        self.marks_label.pack(expand=True, side="left")