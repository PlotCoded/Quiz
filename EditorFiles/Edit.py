# proceed
import customtkinter as ctk
import tkinter as tk
from PIL import Image
import time, os, pandas
from EditorFiles import EditFuncs

from EditorFiles import ExFunc

class Edit:
	def __init__(self, app):
		self.app = app
		self.swap_numbers = []

	def topicsPage(self):
		if self.app.window_up == False:
			# Widgets
			self.app.window_up = True

			self.window = ctk.CTkToplevel(self.app)
			self.window.transient(self.app)
			self.window.title("Add")
			self.window.geometry("800x550+300+50")

			# Implementing the exit command
			self.window.protocol("WM_DELETE_WINDOW", lambda: self.destroyCommand())

			EditFuncs.initialiseAllWidgets(self)
			self.displayScrollPage()

	def destroyCommand(self):
		you_sure = tk.messagebox.askyesno(title="Exit", message="Are you sure you want to exit out of this window?", default="no")

		if you_sure:
			self.window.destroy()
			self.app.window_up = False

	def displayScrollPage(self):
		self.topics_scroll_frame.pack()

		self.displayTopics()

	def displayTopics(self):
		self.topic_buttons = {}

		# Inserting the topics
		filenames = os.listdir(r"C:\Users\hp\Documents\Quiz\Storage")

		for file in filenames:
		    if file.endswith(".csv"):
		        file_name = file[:-4]  # remove ".csv"
		        # capture the current file_name in the lambda default
		        call = lambda f=file_name: self.topicClickedFunc(f)
		        button = ctk.CTkButton(self.topics_scroll_frame, text=file_name, command=call)
		        button.pack(pady=50)
		        self.topic_buttons[file_name] = button

	def forgetTopics(self):
		self.topics_scroll_frame.pack_forget()

		# Inserting the topics
		filenames = os.listdir(r"C:\Users\hp\Documents\Quiz\Storage")

		for file in filenames:
			if file.endswith(".csv"):
				file_name = file[:-4]  # remove ".csv"
				self.topic_buttons[file_name].pack_forget()

	def displayQuestions(self,topic_name):
		self.topic_name = topic_name

		file = rF"C:\Users\hp\Documents\Quiz\Storage\{topic_name}.csv"
		pf = pandas.read_csv(file)
		no_of_questions = pf.shape[0]

		self.questions_scroll_frame.pack(expand=True,fill="both")

		for q in range(1,no_of_questions+1):
			try:
				self.questions_frame[q].pack(side="top",pady=5)
				self.swap_variable[q].pack(side="left",padx=5)
				self.view_question[q].pack(side="left",padx=5)
				self.add_before[q].pack(side="left",padx=5)
				self.add_after[q].pack(side="left",padx=5)
				self.delete[q].pack(side="left",padx=5)
			except:
				pass

		self.questions_page_cancel_button.pack(pady=50)

	def forgetQuestions(self):
		self.questions_scroll_frame.pack_forget()

		pf = pandas.read_csv(self.file)
		no_of_questions = pf.shape[0] # Why do I need this? Nevermind, didn't see the bottom logic

		for q in range(1,no_of_questions+1):
			try:
				self.questions_frame[q].pack_forget()
				self.swap_variable[q].pack_forget()
				self.view_question[q].pack_forget()
				self.add_before[q].pack_forget()
				self.add_after[q].pack_forget()
				self.delete[q].pack_forget()
			except:
				pass
		self.questions_page_cancel_button.pack_forget()

	def topicClickedFunc(self,topic_name):
		self.file = rF"C:\Users\hp\Documents\Quiz\Storage\{topic_name}.csv"

		pf = pandas.read_csv(self.file)
		no_of_questions = pf.shape[0]

		for q in range(1,no_of_questions+1):
			self.questions_frame[q] = ctk.CTkFrame(self.questions_scroll_frame, corner_radius=0, border_width=0, fg_color="#c3c3c3", width=750, height=100)
			
			call_swap = lambda f=q: self.swap(f)
			call_view = lambda c,f=q: EditFuncs.viewQuestion(self,f,c)
			call_delete = lambda f=q: self.deleteFunc(f)
			self.swap_variable[q] = ctk.CTkCheckBox(self.questions_frame[q], onvalue=True, offvalue=False,text="", command=lambda q=q: call_swap(q))
			self.view_question[q] = ctk.CTkButton(self.questions_frame[q],text=f"View Question {q}",command=lambda q=q: call_view("VQ",q))
			self.add_before[q] = ctk.CTkButton(self.questions_frame[q],text=f"Add Before",command=lambda q=q: call_view("AB", q))
			self.add_after[q] = ctk.CTkButton(self.questions_frame[q],text=f"Add After",command=lambda q=q: call_view("AA",q))
			self.delete[q] = ctk.CTkButton(self.questions_frame[q],text=f"Delete",command=lambda q=q: call_delete(q))

		self.forgetTopics()
		self.displayQuestions(topic_name)

	def questionsPageCancelFunc(self):
		self.forgetQuestions()
		self.displayScrollPage()

	def swap(self,question_number):
		if len(self.swap_numbers) < 2:
			# print(self.swap_variable[question_number].get(),question_number)
			if self.swap_variable[question_number].get():
				self.swap_numbers.append(question_number)

				if len(self.swap_numbers) == 2:
					# print("Two")
					pf = pandas.read_csv(self.file)

					# If there are two values in self.swap_numbers, proceed with the swap
					a, b = self.swap_numbers[0], self.swap_numbers[1]

					# Perform the swap for each column
					pf.loc[a-1, "Time"], pf.loc[b-1, "Time"] = pf.loc[b-1, "Time"], pf.loc[a-1, "Time"]
					pf.loc[a-1, "Marks"], pf.loc[b-1, "Marks"] = pf.loc[b-1, "Marks"], pf.loc[a-1, "Marks"]
					pf.loc[a-1, "Option Type"], pf.loc[b-1, "Option Type"] = pf.loc[b-1, "Option Type"], pf.loc[a-1, "Option Type"]
					pf.loc[a-1, "Text Question"], pf.loc[b-1, "Text Question"] = pf.loc[b-1, "Text Question"], pf.loc[a-1, "Text Question"]
					pf.loc[a-1, "Image Question"], pf.loc[b-1, "Image Question"] = pf.loc[b-1, "Image Question"], pf.loc[a-1, "Image Question"]
					pf.loc[a-1, "Hint"], pf.loc[b-1, "Hint"] = pf.loc[b-1, "Hint"], pf.loc[a-1, "Hint"]
					pf.loc[a-1, "Solution Text"], pf.loc[b-1, "Solution Text"] = pf.loc[b-1, "Solution Text"], pf.loc[a-1, "Solution Text"]
					pf.loc[a-1, "Solution Image"], pf.loc[b-1, "Solution Image"] = pf.loc[b-1, "Solution Image"], pf.loc[a-1, "Solution Image"]
					pf.loc[a-1, "Options"], pf.loc[b-1, "Options"] = pf.loc[b-1, "Options"], pf.loc[a-1, "Options"]
					pf.loc[a-1, "Answer"], pf.loc[b-1, "Answer"] = pf.loc[b-1, "Answer"], pf.loc[a-1, "Answer"]

					pf.to_csv(self.file,index=False)

					# print(f"Swap: {self.swap_numbers}")
					self.swap_variable[self.swap_numbers[0]].deselect(); self.swap_variable[self.swap_numbers[1]].deselect()
					self.swap_numbers.clear()
			else:
				# print(question_number)
				if self.question_number in self.swap_numbers:
					self.swap_numbers.remove(question_number) 

	def deleteFunc(self,question_number):
		you_sure = tk.messagebox.askyesno(title="Exit", message="Are you sure you want to delete this question?", default="no")

		df = pandas.read_csv(f"{self.file}")
		df = df.drop(question_number-1)
		df.to_csv(f"{self.file}", index=False)

		if you_sure:
			self.forgetQuestions()
			self.displayQuestions(self.topic_name)