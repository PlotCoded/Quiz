# This script here contains all the functions that are imported by two or more python scripts. Every function here is shared/imported as a function of the module "ExFunc" meaning "External Functionalities" by a least 2 scripts

import re
import tkinter as tk
import customtkinter as ctk
from PIL import Image

def Validator(topic_entry_widget, time_entry_widget, marks_entry_widget):
    #Validating the topic names input
    if topic_entry_widget != None:
        if topic_entry_widget.get() != None and topic_entry_widget.get().isidentifier() == False:
            tk.messagebox.showinfo(title="Invalid Topic Name", message="Your topic name doesn't have valid character(A-Z or _)")
            return False

    #Validating for time entry widget
    if len(time_entry_widget.get()) != 8:
        tk.messagebox.showinfo(title="Invalid Time Format", message='Your time format must be in the correct form. Example: "01:13:30" with 2 double colon each between 3 two digits numbers')
        return False

    #Validating the time input
    time = re.findall("[0-9][0-9]", time_entry_widget.get())

    #Validating for any zero time formats. Any also when the time format doesn't have 2 double colons and doesn't have 3 two digits numbers 
    if len(time) !=3 or len(time_entry_widget.get().split(":")) != 3:
        tk.messagebox.showinfo(title="Invalid Time Format", message='Your time format must be in the correct form. Example: "01:13:30" with 2 double colon each between 3 two digits numbers')
        return False

    if time_entry_widget.get() == "" or time_entry_widget.get() == "00:00:00":
        tk.messagebox.showinfo(title="Invalid Time Format", message='Your time value cannot be zero')
        return False

    #Validating for any value where the hours is greater than 24 and minutes and seconds is greater than 59
    if int(time[0]) > 23 or int(time[1]) > 59 or int(time[2]) > 59:
        tk.messagebox.showinfo(title="Invalid Time Format", message="Your time is not a valid standardized time format")
        return False

    #Validating for any string values
    if re.findall("[a-zA-Z]", time_entry_widget.get()):
        tk.messagebox.showinfo(title="Invalid Time Format", message='Your time format must be in the correct form. Example: "01:13:30" with no alphabets')
        return False

    #Validating for any symbol characters except ":"
    if re.findall(r"[!\"#$%&'()*+,\-./;<=>?@[\]^_`{|}~]", time_entry_widget.get()):
        tk.messagebox.showinfo(title="Invalid Time Format", message='Your time format must be in the correct form. Example: "01:13:30" with no symbols except ":"')
        return False

    #Validating for any spaces in the time
    if re.findall("\\s", time_entry_widget.get()):
        tk.messagebox.showinfo(title="Invalid Time Format", message='Your time format must be in the correct form. Example: "01:13:30" with no spaces')
        return False        

    #Validating the marks input
    if marks_entry_widget.get() == "" or marks_entry_widget.get() == "0" or marks_entry_widget.get().isnumeric() != True:
        tk.messagebox.showinfo(title="Invalid Marks Assigned", message="Your marks assigned must be made up of digits only")
        return False

def selectedOption(option_A_entry, option_B_entry, option_C_entry, option_D_entry, options_variable):
    # Don't forget to remove parameters and add "self" parameters
    if options_variable.get() == "A": #if Option A is selected
        option_A_entry.configure(text_color="#00FF00")
        option_B_entry.configure(text_color="#FF0000")
        option_C_entry.configure(text_color="#FF0000")
        option_D_entry.configure(text_color="#FF0000")
    elif options_variable.get() == "B": #if Option B is selected
        option_A_entry.configure(text_color="#FF0000")
        option_B_entry.configure(text_color="#00FF00")
        option_C_entry.configure(text_color="#FF0000")
        option_D_entry.configure(text_color="#FF0000")
    elif options_variable.get() == "C": #if Option C is selected
        option_A_entry.configure(text_color="#FF0000")
        option_B_entry.configure(text_color="#FF0000")
        option_C_entry.configure(text_color="#00FF00")
        option_D_entry.configure(text_color="#FF0000")
    elif options_variable.get() == "D": #if Option D is selected
        option_A_entry.configure(text_color="#FF0000")
        option_B_entry.configure(text_color="#FF0000")
        option_C_entry.configure(text_color="#FF0000")
        option_D_entry.configure(text_color="#00FF00")

def actualQuestionValidation(option_A_entry, option_B_entry, option_C_entry, option_D_entry, option_A_button, option_B_button, option_C_button, option_D_button, options_variable, answer_format_menu_variable, without_options_textbox, question, image_filename):
    # Don't forget to remove parameters and add "self" parameters

    #List of all options entry
    options_entry = [option_A_entry, option_B_entry, option_C_entry, option_D_entry]
    option_radio_buttons = [option_A_button, option_B_button, option_C_button, option_D_button]
    
    if answer_format_menu_variable.get() == "Options":
        #Validating for all the options 
        for _ in options_entry:
            if _.get() == "":
                tk.messagebox.showinfo(title="Empty Options Entry", message="Your option entry(s) cannot be empty")
                return False

        #Validating for answers: Ensuring an option is picked as an answer. Works for only the "options" format
        if options_variable.get() not in ["A","B","C","D"]:
            tk.messagebox.showinfo(title="No Answer Selected", message="You have to select an option as an answer")
            return False

    elif answer_format_menu_variable.get() == "Without Options":
        #Validating for non options answer textbox
        if without_options_textbox.get("0.0","end") == "\n":
            tk.messagebox.showinfo(title="Empty Options Entry", message="Your answer textbox cannot be empty")
            return False

    #Validating the question textbox and question image but checking is both formats are empty
    if question.get("0.0", "end") == "\n" and image_filename == "Pictures/AddImage.jpg":
        tk.messagebox.showinfo(title="No Question provided", message="You have no question provided")
        return False
    else:
        return True

def displayActualQuestionPageWidgets(self, continue_present):
    #Displaying the widgets
    self.frame1.pack(pady=20)
    self.format_menu.pack(side="left", padx=40)
    self.hint_button.pack(side="left", padx=40)
    self.solution_and_feedback_button.pack(side="left", padx=40)

    #If the questin format is to be in text form
    if self.format_var.get() == "Text":
        self.question.pack(pady=10)

        # For testing
        # self.question.insert("0.0","Which is the odd one?")
        self.question_image_label.pack_forget()

    #Else if the question format is to be in image form
    elif self.format_var.get() == "Image":
        self.question_image_label.pack(pady=10)
        self.question.pack_forget()

    #Else if the questin format is to be in video form
    elif self.format_var.get() == "Video":
        pass

    #Telling what answer format type to display: "Options" or "Without Options"
    if self.answer_format_menu_variable.get() == "Options":
        self.option_frame1.pack(fill="x", pady=3)
        self.option_frame2.pack(fill="x",pady=3)
        self.option_A_button.place(relx=0.05, rely=0.1)
        self.option_A_entry.place(relx=0.09,rely=0.1)
        self.option_B_button.place(relx=0.5,rely=0.1,)
        self.option_B_entry.place(relx=0.54,rely=0.1)
        self.option_C_button.place(relx=0.05,rely=0.1)
        self.option_C_entry.place(relx=0.09,rely=0.1)
        self.option_D_button.place(relx=0.5,rely=0.1)
        self.option_D_entry.place(relx=0.54,rely=0.1)

        # For testing
        # if self.question_number == 1:
        #     self.option_A_entry.insert(0,"Apple")
        #     self.option_B_entry.insert(0,"Banana")
        #     self.option_C_entry.insert(0,"Denmark")
        #     self.option_D_entry.insert(0,"Cherry")

    elif self.answer_format_menu_variable.get() == "Without Options":
        self.without_options_textbox.pack()

    if continue_present == True:
        self.continue_actual_question_page_button.pack(side="left", padx=20, pady=20, expand=True)
    self.cancel_actual_question_page_button.pack(side="left", padx=20, pady=20, expand=True)
    self.done_button.pack(side="left", padx=20, pady=20, expand=True)

def forgetActualQuestionPageWidgets(self):
    #Forgetting the widgets
    self.frame1.pack_forget()
    self.question.pack_forget()
    self.question_image_label.pack_forget()
    self.without_options_textbox.pack_forget()
    self.option_frame1.pack_forget()
    self.option_frame2.pack_forget()
    self.continue_actual_question_page_button.pack_forget()
    self.cancel_actual_question_page_button.pack_forget()
    self.done_button.pack_forget()

def createHintWidgets(self):
    #Displaying the window and its features
    self.hint_window = ctk.CTkToplevel(self.window)
    self.hint_window.transient(self.window)
    self.hint_window.title("Hint")
    self.hint_window.geometry("600x200+300+50")

    #Adding wigets to the window
    self.hint_title = ctk.CTkLabel(self.hint_window, text="Please add a hint")
    self.hint_entry_variable = tk.StringVar(value=self.hint)
    self.hint_entry = ctk.CTkEntry(self.hint_window, textvariable=self.hint_entry_variable, width=300, height=40, border_width=0, text_color="#c8b800")
    self.hint_ok_button = ctk.CTkButton(self.hint_window, text="Ok", border_width=0, command=lambda: hintOkFunction(self))
    self.hint_restart_button = ctk.CTkButton(self.hint_window, text="Restart Hint", border_width=0, command=lambda: restartHint(self))
    self.hint_cancel_button = ctk.CTkButton(self.hint_window, text="Cancel",border_width=0, command=lambda: hintCancelFunction(self))
    
    #Displaying the widgets
    self.hint_title.pack()
    self.hint_entry.pack(pady=10)
    self.hint_ok_button.pack(side="left", padx=30)
    self.hint_restart_button.pack(side="left", padx=30)
    self.hint_cancel_button.pack(side="left", padx=30)

def hintOkFunction(self):
    if self.hint_entry.get() == "" or self.hint_entry.get().isspace():
        print(self.hint, "If statement")
        tk.messagebox.showinfo(title="Invalid Hint", message="You have no real characters in your hint")
    else:
        #Deleting any previous hints and storing the current hint
        self.hint = self.hint_entry_variable.get()
        print(self.hint, "Else statement")

        self.hint_button.configure(text="Hint Added")
        self.hint_window.destroy()

def restartHint(self):
    self.hint_restart = tk.messagebox.askyesno(title="Restart Hint", message="Are you sure you want to your previous hint?")
    if self.hint_restart:
        self.hint = "" #Deleting/Restarting the hint

        self.hint_button.configure(text="Add Hint")
        self.hint_window.destroy()

def hintCancelFunction(self):
    self.hint_window.destroy()

def solutionQuestionImageFunction(self):
    self.solution_image_filename = ctk.filedialog.askopenfilename()

    #Handling potential errors. Eg, when the user chooses a non-image file, i.e exe, mp4, py
    try:
        #Displaying the image on the question image label
        self.solution_question_image.configure(light_image=Image.open(self.solution_image_filename))
    except:
        if self.solution_image_filename != "":
            #Error message when the user chooses a non-image file
            tk.messagebox.showerror(title="Invalid File", message="Please insert a valid image")

        #Making the image file to be its default "Pictures/AddImage.jpg"
        self.solution_image_filename = "Pictures/AddImage.jpg"

def questionImageFunction(self):
    print("Opening file window")
    self.image_filename = ctk.filedialog.askopenfilename()

    print(self.image_filename)
    #Handling potential errors. Eg, when the user chooses a non-image file, i.e exe, mp4, py
    try:
        #Displaying the image on the question image label format
        self.question_image.configure(light_image=Image.open(self.image_filename))
        print("No error occured")
    except Exception as message:
        print(message)
        if self.image_filename != "":
            #Error message when the user chooses a non-image file
            tk.messagebox.showerror(title="Invalid File", message="Please insert a valid image")
        
        #Making the image file to be its default "Pictures/AddImage.jpg"
        self.image_filename = "Pictures/AddImage.jpg"

def displaySolutionWidgets(self):
    #Displaying the widgets
    self.solution_frame.pack(pady=20)
    self.solution_format_menu.pack(side="left", padx=20)
    self.solution_title.pack(side="left", padx=20)

    #If the solution format is to be in text form
    if self.solution_format_var.get() == "Text":
        self.solution_textbox.pack(pady=10)

    #Else if the solution format is to be in image form
    elif self.solution_format_var.get() == "Image":
        self.solution_question_image_label.pack(pady=10)

    #Else if the solution format is to be in video form
    elif self.solution_format_var.get() == "Video":
        pass

    self.solution_ok_button.pack(side="left", padx=30)
    self.solution_restart_button.pack(side="left", padx=30)
    self.solution_cancel_button.pack(side="left", padx=30)

def solutionOkFunction(self):
    if (self.solution_textbox.get('0.0', tk.END) == "" or self.solution_textbox.get('0.0', tk.END).isspace()) and self.solution_image_filename == "Pictures/AddImage.jpg":
        tk.messagebox.showinfo(title="Invalid Solution and Feedback", message="You have no real characters in your solution and feedback")
    else:
        #Deleting any previous solution and feedback and storing the current solution and feedback
        self.solution_and_feedback = self.solution_textbox.get('0.0', tk.END)

        self.solution_and_feedback_button.configure(text="Solutions Added")
        self.solution_and_feedback_window.destroy()

def restartSolution(self):
    solution_restart = tk.messagebox.askyesno(title="Restart Solution and Feedback", message="Are you sure you want to delete your solution and feedback?")
    if solution_restart:
        #Deleting/Restarting the solution and feedback and feedback
        self.solution_and_feedback = ""
        self.solution_image_filename = "Pictures/AddImage.jpg"

        self.solution_and_feedback_button.configure(text="Add Solutions")
        self.solution_and_feedback_window.destroy() 

def forgetSolutionWidgets(self):
    #Getting rid of widgets
    self.solution_frame.pack_forget()
    self.solution_format_menu.pack_forget()
    self.solution_title.pack_forget()
    self.solution_textbox.pack_forget()
    self.solution_question_image_label.pack_forget()
    self.solution_ok_button.pack_forget()
    self.solution_restart_button.pack_forget()
    self.solution_cancel_button.pack_forget()

def solutionCancelFunction(self):
    self.solution_and_feedback_window.destroy()

# # Storage part
# data = {
#     "Randomize": True,
#     "Time": ["00:00:10","00:00:60","00:03:00","00:01:00","00:07:30",], format_var
#     "Marks": [1,1,1,1,1],
#     "Option Type": ["Without Options", "Options", "Without Options", "Options", "Without Options"],
#     "Text Question": ["What is the sum of 1 and 1?","What is the largest prime in between 100 and 200?","What is the value of the integral of f(x) in the interval [2,5], for which f(x) = x^2?","What is gradient of e^x when x = ln(1)?","Find the sum of all natural numbers bettween 1 to 100"],
#     "Image Question": ["Pictures/AddImage.jpg","Pictures/AddImage.jpg","Pictures/AddImage.jpg","Pictures/AddImage.jpg","Pictures/AddImage.jpg"],
#     "Question No": [1,2,3,4,5],
#     "Hint": [None, "Try starting from 200 downwards",None, "f(f^-1(x)) = x?","Try pairing up the starting number to the end number"],
#     "Solution Text": ["2","199","39","1","5050"],
#     "Solution Image": ["Pictures/AddImage.jpg","Pictures/AddImage.jpg","Pictures/AddImage.jpg","Pictures/AddImage.jpg","Pictures/AddImage.jpg"],
#     "Options": [["2","199","39","1"], ["2","199","39","1"],["2","199","39","1"],["2","199","39","1"],["2","199","39","5050"]],
#     "Answer": ["2","199","39","1","5050"]
# }

data = {
    "Randomize": True,
    "Time": [None],
    "Marks": [None],
    "Option Type": [None],
    "Text Question": [None],
    "Image Question": [None],
    "Question No": [None],
    "Hint": [None],
    "Solution Text": [None],
    "Solution Image": [None],
    "Options": [None],
    "Option Choosen": [None],
    "Answer": [None]
}

# def save(data):
#     dataframe = pandas.DataFrame(data, index=list(range(len(data["Question No"]))))
#     dataframe.to_csv("P.csv") # Creating the file for the topic. This file contains all the details for the topic created
