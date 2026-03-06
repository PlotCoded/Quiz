import customtkinter as ctk
import tkinter as tk
from PIL import Image
import pandas

from EditorFiles import ExFunc
from EditorFiles.AddFuncs import *

class Add:
    def __init__(self, app):
        self.app = app
        self.record = {}

        self.record["Time"] = []
        self.record["Marks"] = []
        self.record["Randomize"] = []
        self.record["Option Type"] = []
        self.record["Text Question"] = []
        self.record["Image Question"] = []
        # self.record["Question No"] = []
        self.record["Hint"] = []
        self.record["Solution Text"] = []
        self.record["Solution Image"] = []
        self.record["Options"] = []
        self.record["Answer"] = []

    def firstPage(self):
        if self.app.window_up == False:
            # Control variable to prevent more than one editor window from opening at the same time
            self.app.window_up = True

            self.window = ctk.CTkToplevel(self.app)
            self.window.transient(self.app)
            self.window.title("Add")
            self.window.geometry("800x550+300+50")

            # Implementing the exit command
            self.window.protocol("WM_DELETE_WINDOW", lambda: destroyCommand(self))

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
            self.continue_details_page_button = ctk.CTkButton(self.window, text="Continue", border_width=0, command=lambda: continueFirstPageFunction(self))

            #Cancel Button
            self.cancel_details_page_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=lambda: cancelFirstPageFunction(self))

            #Exit Button
            self.exit_button = ctk.CTkButton(self.window, text="Exit", border_width=0, command=lambda: exitFirstPageFunction(self))

            # Excecuting functionality
            ExFunc.displayFirstPage(self)

    def secondPage(self):
        self.hint = "" #Making an attribute to store the 

        self.solution_and_feedback = "" #Making an attribute to store the solution and feedback 
        self.solution_image_filename = "Pictures/AddImage.jpg" #Making an attribute to store the solution image 

        #This frame is used as a container for the "format menu" and the "hint button"
        self.frame1 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

        #Question Format Menu
        self.question_formats = ["Text","Image","Video"]
        self.format_var = tk.StringVar(value=self.question_formats[0])
        self.format_menu = ctk.CTkOptionMenu(self.frame1, values=self.question_formats, variable=self.format_var, command=lambda event: secondPageQuestionFormat(self))

        #Hint button: When clicked, it allows the user to add or changes an assigned hint 
        self.hint_button = ctk.CTkButton(self.frame1, text="Add Hint", command=lambda: ExFunc.createHintWidgets(self))

        #Solution button: When clicked, it allows the user to add the solution and feedback to that question
        self.solution_and_feedback_button = ctk.CTkButton(self.frame1, text="Add Solutions", command=lambda: solutionFunction(self))

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
        self.cancel_actual_question_page_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=lambda: secondPageCancelFunction(self))

        #Done Button
        self.done_button = ctk.CTkButton(self.window, text="Done", border_width=0, command=lambda: doneFunction(self))
            
        ExFunc.displayActualQuestionPageWidgets(self, True)
