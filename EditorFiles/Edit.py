# proceed
import customtkinter as ctk
import tkinter as tk
from PIL import Image
import time, os, pandas

from EditorFiles import ExFunc

class Edit:
	def __init__(self, app):
		self.app = app

	def destroyCommand(self):
		you_sure = tk.messagebox.askyesno(title="Exit", message="Are you sure you want to exit out of this window?", default="no")

		if you_sure:
			self.window.destroy()
			self.app.window_up = False

	def scrollWindow(self):
		if self.app.window_up == False:
			# Widgets
			self.app.window_up = True

			self.window = ctk.CTkToplevel(self.app)
			self.window.transient(self.app)
			self.window.title("Add")
			self.window.geometry("800x550+300+50")

			# Implementing the exit command
			self.window.protocol("WM_DELETE_WINDOW", lambda: self.destroyCommand())

			self.scroll_frame = ctk.CTkScrollableFrame(self.window, corner_radius=0, border_width=0, fg_color="#c3c3c3",orientation="vertical", width=750, height=500)

			self.displayScrollPage()

	def displayScrollPage(self):
		self.scroll_frame.pack()

	def displayTopics(self):
		self.topic_buttons = {}

		# Inserting the topics
		filenames = os.listdir(r"C:\Users\hp\Documents\Quiz\Storage")

		for file in filenames:
		    if file.endswith(".csv"):
		        file_name = file[:-4]  # remove ".csv"
		        # capture the current file_name in the lambda default
		        call = lambda f=file_name: self.__init__(f)
		        button = ctk.CTkButton(self.scroll_frame, text=file_name, command=call)
		        button.pack(pady=50)
		        self.topic_buttons[file_name] = button
