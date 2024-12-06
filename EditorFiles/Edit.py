import customtkinter as ctk
import tkinter as tk

class Edit:
	def __init__(self, app):
		self.app = app

	def mainWindow(self):
		self.window = ctk.CTkToplevel(self.app)
		self.window.transient(self.app)
		self.window.title("Edit")
		self.window.geometry("750x500+500+150")

		def displayWidgets():
			self.description.pack()
			self.edit_scroll_frame.pack()

		def forgetWidgets():
			self.description.pack_forget()
			self.edit_scroll_frame.pack_forget()

		#Creating an attribute of the functions above
		self.forget_main_window_widgets = forgetWidgets
		self.displayWidgets = displayWidgets

		#Adding a label describing the page
		self.description = ctk.CTkLabel(self.window, text="Please select a topic to make changes to it")

		#Creating a scrollbar for all the topics
		self.edit_scroll_frame = ctk.CTkScrollableFrame(self.window, corner_radius=0, border_width=0, fg_color="#c3c3c3",orientation="vertical", width=750, height=500)

		#Inserting subjects
		for _ in range(10):
			ctk.CTkButton(self.edit_scroll_frame, text="Tom", command=self.optionsWindow).pack(pady=50)

		displayWidgets()

	def optionsWindow(self):
		def displayOptionsWindowWidgets():
			self.guide.pack(pady=30)
			self.editing_options.pack()
			self.options_window_cancel_button.pack(side="left", padx=100)
			self.options_window_next_button.pack(side="right", padx=100)

		def forgetOptionsWindowWidgets():
			self.guide.pack_forget()
			self.editing_options.pack_forget()
			self.options_window_cancel_button.pack_forget()
			self.options_window_next_button.pack_forget()

		def optionsWindowCancelFunction():
			forgetOptionsWindowWidgets()
			self.displayWidgets()

		def optionsWindowNextFunction():
			print(self.editing_options.get())

			#If the user choice to change topic details by selecting "Change Topic Details" in the editing options menu
			if self.editing_options.get() == "Change Topic Details":
				self.changeTopicDetails()
			
			#If the user choice to change question by selecting "Change a Question" in the editing options menu
			elif self.editing_options.get() == "Change a Question":
				self.changeAQuestion()

		#Creating an attribute of the "forgetOptionsWindowWidgets" and "displayOptionsWindowWidgets" functions
		self.forgetOptionsWindowWidgets = forgetOptionsWindowWidgets
		self.displayOptionsWindowWidgets = displayOptionsWindowWidgets

		#Creating some widgets
		self.guide = ctk.CTkLabel(self.window, text="Do you wish to: ")

		#Creating a list of editing chioces
		self.editing_choices = ["Change Topic Details", "Change a Question","Add a New Question","Delete a Question"]

		#Creating an options menu which contain the user's choice of editing, eg, change Topic Details, change Questions, etc
		self.editing_options = ctk.CTkOptionMenu(self.window, values=self.editing_choices)

		#Cancel Button
		self.options_window_cancel_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=optionsWindowCancelFunction)

		#Next Button
		self.options_window_next_button = ctk.CTkButton(self.window, text="Next", border_width=0, command=optionsWindowNextFunction)
		
		#Forgeting the main window's widgets
		self.forget_main_window_widgets()

		displayOptionsWindowWidgets()

	def changeTopicDetails(self):
		def displayTopicDetailsWidgets():
			self.indicator.pack()
			self.topic.pack(pady=100)
			self.randomize.pack()
			self.cancel_change_topic_detail_button.pack(side="left", padx=100)
			self.save_change_topic_detail_button.pack(side="right", padx=100)

		def forgetTopicDetailsWidgets():
			self.indicator.pack_forget()
			self.topic.pack_forget()
			self.randomize.pack_forget()
			self.save_change_topic_detail_button.pack_forget()
			self.cancel_change_topic_detail_button.pack_forget()

		def nameValidator():
			#Validating the topic names input
			if self.topic.get().isidentifier() == False:
				tk.messagebox.showinfo(title="Invalid Topic Name", message="Your topic name doesn't have valid character(A-Z or _)")
				return False
				
			return True

		def cancelTopicDetailsFunction():
			forgetTopicDetailsWidgets()
			self.displayOptionsWindowWidgets()

		def saveTopicDetailsFunction():
			if nameValidator():
				self.window.destroy()

		#Forgeting the main window's widgets
		self.forgetOptionsWindowWidgets()

		#Indicator label
		self.indicator = ctk.CTkLabel(self.window, text=f"Change #topic's name or its the randomize option")

		#Allowing the user to enter the name of their topic
		self.topic_var = tk.StringVar(value="EnterNewTopicName") #This value is for testing
		self.topic = ctk.CTkEntry(self.window, textvariable=self.topic_var, border_width=0, corner_radius=10, width=300, justify="center", placeholder_text="Topic Name", placeholder_text_color="#c3c3c3")

		#Randomize checkbox
		self.randomize = ctk.CTkCheckBox(self.window, text="Change the randomize option", offvalue=0, onvalue=1)

		#Cancel Button
		self.cancel_change_topic_detail_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=cancelTopicDetailsFunction)

		#Save Button
		self.save_change_topic_detail_button = ctk.CTkButton(self.window, text="Save", border_width=0, command=saveTopicDetailsFunction)
		
		displayTopicDetailsWidgets()

	def changeAQuestion(self):
		def displayChangeAQuestionWidgets():
			self.question_number_label.pack()

		def forgetChangeAQuestionWidgets():
			pass

		def cancelChangeAQuestionFunction():
			pass

		def nextChangeAQuestionFunction():
			pass

		#Variable to keep track of the question
        self.question_number = 1

        #Creating title label
        self.question_number_label = ctk.CTkLabel(self.frameB, text=f"Question {self.question_number}'s time setting and marks:")

       	displayChangeAQuestionWidgets()

	def addNewQuestion(self):
		pass

	def deleteQuestion(self):
		pass
