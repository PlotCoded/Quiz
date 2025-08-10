import customtkinter as ctk
import tkinter as tk
import os

class Delete:
	def __init__(self, app):
		self.app = app

	def window(self):
		if self.app.window_up == False:
            # Control variable to prevent more than one editor window from opening at the same time
			self.app.window_up = True

			def delete():
				filenames = os.listdir(r"C:\Users\hp\Documents\Quiz\Storage")

				for file in filenames:
					print(file)
					if ".csv" in file and file[:-4] == self.delete_bar_var.get():
						you_sure = tk.messagebox.askyesno(title="Delete?", message="Are you sure you want to deleted this subject?")
						
						if you_sure:
							self.app.window_up = False
							self.window.destroy()

							# Deleting the topic/file
							os.remove(f"C:\\Users\\hp\\Documents\\Quiz\\Storage\\{self.delete_bar_var.get()}.csv")

							exec(f"self.app.menu.v{self.delete_bar_var.get()}.pack_forget()")

							# # Redisplaying the menu page
							# # First remving the previous 
							# filenames = os.listdir(r"C:\Users\hp\Documents\Quiz\Storage")
        					# self.topic_names = []

        					# for file in filenames:
					        #     if ".csv" in file:
					        #         self.topic_names.append(file) # I might not been this list

					        #         # Displaying the topic on the menu
					        #         exec(f"self.{file[::-4]} = ctk.CTkButton(self.scroll_frame, text='{file[:-4]}', command=self.app.question_page.starting)")
					        #         exec(f"self.{file[::-4]}.pack(pady=50)")
							break
						else:
							break
				else:
					self.frame.pack_forget()

					self.error.pack(pady=50)
					self.frame.pack(expand=True, fill="x")

			def cancel():
				self.app.window_up = False
				self.window.destroy()

			self.window = ctk.CTkToplevel(self.app)
			self.window.transient(self.app)
			self.window.title("Delete")
			self.window.geometry("750x500+500+150")

			#Search Bar
			self.delete_bar_var = tk.StringVar()
			self.delete_bar = ctk.CTkEntry(self.window, textvariable=self.delete_bar_var, placeholder_text="Please enter a topic", placeholder_text_color="#939393", justify="center", width=350, height=50, border_width=2)
			self.delete_bar.pack(pady=30)

			#Error Message
			self.error = ctk.CTkLabel(self.window, text="Sorry, this topic doesn't exist", text_color="red")

			#Search and Cancel button
			self.frame = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")
			self.frame.pack(expand=True, fill="x")

			#Search Button
			self.delete_button = ctk.CTkButton(self.frame, text="Delete", border_width=0, command=delete)
			self.delete_button.pack(expand=True, side="left")

			#Cancel Button
			self.cancel_button = ctk.CTkButton(self.frame, text="Cancel", border_width=0, command=cancel)
			self.cancel_button.pack(expand=True, side="right")

			self.window.protocol("WM_DELETE_WINDOW", cancel)