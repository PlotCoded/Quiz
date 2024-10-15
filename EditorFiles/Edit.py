import customtkinter as ctk

class Edit:
	def __init__(self, app):
		self.app = app

	def window(self):
		self.window = ctk.CTkToplevel(self.app)
		self.window.transient(self.app)
		self.window.title("Edit")
		self.window.geometry("750x500+500+150")