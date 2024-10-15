import customtkinter as ctk
import tkinter as tk

class Delete:
	def __init__(self, app):
		self.app = app

	def window(self):
		def delete():
			you_sure = tk.messagebox.askyesno(title="Delete?", message="Are you sure you want to deleted this subject?")
			if you_sure:
				self.window.destroy()

		def cancel():
			self.window.destroy()

		self.window = ctk.CTkToplevel(self.app)
		self.window.transient(self.app)
		self.window.title("Delete")
		self.window.geometry("750x500+500+150")

		#Search Bar
		self.search_bar_var = tk.StringVar()
		self.search_bar = ctk.CTkEntry(self.window, placeholder_text="Please enter a topic", placeholder_text_color="#939393", justify="center", width=350, height=50, border_width=2)
		self.search_bar.pack(pady=30)

		#Error Message
		self.error = ctk.CTkLabel(self.window, text="Sorry, this topic doesn't exist", text_color="red")
		self.error.pack(pady=50)

		#Search and Cancel button
		self.frame = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")
		self.frame.pack(expand=True, fill="x")

		#Search Button
		self.search_button = ctk.CTkButton(self.frame, text="Delete", border_width=0, command=delete)
		self.search_button.pack(expand=True, side="left")

		#Cancel Button
		self.cancel_button = ctk.CTkButton(self.frame, text="Cancel", border_width=0, command=cancel)
		self.cancel_button.pack(expand=True, side="right")