# This script here contains all the functions that are imported by two or more python scripts. Every function here is shared/imported as a function of the module "ExFunc" meaning "External Functionalities" by a least 2 scripts

import re
import tkinter as tk

def Validator(topic_entry_widget, time_entry_widget, marks_entry_widget):
    #Validating the topic names input
    if topic_entry_widget != None:
        if topic_entry_widget.get().isidentifier() == False:
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

def displayActualQuestionPageWidgets(frame1, format_menu, hint_button, solution_and_feedback_button, format_var, question_image_label, question, answer_format_menu_variable, option_frame1, option_frame2, option_A_button, option_A_entry, option_B_button, option_B_entry, option_C_button, option_C_entry, option_D_button, option_D_entry, without_options_textbox, cancel_actual_question_page_button, done_button, continue_present, continue_actual_question_page_button = None):
    #Displaying the widgets
    frame1.pack(pady=20)
    format_menu.pack(side="left", padx=40)
    hint_button.pack(side="left", padx=40)
    solution_and_feedback_button.pack(side="left", padx=40)

    #If the questin format is to be in text form
    if format_var.get() == "Text":
        question.pack(pady=10)
        question_image_label.pack_forget()

    #Else if the question format is to be in image form
    elif format_var.get() == "Image":
        question_image_label.pack(pady=10)
        question.pack_forget()

    #Else if the questin format is to be in video form
    elif format_var.get() == "Video":
        pass

    #Telling what answer format type to display: "Options" or "Without Options"
    if answer_format_menu_variable.get() == "Options":
        option_frame1.pack(fill="x", pady=3)
        option_frame2.pack(fill="x",pady=3)
        option_A_button.place(relx=0.05, rely=0.1)
        option_A_entry.place(relx=0.09,rely=0.1)
        option_B_button.place(relx=0.5,rely=0.1,)
        option_B_entry.place(relx=0.54,rely=0.1)
        option_C_button.place(relx=0.05,rely=0.1)
        option_C_entry.place(relx=0.09,rely=0.1)
        option_D_button.place(relx=0.5,rely=0.1)
        option_D_entry.place(relx=0.54,rely=0.1)

    elif answer_format_menu_variable.get() == "Without Options":
        without_options_textbox.pack()

    if continue_present == True:
        continue_actual_question_page_button.pack(side="left", padx=20, pady=20, expand=True)
    cancel_actual_question_page_button.pack(side="left", padx=20, pady=20, expand=True)
    done_button.pack(side="left", padx=20, pady=20, expand=True)

def forgetActualQuestionPageWidgets(frame1, question, question_image_label, without_options_textbox, option_frame1, option_frame2, continue_actual_question_page_button, cancel_actual_question_page_button, done_button):
    #Forgetting the widgets
    frame1.pack_forget()
    question.pack_forget()
    question_image_label.pack_forget()
    without_options_textbox.pack_forget()
    option_frame1.pack_forget()
    option_frame2.pack_forget()
    continue_actual_question_page_button.pack_forget()
    cancel_actual_question_page_button.pack_forget()
    done_button.pack_forget()

def createHintWidgets(self):
    import customtkinter as ctk

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