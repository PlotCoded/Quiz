import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os

class Search:
	def __init__(self, app):
		self.app = app

	def window(self):
		if self.app.window_up == False:
            # Control variable to prevent more than one editor window from opening at the same time
			self.app.window_up = True

			def search():
				filenames = os.listdir(r"C:\Users\hp\Documents\Quiz\Storage")

				for file in filenames:
					if ".csv" in file and file[:-4] == self.search_bar_var.get():
						self.window.destroy()
						self.app.question_page.starting()
						self.app.window_up = False
						break
				else:
					self.frame.pack_forget()

					# Error message 
					self.error = ctk.CTkLabel(self.window, text="Sorry, this topic doesn't exist. \n Please enter a topic that has been created", text_color="red")
					self.error.pack(pady=1)

					self.frame.pack(expand=True, fill="x")

			def cancel():
				self.app.window_up = False
				self.window.destroy()

			# Creating a window
			self.window = ctk.CTkToplevel(self.app)
			self.window.transient(self.app)
			self.window.title("Search")
			self.window.geometry("750x500+500+150")

			#Search Bar
			self.search_bar_var = tk.StringVar()
			self.search_bar = ctk.CTkEntry(self.window, textvariable=self.search_bar_var, placeholder_text="Please enter a topic", placeholder_text_color="#939393", justify="center", width=350, height=50, border_width=2)
			self.search_bar.pack(pady=30)

			#Search and Cancel button
			self.frame = ctk.CTkFrame(self.window, border_width=0,fg_color="#c3c3c3")
			self.frame.pack(expand=True, fill="x")

			#Search Button
			self.search_button = ctk.CTkButton(self.frame, text="Search", border_width=0, command=search)
			self.search_button.pack(expand=True, side="left")

			#Cancel Button
			self.cancel_button = ctk.CTkButton(self.frame, text="Cancel", border_width=0, command=cancel)
			self.cancel_button.pack(expand=True, side="right")

			# Implementing the exit command
			self.window.protocol("WM_DELETE_WINDOW", cancel)