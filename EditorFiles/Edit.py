# proceed
import customtkinter as ctk
import tkinter as tk
from PIL import Image
import time, os, pandas

from EditorFiles import ExFunc

class Edit:
	def __init__(self, app):
		self.app = app

	def optionsWindow(self, topic_name):
		self.topic_name = topic_name
		# print(self.topic_name)

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
			#If the user choice to change topic details by selecting "Change Topic Details" in the editing options menu
			if self.editing_options.get() == "Change Topic Details":
				self.changeTopicDetails()
			
			#If the user choice to change question by selecting "Change a Question" in the editing options menu
			elif self.editing_options.get() == "Change a Question":
				self.changeAQuestion()

			#If the user choice to change question by selecting "Delete a Question" in the editing options menu
			elif self.editing_options.get() == "Delete a Question":
				self.deleteQuestion()

		#Creating an attribute of the "forgetOptionsWindowWidgets" and "displayOptionsWindowWidgets" functions
		self.forgetOptionsWindowWidgets = forgetOptionsWindowWidgets
		self.displayOptionsWindowWidgets = displayOptionsWindowWidgets

		#Creating some widgets
		self.guide = ctk.CTkLabel(self.window, text="Do you wish to: ")

		#Creating a list of editing chioces
		self.editing_choices = ["Change Topic Details", "Change a Question","Delete a Question"]

		#Creating an options menu which contain the user's choice of editing, eg, change Topic Details, change Questions, etc
		self.editing_options = ctk.CTkOptionMenu(self.window, values=self.editing_choices)

		#Cancel Button
		self.options_window_cancel_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=optionsWindowCancelFunction)

		#Next Button
		self.options_window_next_button = ctk.CTkButton(self.window, text="Next", border_width=0, command=optionsWindowNextFunction)
		
		#Forgeting the main window's widgets
		self.forget_main_window_widgets()

		displayOptionsWindowWidgets()

	def mainWindow(self):
		if self.app.window_up == False:
			# Control variable to prevent more than one editor window from opening at the same time
			self.app.window_up = True

			self.window = ctk.CTkToplevel(self.app)
			self.window.transient(self.app)
			self.window.title("Edit")
			self.window.geometry("750x500+500+150")

			def destroyCommand():
				you_sure = tk.messagebox.askyesno(title="Exit", message="Are you sure you want to exit out of this window?", default="no")

				if you_sure:
					self.window.destroy()
					self.app.window_up = False

			def displayWidgets():
				self.description.pack()
				self.edit_scroll_frame.pack()

			def forgetWidgets():
				self.description.pack_forget()
				self.edit_scroll_frame.pack_forget()

			# Implementing the exit command
			self.window.protocol("WM_DELETE_WINDOW", destroyCommand)

			# Creating an attribute of the functions above
			self.forget_main_window_widgets = forgetWidgets
			self.displayWidgets = displayWidgets

			# Adding a label describing the page
			self.description = ctk.CTkLabel(self.window, text="Please select a topic to make changes to it")

			# Creating a scrollbar for all the topics
			self.edit_scroll_frame = ctk.CTkScrollableFrame(self.window, corner_radius=0, border_width=0, fg_color="#c3c3c3",orientation="vertical", width=750, height=500)

			# Inserting the topics
			filenames = os.listdir(r"C:\Users\hp\Documents\Quiz\Storage")

			self.buttons = {} # store buttons so you can access them later

			for file in filenames:
			    if file.endswith(".csv"):
			        file_name = file[:-4]  # remove ".csv"
			        # capture the current file_name in the lambda default
			        call = lambda f=file_name: self.optionsWindow(f)
			        button = ctk.CTkButton(self.edit_scroll_frame, text=file_name, command=call)
			        button.pack(pady=50)
			        self.buttons[file_name] = button

			displayWidgets()

	# This function is to edit the topic's meta data
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
			# Validating the topic names input
			if self.topic.get().isidentifier() == False:
				tk.messagebox.showinfo(title="Invalid Topic Name", message="Your topic name doesn't have valid character(A-Z or _)")
				return False
				
			return True

		def cancelTopicDetailsFunction():
			forgetTopicDetailsWidgets()
			self.displayWidgets()

		def saveTopicDetailsFunction(): 
			cancelTopicDetailsFunction() # Next

			# Updating the topic
			data = pandas.read_csv(fr"C:\Users\hp\Documents\Quiz\Storage\{self.topic_name}.csv")
			data = data.replace(True, self.randomize.get())

			# Deleting the previous topic
			os.remove(f"Storage\\{self.topic_name}.csv")

			# Updating the existing buttons
			# self.buttons.pop(self.topic_name)
			
			# Storing the changes on the file
			data.to_csv(f"Storage\\{self.topic_var.get()}.csv")

			# Redisplaying the button properly and updated this time
			# Getting rid of the previous buttons and outdated buttons
			for button in self.buttons:
				self.buttons[button].pack_forget()

			# Getting the new list of topics
			filenames = os.listdir(r"C:\Users\hp\Documents\Quiz\Storage")

			self.buttons = {}  # store buttons so you can access them later

			# Displaying the new buttons
			for file in filenames:
			    if file.endswith(".csv"):
			        file_name = file[:-4]  # remove ".csv"
			        # capture the current file_name in the lambda default
			        call = lambda f=file_name: self.optionsWindow(f)
			        button = ctk.CTkButton(self.edit_scroll_frame, text=file_name, command=call)
			        button.pack(pady=50)
			        self.buttons[file_name] = button

			self.displayWidgets()
			# print(data, type(data), self.topic_name, "\n", data.to_dict())
			# print(self.buttons)

		# Forgeting the main window's widgets
		self.forgetOptionsWindowWidgets()

		# Indicator label
		self.indicator = ctk.CTkLabel(self.window, text=f"Change {self.topic_name}'s topic name or its the randomize option")

		# Allowing the user to enter the name of their topic
		self.topic_var = tk.StringVar(value=self.topic_name) #This value is for testing
		self.topic = ctk.CTkEntry(self.window, textvariable=self.topic_var, border_width=0, corner_radius=10, width=300, justify="center", placeholder_text="Topic Name", placeholder_text_color="#c3c3c3")

		# Randomize checkbox
		self.randomize = ctk.CTkCheckBox(self.window, text="Change the randomize option", offvalue=False, onvalue=True)

		# Cancel Button
		self.cancel_change_topic_detail_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=cancelTopicDetailsFunction)

		# Save Button
		self.save_change_topic_detail_button = ctk.CTkButton(self.window, text="Save", border_width=0, command=saveTopicDetailsFunction)
		
		displayTopicDetailsWidgets()

	# To edit the actual questions
	def changeAQuestion(self): # proceed
		def displayScrollWidgets():
			# Guide on what to do
			self.question_guide.pack()
			self.scroll_frame.pack()
			self.scroll_cancel_button.pack(side="left", padx=110, pady=20)
			self.scroll_continue_button.pack(side="right", padx=110, pady=20)

		def forgetScrollWidget():
			self.question_guide.pack_forget()
			self.scroll_frame.pack_forget()
			self.scroll_cancel_button.pack_forget()
			self.scroll_continue_button.pack_forget()

		def scrollCancelFunction():
			forgetScrollWidget()
			self.displayOptionsWindowWidgets()

		def scrollContinueFunction():
			forgetScrollWidget()
			displayChangeAQuestionWidgets()

		def displayChangeAQuestionWidgets():
			self.question_number_label.pack()
			self.frameA.pack(pady=30)
			self.add_delete_frame.pack()
			self.add_button.pack(side="left", padx=30)
			self.delete_button.pack(side="right", padx=30)
			self.time.pack(padx=10, side="left")
			self.marks.pack(padx=10, side="left")
			self.answer_format_menu.pack(pady=20, padx=20)
			self.continue_details_page_button.pack(side="right", padx=20, pady=20, expand=True)
			self.cancel_details_page_button.pack(side="left", padx=20, pady=20, expand=True)

		def actualQuestionFormatFunction(event):
			ExFunc.forgetActualQuestionPageWidgets(self)
			ExFunc.displayActualQuestionPageWidgets(self, True)
			
		def forgetChangeAQuestionWidgets():
			self.question_number_label.pack_forget()
			self.frameA.pack_forget()
			self.add_delete_frame.pack_forget()
			self.answer_format_menu.pack_forget()
			self.cancel_details_page_button.pack_forget()
			self.continue_details_page_button.pack_forget()

		def questionsCommand(question, question_checkbox, all_checkbox):
			forgetScrollWidget()

			# Implementing functionalities
			self.edit_question_number = question

			displayChangeAQuestionWidgets()

			# Updating the widgets data
			data = pandas.read_csv(fr"C:\Users\hp\Documents\Quiz\Storage\{self.topic_name}.csv")
			
			for column, items in data.items():
				if column == "Time":
					self.time_var.set(value=items[question-1])
				elif column == "Marks":
					self.marks_var.set(value=items[question-1])
			
			self.question_number_label.configure(text=f"Question {self.edit_question_number}'s time setting and marks:")

		def hintFunction():
			ExFunc.createHintWidgets(self)

		def solutionFunction():
			#Displaying the window and its features
			self.solution_and_feedback_window = ctk.CTkToplevel(self.window)
			self.solution_and_feedback_window.transient(self.window)
			self.solution_and_feedback_window.title("Solutions and Feedback")
			self.solution_and_feedback_window.geometry("700x500+300+50")

			#Adding wigets to the window
			self.solution_frame = ctk.CTkFrame(self.solution_and_feedback_window, border_width=0, bg_color="#c3c3c3")
			self.solution_title = ctk.CTkLabel(self.solution_frame, text="Please add a solution/feedback")
			self.solution_question_formats = ["Text", "Image","Video"]
			self.solution_format_var = tk.StringVar(value=self.solution_question_formats[0])
			self.solution_format_menu = ctk.CTkOptionMenu(self.solution_frame, values=self.solution_question_formats, variable=self.solution_format_var, command=solutionFormatFunction)

			#Textbox widget for text only
			self.solution_textbox = ctk.CTkTextbox(self.solution_and_feedback_window, width=500, height=300, border_width=0, text_color="#c8b800", wrap="word")
			self.solution_textbox.insert("0.0", self.solution_and_feedback) #Inserting the solution to the textbox

			#Add image widget for images only
			self.solution_question_image = ctk.CTkImage(light_image=Image.open(self.solution_image_filename), size=(400,200))
			self.solution_question_image_label = ctk.CTkLabel(self.solution_and_feedback_window, image=self.solution_question_image, text="", width=400, height=200)
			self.solution_question_image_label.bind("<Button-1>", lambda event: ExFunc.solutionQuestionImageFunction(self))

			self.solution_ok_button = ctk.CTkButton(self.solution_and_feedback_window, text="Ok", border_width=0, command=lambda: ExFunc.solutionOkFunction(self))
			self.solution_restart_button = ctk.CTkButton(self.solution_and_feedback_window, text="Restart Solution", border_width=0, command=lambda: ExFunc.restartSolution(self))
			self.solution_cancel_button = ctk.CTkButton(self.solution_and_feedback_window, text="Cancel",border_width=0, command=lambda: ExFunc.solutionCancelFunction(self))

			ExFunc.displaySolutionWidgets(self)

		def solutionFormatFunction(event):
			ExFunc.forgetSolutionWidgets(self)
			ExFunc.displaySolutionWidgets(self)

		def addNewQuestionFunction():
			#Editing the question number label to give more info
			# Note: At this point, people might get a bit confused with the UI design because of the way it moved from an editing question to a new question
			self.question_number_label.configure(text=f"This is now the new question {self.question_number+1}.")

			forgetChangeAQuestionWidgets() # Forgetting the Options Page

			def displayAddQuestion():
				displayChangeAQuestionWidgets()

				#Removing the widgets that aren't necessary
				self.add_button.pack_forget()
				self.delete_button.pack_forget()

				# Changing the "cancel_details_page_button" button function
				self.cancel_details_page_button.configure(command=addNewQuestionCancelFunction)

				# Preventing the "continue_actual_question_page_button" from appearing on the next page
				self.continue_present = False

				# Changing the solution and hint variables for only adding new questions purposes

			# Maybe add a timer here to reduce the confusion at this point
			self.app.after(100, displayAddQuestion)

			# Configuring the done button just for the add new question page
			self.done_button.configure(command=addNewQuestionDoneFunction) # print

		def addNewQuestionCancelFunction():
			# Bringing back the continue button on the actual page
			self.continue_present = True

			forgetChangeAQuestionWidgets()

			# Changing the question label to the usual text
			self.question_number_label.configure(text=f"Question {self.question_number}'s time setting and marks:")

			# Changing the cancel button command to its original command
			self.cancel_details_page_button.configure(command=cancelChangeAQuestionFunction)

			# Bringing back the previous widgets "Change a question widgets"
			displayChangeAQuestionWidgets()

		def addNewQuestionDoneFunction():
			ExFunc.forgetActualQuestionPageWidgets(self)

			# Configuring the variables back to their original state
			self.continue_present = True
			self.question_number_label.configure(text=f"Question {self.question_number}'s time setting and marks:")
			self.done_button.configure(command=actualQuestionDoneFunction)

			# Changing the solutions widgets to its default
			self.solution_image_filename = "Pictures/AddImage.jpg"

			displayChangeAQuestionWidgets()

		def infoFunction():
			# This function is implemented to the info button
			window = ctk.CTkTopLevel()

			# This text contains all the help information needed for the user
			text = ""

		def deleteQuestionFunction():
			you_sure = tk.messagebox.askyesno(title="Delete",message="Are you sure you want to delete this question?")

			if you_sure:
				if self.question_number > 1:
					self.question_number-=1
					self.question_number_label.configure(text=f"Question {self.question_number}'s time setting and marks:")
					
					forgetChangeAQuestionWidgets()
					displayChangeAQuestionWidgets()

		def cancelChangeAQuestionFunction():
			forgetChangeAQuestionWidgets()

			if self.question_number > 1:
				# Change the question nummber minus 1
				self.question_number-=1

				# Updating the question number label
				self.question_number_label.configure(text=f"Question {self.question_number}'s time setting and marks:")
				
				ExFunc.displayActualQuestionPageWidgets(self, True)	
			else: displayScrollWidgets()

		def continueChangeAQuestionFunction():	
			if ExFunc.Validator(None, self.time, self.marks) != False: #If the validation does meet its needs then it allows the actual question widgets to be displayed,else not displayed
				forgetChangeAQuestionWidgets()
				ExFunc.displayActualQuestionPageWidgets(self, self.continue_present) # print

		def actualQuestionCancelFunction():
			ExFunc.forgetActualQuestionPageWidgets(self)
			displayChangeAQuestionWidgets()

			if self.continue_present == False:
				self.add_delete_frame.pack_forget()

		def actualQuestionContinueFunction():
			# Don't forget to implement Validations
			if ExFunc.actualQuestionValidation(self.option_A_entry, self.option_B_entry, self.option_C_entry, self.option_D_entry, self.option_A_button, self.option_B_button, self.option_C_button, self.option_D_button, self.options_variable, self.answer_format_menu_variable, self.without_options_textbox, self.question, self.image_filename):
				ExFunc.forgetActualQuestionPageWidgets(self)

				# Update the question number by adding one to it
				self.question_number+=1

				# Updating the question number label
				self.question_number_label.configure(text=f"Question {self.question_number}'s time setting and marks:")

				displayChangeAQuestionWidgets()

		def actualQuestionDoneFunction():
			if ExFunc.actualQuestionValidation(self.option_A_entry, self.option_B_entry, self.option_C_entry, self.option_D_entry, self.option_A_button, self.option_B_button, self.option_C_button, self.option_D_button, self.options_variable, self.answer_format_menu_variable, self.without_options_textbox, self.question, self.image_filename):
				you_sure = tk.messagebox.askyesno(title="Save", message="Are you sure you want to save this topic?")

				if you_sure:
					ExFunc.forgetActualQuestionPageWidgets(self)
					displayScrollWidgets()
		
		# Getting the stored data
		data = pandas.read_csv(f"Storage\\{self.topic_name}.csv")

		# Wigets here is for the scroll frame only Validator

		# Guide on what to do
		self.question_guide = ctk.CTkLabel(self.window, text="Please click on a question to change")

		# Scroll Frame
		self.scroll_frame = ctk.CTkScrollableFrame(self.window, corner_radius=0, border_width=0, fg_color="#c3c3c3",orientation="vertical", width=750, height=500)

		#Adding questions

		self.question_checkboxes = {}  # store buttons so you can access them later

		# Displaying the new radio buttons
		for questions in data["Question No"]:
			question = int(questions)
			# capture the current file_name in the lambda default
			call = lambda f=question: questionsCommand(question, question_checkbox.cget("text"), self.question_checkboxes)
			question_checkbox = ctk.CTkRadioButton(self.scroll_frame, text=str(question), command=call)
			question_checkbox.cget("text")
			question_checkbox.pack(pady=50)
			self.question_checkboxes[question] = question_checkbox

		# for _  in range(5):
		# 	variable = tk.IntVar(value=1)
		# 	ctk.CTkRadioButton(self.scroll_frame, text=f"Question {_+1}", variable=variable, value=_+1, command=questionsCommand).pack(pady=50,expand=False)

		#Scroll cancel button
		self.scroll_cancel_button = ctk.CTkButton(self.scroll_frame, text="Cancel", border_width=0, command=scrollCancelFunction)
		
		#Scroll continue button
		self.scroll_continue_button = ctk.CTkButton(self.scroll_frame, text="Continue", border_width=0, command=scrollContinueFunction)

		#Wigets from here is for the question individually

		#Variable to keep track of the question
		self.question_number = 1

		#Creating title label
		self.question_number_label = ctk.CTkLabel(self.window, text=f"Question {self.question_number}'s time setting and marks:")

		#Contains the add and delete buttons
		self.add_delete_frame = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

		self.add_button = ctk.CTkButton(self.add_delete_frame, text="Add a New Question", border_width=0, command=addNewQuestionFunction)

		self.delete_button = ctk.CTkButton(self.add_delete_frame, text="Delete this Question", border_width=0, command=deleteQuestionFunction)

        # Info button: Contains the help information about what the "add question page" does
		self.info = ctk.CTkButton(self.window, text="", border_width=0, command=infoFunction)

		#Contains the time and marks entry widgets
		self.frameA = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

		self.time_var = tk.StringVar(value="00:00:10")
		self.time = ctk.CTkEntry(self.frameA, textvariable=self.time_var, border_width=0, corner_radius=10, width=200, justify="center",placeholder_text_color="#c3c3c3", placeholder_text="00:00:00")

		#Allowing the user to enter the total marks for their an individual question
		self.marks_var = tk.IntVar(value=1)
		self.marks = ctk.CTkEntry(self.frameA, textvariable=self.marks_var, border_width=0, corner_radius=10, width=200, justify="center", placeholder_text="0", placeholder_text_color="#c3c3c3")

		#Option Menu
		self.answer_format = ["Options","Without Options"]
		self.answer_format_menu_variable = tk.StringVar(value=self.answer_format[0])
		self.answer_format_menu = ctk.CTkOptionMenu(self.window, values=self.answer_format, variable=self.answer_format_menu_variable)

		#Cancel Button
		self.cancel_details_page_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=cancelChangeAQuestionFunction)

		# Continue Present
		self.continue_present = True
		
		#Continue Button
		self.continue_details_page_button = ctk.CTkButton(self.window, text="Continue", border_width=0, command=continueChangeAQuestionFunction)

		#This frame is used as a container for the "format menu" and the "hint button"
		self.frame1 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

		#Question Format Menu
		self.question_formats = ["Text","Image","Video"]
		self.format_var = tk.StringVar(value=self.question_formats[0])
		self.format_menu = ctk.CTkOptionMenu(self.frame1, values=self.question_formats, variable=self.format_var, command=actualQuestionFormatFunction)
		
		self.hint = "" # Making an attribute to store the hint

		self.solution_and_feedback = "" #Making an attribute to store the solution and feedback 
		self.solution_image_filename = "Pictures/AddImage.jpg" #Making an attribute to store the solution image 
		
		# Solution button: When clicked, it allows the user to add the solution and feedback to that question
		self.solution_and_feedback_button = ctk.CTkButton(self.frame1, text="Add Solutions", command=solutionFunction)

		# Hint image for the button
		self.hint_img = ctk.CTkImage(light_image=Image.open("Pictures/Hint.png"), size=(30,30))

		#Hint button: When clicked, it allows the user to add or changes an assigned hint 
		self.hint_button = ctk.CTkButton(self.frame1, text="Add Hint", command=hintFunction)

		#Question textbox: This is where the user inserts their question
		self.question = ctk.CTkTextbox(self.window, width=600, text_color="#098bed", wrap="word")

		#The is a guide in the "question" textbox at the beginning of every making a new topic
		if self.question_number == 1:
		    self.question.insert("0.0", "Please add your question")
		self.question.focus_set()

		#Question Image: This label stores the question(in image form) inserted by the user
		self.image_filename = "Pictures/AddImage.jpg"
		self.question_image = ctk.CTkImage(light_image=Image.open(self.image_filename), size=(400,200))
		self.question_image_label = ctk.CTkLabel(self.window, image=self.question_image, text="", width=400, height=200)
		self.question_image_label.bind("<Button-1>", lambda event: ExFunc.questionImageFunction(self))

		#Option frames
		self.option_frame1 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3",height=50)

		self.option_frame2 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3",height=50)

		#Options variable
		self.options_variable = tk.StringVar()

		#Options button(radio button) and their entries
		self.option_A_button = ctk.CTkRadioButton(self.option_frame1,variable=self.options_variable, value="A", text="", command=lambda: ExFunc.selectedOption(self.option_A_entry, self.option_B_entry, self.option_C_entry, self.option_D_entry, self.options_variable))

		self.option_A_entry = ctk.CTkEntry(self.option_frame1, border_width=2, width=275, placeholder_text="Option A", placeholder_text_color="#b3b3b3")

		self.option_B_button = ctk.CTkRadioButton(self.option_frame1,variable=self.options_variable, value="B", text="", command=lambda: ExFunc.selectedOption(self.option_A_entry, self.option_B_entry, self.option_C_entry, self.option_D_entry, self.options_variable))

		self.option_B_entry = ctk.CTkEntry(self.option_frame1, border_width=2, width=275, placeholder_text="Option B", placeholder_text_color="#b3b3b3")

		self.option_C_button = ctk.CTkRadioButton(self.option_frame2,variable=self.options_variable, value="C", text="", command=lambda: ExFunc.selectedOption(self.option_A_entry, self.option_B_entry, self.option_C_entry, self.option_D_entry, self.options_variable))

		self.option_C_entry = ctk.CTkEntry(self.option_frame2, border_width=2, width=275, placeholder_text="Option C", placeholder_text_color="#b3b3b3")

		self.option_D_button = ctk.CTkRadioButton(self.option_frame2,variable=self.options_variable, value="D", text="", command=lambda: ExFunc.selectedOption(self.option_A_entry, self.option_B_entry, self.option_C_entry, self.option_D_entry, self.options_variable))

		self.option_D_entry = ctk.CTkEntry(self.option_frame2, border_width=2, width=275, placeholder_text="Option D", placeholder_text_color="#b3b3b3")

		#Without Options Textbox
		self.without_options_textbox = ctk.CTkTextbox(self.window, width=600, height=50, text_color="#00FF00")

		#Guide in the "without options textbox" for every beginning of every topic
		if self.question_number == 1:
		    self.without_options_textbox.insert("0.0", "Please add your answer")

		# Continue Button
		self.continue_actual_question_page_button = ctk.CTkButton(self.window, text="Continue", border_width=0, command=actualQuestionContinueFunction)
		
		#Cancel Button
		self.cancel_actual_question_page_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=actualQuestionCancelFunction)

		#Done Button
		self.done_button = ctk.CTkButton(self.window, text="Done", border_width=0, command=actualQuestionDoneFunction)
		
		self.forgetOptionsWindowWidgets()
		displayScrollWidgets()

	def deleteQuestion(self):
		# Removing the previous widgets that was on the page
		self.forgetOptionsWindowWidgets()

		def forgetDeleteWidgets():
			self.delete_scroll_frame.pack_forget()
			self.scroll_delete_cancel_button.pack_forget()
			self.scroll_delete_button.pack_forget()

		def deleteCommand():
			pass

		def deleteCancelFunction():
			forgetDeleteWidgets()
			self.optionsWindow()

		def deleteFunction():
			you_sure = tk.messagebox.askyesnocancel(title="Delete",message="Do you actually want to delete this questions?")

			if you_sure:
				forgetDeleteWidgets()
				self.optionsWindow()

		# Scroll Frame
		self.delete_scroll_frame = ctk.CTkScrollableFrame(self.window, corner_radius=0, border_width=0, fg_color="#c3c3c3",orientation="vertical", width=750, height=500)
		self.delete_scroll_frame.pack(expand=True, fill="both")

		#Adding questions
		for _  in range(5): 
			variable = tk.IntVar(value=0)
			ctk.CTkCheckBox(self.delete_scroll_frame, text=f"Question {_+1}", variable=variable, onvalue=1, offvalue=0, command=deleteCommand).pack(pady=50,expand=False)

		#Scroll cancel button
		self.scroll_delete_cancel_button = ctk.CTkButton(self.delete_scroll_frame, text="Cancel", border_width=0, command=deleteCancelFunction)
		self.scroll_delete_cancel_button.pack(side="left", padx=100)
		
		#Scroll continue button
		self.scroll_delete_button = ctk.CTkButton(self.delete_scroll_frame, text="Delete", border_width=0, command=deleteFunction)
		self.scroll_delete_button.pack(side="right", padx=100)