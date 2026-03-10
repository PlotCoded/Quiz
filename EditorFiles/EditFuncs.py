import customtkinter as ctk
import pandas
import tkinter as tk
from PIL import Image
from EditorFiles import AddFuncs,ExFunc
from ast import literal_eval

def initialiseFirstPage(self):
	#Variable to keep track of the question
    self.question_number = 1

    #Contains the option menu and randomize checkbox
    self.frameA = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

    #Allowing the user to enter the name of their topic
    self.topic_var = tk.StringVar(value="TopicName") #This value is for testing
    self.topic = ctk.CTkEntry(self.frameA, textvariable=self.topic_var, border_width=0, corner_radius=10, width=200, justify="center", placeholder_text="Topic Name", placeholder_text_color="#c3c3c3")

    #Randomize checkbox
    self.randomize = ctk.CTkCheckBox(self.frameA, text="Randomize", offvalue=False, onvalue=True,command=None)

    #Details frame: Contains the question number, subject name, subject time an subject 
    self.frameB = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

    #Creating title label
    self.question_number_label = ctk.CTkLabel(self.frameB, text=f"Question {self.question_number}'s time setting and marks:")

    #Allowing the user to enter the time boundry for their an individual question
    self.time_var = tk.StringVar(value="00:00:11")
    self.time = ctk.CTkEntry(self.frameB, textvariable=self.time_var, border_width=0, corner_radius=10, width=200, justify="center",placeholder_text_color="#c3c3c3", placeholder_text="00:00:00")

    #Allowing the user to enter the total marks for their an individual question
    self.marks_var = tk.StringVar(value="1")
    self.marks = ctk.CTkEntry(self.frameB, textvariable=self.marks_var, border_width=0, corner_radius=10, width=200, justify="center", placeholder_text="0", placeholder_text_color="#c3c3c3")

    #Option Menu
    self.answer_format = ["Options","Without Options"]
    self.answer_format_menu_variable = tk.StringVar(value=self.answer_format[0])
    self.answer_format_menu = ctk.CTkOptionMenu(self.window, values=self.answer_format, variable=self.answer_format_menu_variable)

    #Continue Button
    self.continue_details_page_button = ctk.CTkButton(self.window, text="Continue", border_width=0, command=lambda: None)

    #Cancel Button
    self.cancel_details_page_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=lambda: None)

   	#Exit Button
    self.exit_button = ctk.CTkButton(self.window, text="Exit", border_width=0, command=lambda: exitFirstPageFunction(self))

def initialiseSecondPage(self):
	self.hint = "" #Making an attribute to store the 

	self.solution_and_feedback = "" #Making an attribute to store the solution and feedback 
	self.solution_image_filename = "Pictures/AddImage.jpg" #Making an attribute to store the solution image 

	#This frame is used as a container for the "format menu" and the "hint button"
	self.frame1 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

	#Question Format Menu
	self.question_formats = ["Text","Image","Video"]
	self.format_var = tk.StringVar(value=self.question_formats[0])
	self.format_menu = ctk.CTkOptionMenu(self.frame1, values=self.question_formats, variable=self.format_var, command=lambda event: None)

	#Hint button: When clicked, it allows the user to add or changes an assigned hint 
	self.hint_button = ctk.CTkButton(self.frame1, text="Add Hint", command=lambda: ExFunc.createHintWidgets(self))

	#Solution button: When clicked, it allows the user to add the solution and feedback to that question
	self.solution_and_feedback_button = ctk.CTkButton(self.frame1, text="Add Solutions", command=lambda: None)

	#Question textbox: This is where the user inserts their question
	self.question = ctk.CTkTextbox(self.window, width=600, text_color="#098bed", wrap="word")

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

	#Continue Button
	self.continue_actual_question_page_button = ctk.CTkButton(self.window, text="Continue", border_width=0, command=lambda: secondPageContinueFunction(self))

	#Cancel Button
	self.cancel_actual_question_page_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=lambda: None)

	#Done Button
	self.done_button = ctk.CTkButton(self.window, text="Done", border_width=0, command=lambda: None)

def initialiseAllWidgets(self):
	self.topics_scroll_frame = ctk.CTkScrollableFrame(self.window, corner_radius=0, border_width=0, fg_color="#c939c3",orientation="vertical", width=750, height=500)

	self.questions_scroll_frame = ctk.CTkScrollableFrame(self.window, corner_radius=0, border_width=0, fg_color="#c3c3c3", orientation="vertical", width=750, height=500)
		
	self.questions_frame = {}
	self.swap_variable = {}
	self.view_question = {}
	self.add_before = {}
	self.add_after = {}
	self.delete = {}

	self.questions_page_cancel_button = ctk.CTkButton(self.questions_scroll_frame,text=f"Cancel",command=lambda: self.questionsPageCancelFunc())

	initialiseFirstPage(self); initialiseSecondPage(self)

def continueFirstPageFunction(self):
    if ExFunc.firstPageValidator(self) != False:
        AddFuncs.forgetFirstPageWidgets(self)

        # Opening the next page
        ExFunc.displayActualQuestionPageWidgets(self,True)

        self.continue_actual_question_page_button.pack_forget()

def cancelFirstPageFunction(self):
    AddFuncs.forgetFirstPageWidgets(self)

    # Opening the topic page
    self.displayQuestions(self.topic_name)

def cancelSecondPageFunc(self):
	AddFuncs.secondPageCancelFunction(self)

	ExFunc.displayFirstPage(self)

def doneFunc(self,command,question_number):
	print(command)
	match command:
		case "VQ":
			pf = pandas.read_csv(self.file)

			# If there are two values in self.swap_numbers, proceed with the swap
			a = question_number
			try:
				pf.loc[a-1, "Time"] = self.time_var.get()
				pf.loc[a-1, "Marks"] = self.marks_var.get()
				pf.loc[a-1,"Randomize"] = self.randomize.get()
				pf.loc[a-1, "Option Type"] = self.answer_format_menu_variable.get()
				pf.loc[a-1, "Text Question"] = self.question.get("0.0","end")
				pf.loc[a-1, "Image Question"] = self.image_filename
				pf.loc[a-1, "Hint"] = self.hint
				pf.loc[a-1, "Solution Text"] = self.solution_and_feedback
				pf.loc[a-1, "Solution Image"] = self.solution_image_filename
				options = (self.option_A_entry.get(),self.option_B_entry.get(),self.option_C_entry.get(),self.option_D_entry.get())
				pf.loc[a-1, "Options"] = options

				if pf.loc[a-1, "Option Type"] == "Options":
					pf.loc[a-1, "Answer"] = (options[ExFunc.getAnswerChoosenIndex(self,self.options_variable.get())])
				else:
					pf.loc[a-1, "Answer"] = (self.without_options_textbox.get("0.0","end"))
			except:
				pf.to_csv(self.file,index=False)

		case "AB":
			self.record = {}
			pf = pandas.read_csv(self.file)
			options = (self.option_A_entry.get(),self.option_B_entry.get(),self.option_C_entry.get(),self.option_D_entry.get())

			self.record["Time"] = []
			self.record["Marks"] = []
			self.record["Randomize"] = []
			self.record["Option Type"] = []
			self.record["Text Question"] = []
			self.record["Image Question"] = []
			self.record["Hint"] = []
			self.record["Solution Text"] = []
			self.record["Solution Image"] = []
			self.record["Options"] = []
			self.record["Answer"] = []

			self.record["Time"].append(self.time_var.get())
			self.record["Marks"].append(self.marks_var.get())
			self.record["Randomize"].append(self.randomize.get())
			self.record["Option Type"].append(self.answer_format_menu_variable.get())
			self.record["Text Question"].append(self.question.get("0.0","end"))
			self.record["Image Question"].append(self.image_filename)
			self.record["Hint"].append(self.hint)
			self.record["Solution Text"].append(self.solution_and_feedback)
			self.record["Solution Image"].append(self.solution_image_filename)
			self.record["Options"].append(options)

			if self.answer_format_menu_variable.get() == "Options":
				self.record["Answer"].append(options[ExFunc.getAnswerChoosenIndex(self,self.options_variable.get())]) 
			else:
				self.record["Answer"].append(self.without_options_textbox.get("0.0","end"))

			temp_pf = pandas.DataFrame(self.record)

			pf = pandas.concat([pf.iloc[:question_number-1], temp_pf, pf.iloc[question_number-1:]], ignore_index=True)
			pf.to_csv(self.file,index=False)

		case "AA":
			self.record = {}
			pf = pandas.read_csv(self.file)
			options = (self.option_A_entry.get(),self.option_B_entry.get(),self.option_C_entry.get(),self.option_D_entry.get())

			self.record["Time"] = []
			self.record["Marks"] = []
			self.record["Randomize"] = []
			self.record["Option Type"] = []
			self.record["Text Question"] = []
			self.record["Image Question"] = []
			self.record["Hint"] = []
			self.record["Solution Text"] = []
			self.record["Solution Image"] = []
			self.record["Options"] = []
			self.record["Answer"] = []

			self.record["Time"].append(self.time_var.get())
			self.record["Marks"].append(self.marks_var.get())
			self.record["Randomize"].append(self.randomize.get())
			self.record["Option Type"].append(self.answer_format_menu_variable.get())
			self.record["Text Question"].append(self.question.get("0.0","end"))
			self.record["Image Question"].append(self.image_filename)
			self.record["Hint"].append(self.hint)
			self.record["Solution Text"].append(self.solution_and_feedback)
			self.record["Solution Image"].append(self.solution_image_filename)
			self.record["Options"].append(options)

			if self.answer_format_menu_variable.get() == "Options":
				self.record["Answer"].append(options[ExFunc.getAnswerChoosenIndex(self,self.options_variable.get())]) 
			else:
				self.record["Answer"].append(self.without_options_textbox.get("0.0","end"))

			temp_pf = pandas.DataFrame(self.record)

			pf = pandas.concat([pf.iloc[:question_number+1], temp_pf, pf.iloc[question_number+1:]], ignore_index=True)
			pf.to_csv(self.file,index=False)

	ExFunc.forgetActualQuestionPageWidgets(self)
	self.displayQuestions(self.topic_name)

def viewQuestion(self,question_number,command):
	print(command)
	self.forgetQuestions()
	self.question_number = 2

	ExFunc.displayFirstPage(self)
	self.exit_button.pack_forget()

	self.topic.configure(state="normal")
	self.randomize.configure(state="normal")

	# Setting their previous values
	pf = pandas.read_csv(self.file)
	a = question_number

	if command == "VQ":
		self.topic_var.set(value=self.topic_name)
		self.marks_var.set(value=pf.loc[a-1, "Marks"])
		self.time_var.set(pf.loc[a-1,"Time"])
		# self.randomize.set(pf.loc[a-1,"Randomize"])
		self.answer_format_menu_variable.set(value=pf.loc[a-1,"Option Type"])
		self.question.delete("0.0","end")
		self.question.insert("0.0",pf.loc[a-1,"Text Question"])
		self.image_filename = pf.loc[a-1,"Image Question"]
		self.hint = pf.loc[a-1, "Hint"]
		self.solution_and_feedback = pf.loc[a-1, "Solution Text"]
		self.solution_image_filename = pf.loc[a-1, "Solution Image"]

		options = literal_eval(pf.loc[a-1, "Options"])
		self.option_A_entry.delete(0,"end"); self.option_B_entry.delete(0,"end"); self.option_C_entry.delete(0,"end"); self.option_D_entry.delete(0,"end")
		self.option_A_entry.insert(0,str(options[0])); self.option_B_entry.insert(0,f"{options[1]}"); self.option_C_entry.insert(0,f"{options[2]}"); self.option_D_entry.insert(0,f"{options[3]}")

		pf.loc[a-1, "Options"] = str(options)

		if pf.loc[a-1, "Option Type"] == "Options":
		    index = options.index(str(pf.loc[a-1, "Answer"]))
		    ExFunc.setAnswerChoosenIndex(self,index)
		else:
			self.without_options_textbox.delete("0.0","end")
			self.without_options_textbox.insert("0.0",f"{pf.loc[a-1, "Answer"]}")
	else:
		self.option_A_entry.delete(0,"end"); self.option_B_entry.delete(0,"end"); self.option_C_entry.delete(0,"end"); self.option_D_entry.delete(0,"end")
		self.question.delete("0.0","end")
		self.without_options_textbox.delete("0.0","end")

	#--------------------------------------------------------------------------------------------------
	match command:
		case "VQ":
			self.question_number_label.configure(text = f"Question {question_number}'s time setting and marks:")
		case "AB":
			if question_number > 1:
				self.question_number_label.configure(text = f"Question {question_number-1}'s time setting and marks:")
			else:
				self.question_number_label.configure(text = f"Question {question_number}'s time setting and marks:")
		case "AA":
			self.question_number_label.configure(text = f"Question {question_number+1}'s time setting and marks:")


	self.continue_details_page_button.configure(command=lambda: continueFirstPageFunction(self))
	self.cancel_details_page_button.configure(command=lambda: cancelFirstPageFunction(self))

	self.format_menu.configure(command=lambda event: AddFuncs.secondPageQuestionFormat(self))
	self.solution_and_feedback_button.configure(command=lambda: AddFuncs.solutionFunction(self))
	self.cancel_actual_question_page_button.configure(command=lambda: cancelSecondPageFunc(self))
	self.done_button.configure(command=lambda: doneFunc(self,command,question_number))