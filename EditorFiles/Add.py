import customtkinter as ctk
import tkinter as tk
from PIL import Image

class Add:
    def __init__(self, app):
        self.app = app

    def detailsPage(self):
        self.window = ctk.CTkToplevel(self.app)
        self.window.transient(self.app)
        self.window.title("Add")
        self.window.geometry("800x550+300+50")

        #Functions
        def randomize():
            print(self.randomize.get())

        def continueFunction():
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.option_menu.pack_forget()
            self.continue_button.pack_forget()
            self.cancel_button.pack_forget()
            self.exit_button.pack_forget()

            #Opening the next page
            self.actualQuestionPage()

        def cancelFunction():
            pass

        def exitFunction():
            pass

        #Variable to keep track of the question
        self.question_number = 1

        #Contains the option menu and randomize checkbox
        self.frame1 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")
        self.frame1.pack(pady=10)

        #Allowing the user to enter the name of their topic
        self.topic_var = tk.StringVar() #This value is for testing
        self.topic = ctk.CTkEntry(self.frame1, border_width=0, corner_radius=10, width=200, justify="center", placeholder_text="Topic", placeholder_text_color="#c3c3c3")
        self.topic.pack(padx=10, side="left")

        #Randomize checkbox
        self.randomize = ctk.CTkCheckBox(self.frame1, text="Randomize", offvalue=0, onvalue=1,command=randomize)
        self.randomize.pack(side="right", pady=20, padx=20)

        #Details frame: Contains the question number, subject name, subject time an subject 
        self.frame2 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")
        self.frame2.pack(pady=30)

        #Creating title label
        self.question = ctk.CTkLabel(self.frame2, text=f"Question {self.question_number}:")
        self.question.pack(padx=10,side="left")

        #Allowing the user to enter the time boundry for their an individual question
        self.hours = "01" 
        self.minutes = "00" 
        self.seconds = "00" 
        self.time_var = tk.StringVar()
        self.time = ctk.CTkEntry(self.frame2, border_width=0, corner_radius=10, width=200, justify="center",placeholder_text_color="#c3c3c3", placeholder_text="00:00:00")
        self.time.pack(padx=10, side="left")

        #Allowing the user to enter the total marks for their an individual question
        self.marks_var = tk.StringVar()
        self.marks = ctk.CTkEntry(self.frame2, border_width=0, corner_radius=10, width=200, justify="center", placeholder_text="0", placeholder_text_color="#c3c3c3")
        self.marks.pack(padx=10,side="left")

        #Option Menu
        self.option_types = ["Options","Without Options"]
        self.option_menu_variable = tk.StringVar(value=self.option_types[0])
        self.option_menu = ctk.CTkOptionMenu(self.window, values=self.option_types, variable=self.option_menu_variable)
        self.option_menu.pack(pady=20, padx=20)

        #Continue Button
        self.continue_button = ctk.CTkButton(self.window, text="Continue", border_width=0, command=continueFunction)
        self.continue_button.pack(side="left", padx=20, pady=20, expand=True)

        #Cancel Button
        self.cancel_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=cancelFunction)
        self.cancel_button.pack(side="left", padx=20, pady=20, expand=True)

        #Exit Button
        self.exit_button = ctk.CTkButton(self.window, text="Exit", border_width=0, command=exitFunction)
        self.exit_button.pack(side="left", padx=20, pady=20, expand=True)

    def actualQuestionPage(self):
        def selectedOption():
            if self.options_variable.get() == "A": #if Option A is selected
                self.option_A_entry.configure(text_color="#00FF00")
                self.option_B_entry.configure(text_color="#FF0000")
                self.option_C_entry.configure(text_color="#FF0000")
                self.option_D_entry.configure(text_color="#FF0000")
            elif self.options_variable.get() == "B": #if Option B is selected
                self.option_A_entry.configure(text_color="#FF0000")
                self.option_B_entry.configure(text_color="#00FF00")
                self.option_C_entry.configure(text_color="#FF0000")
                self.option_D_entry.configure(text_color="#FF0000")
            elif self.options_variable.get() == "C": #if Option C is selected
                self.option_A_entry.configure(text_color="#FF0000")
                self.option_B_entry.configure(text_color="#FF0000")
                self.option_C_entry.configure(text_color="#00FF00")
                self.option_D_entry.configure(text_color="#FF0000")
            elif self.options_variable.get() == "D": #if Option D is selected
                self.option_A_entry.configure(text_color="#FF0000")
                self.option_B_entry.configure(text_color="#FF0000")
                self.option_C_entry.configure(text_color="#FF0000")
                self.option_D_entry.configure(text_color="#00FF00")

        self.hint = "" #Making an attribute to store the hint

        def hintFunction():
            def okFunction():
                if self.hint_entry.get() == "" or self.hint_entry.get().isspace():
                    tk.messagebox.showinfo(title="Invalid Hint", message="You have no real characters in your hint")
                else:
                    #Deleting any previous hints and storing the current hint
                    self.hint = self.hint_entry_variable.get()

                    self.hint_button.configure(text="Hint Added")
                    self.hint_window.destroy()

            def restartHint():
                hint_restart = tk.messagebox.askyesno(title="Restart Hint", message="Are you sure you want to delete your previous hint?")
                if hint_restart:
                    self.hint = "" #Deleting/Restarting the hint

                    self.hint_button.configure(text="Add Hint")
                    self.hint_window.destroy()

            def cancelFunction():
                self.hint_window.destroy()

            #Displaying the window and its features
            self.hint_window = ctk.CTkToplevel(self.window)
            self.hint_window.transient(self.window)
            self.hint_window.title("Hint")
            self.hint_window.geometry("600x200+300+50")

            #Adding wigets to the window
            self.hint_title = ctk.CTkLabel(self.hint_window, text="Please add a hint")
            self.hint_entry_variable = tk.StringVar(value=self.hint)
            self.hint_entry = ctk.CTkEntry(self.hint_window, textvariable=self.hint_entry_variable, width=300, height=40, border_width=0, text_color="#c8b800")
            self.hint_ok_button = ctk.CTkButton(self.hint_window, text="Ok", border_width=0, command=okFunction)
            self.hint_restart_button = ctk.CTkButton(self.hint_window, text="Restart Hint", border_width=0, command=restartHint)
            self.hint_cancel_button = ctk.CTkButton(self.hint_window, text="Cancel",border_width=0, command=cancelFunction)
            
            #Displaying the widgets
            self.hint_title.pack()
            self.hint_entry.pack(pady=10)
            self.hint_ok_button.pack(side="left", padx=30)
            self.hint_restart_button.pack(side="left", padx=30)
            self.hint_cancel_button.pack(side="left", padx=30)

        self.solution_and_feedback = "" #Making an attribute to store the solution and feedback 

        def solutionFunction():
            def solutionOkFunction():
                if self.solution_textbox.get('1.0', tk.END) == "" or self.solution_textbox.get('1.0', tk.END).isspace():
                    tk.messagebox.showinfo(title="Invalid Solution and Feedback", message="You have no real characters in your solution and feedback")
                else:
                    #Deleting any previous solution_and_feedback and feedback and storing the current solution and feedback
                    self.solution_and_feedback = self.solution_textbox.get('0.0', tk.END)

                    self.solution_and_feedback_button.configure(text="Solutions Added")
                    self.solution_and_feedback_window.destroy()

            def restartSolution():
                solution_restart = tk.messagebox.askyesno(title="Restart Solution and Feedback", message="Are you sure you want to delete your previous solution and feedback?")
                if solution_restart:
                    self.solution_and_feedback = "" #Deleting/Restarting the solution and feedback and feedback

                    self.solution_and_feedback_button.configure(text="Add Solutions")
                    self.solution_and_feedback_window.destroy()

            def solutionCancelFunction():
                self.solution_and_feedback_window.destroy()

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
            self.solution_format_menu = ctk.CTkOptionMenu(self.solution_frame, values=self.solution_question_formats, variable=self.solution_format_var)
            self.solution_textbox = ctk.CTkTextbox(self.solution_and_feedback_window, width=500, height=300, border_width=0, text_color="#c8b800", wrap="word")
            self.solution_textbox.insert("0.0", self.solution_and_feedback) #Inserting the solution to the textbox
            self.solution_ok_button = ctk.CTkButton(self.solution_and_feedback_window, text="Ok", border_width=0, command=solutionOkFunction)
            self.solution_restart_button = ctk.CTkButton(self.solution_and_feedback_window, text="Restart Solution", border_width=0, command=restartSolution)
            self.solution_cancel_button = ctk.CTkButton(self.solution_and_feedback_window, text="Cancel",border_width=0, command=solutionCancelFunction)
            
            #Displaying the widgets
            self.solution_frame.pack(pady=20)
            self.solution_format_menu.pack(side="left", padx=20)
            self.solution_title.pack(side="left", padx=20)
            self.solution_textbox.pack(pady=10)
            self.solution_ok_button.pack(side="left", padx=30)
            self.solution_restart_button.pack(side="left", padx=30)
            self.solution_cancel_button.pack(side="left", padx=30)

        def displayMainWidgets():
            #Displaying the widgets
            self.frame1.pack(pady=20)
            self.format_menu.pack(side="left", padx=40)
            self.hint_button.pack(side="left", padx=40)
            self.solution_and_feedback_button.pack(side="left", padx=40)
            if self.format_var.get() == "Text":
                self.question.pack(pady=10)
            elif self.format_var.get() == "Image":
                pass
            elif self.format_var.get() == "Video":
                pass
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
            self.continue_button.pack(side="left", padx=20, pady=20, expand=True)
            self.cancel_button.pack(side="left", padx=20, pady=20, expand=True)
            self.done_button.pack(side="left", padx=20, pady=20, expand=True)

        def forgetMainWidgets():
            #Displaying the widgets
            self.frame1.pack_forget()
            self.question.pack_forget()
            self.option_frame1.pack_forget()
            self.option_frame2.pack_forget()
            self.continue_button.pack_forget()
            self.cancel_button.pack_forget()
            self.done_button.pack_forget()

        def mainFormatFunction(format):
            forgetMainWidgets()
            displayMainWidgets()

        def continueFunction():
            pass

        def cancelFunction():
            pass

        def doneFunction():
            pass

        #This frame is used as a container for the "format menu" and the "hint button"
        self.frame1 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

        #Question Format Menu
        self.question_formats = ["Text","Image","Video"]
        self.format_var = tk.StringVar(value=self.question_formats[0])
        self.format_menu = ctk.CTkOptionMenu(self.frame1, values=self.question_formats, variable=self.format_var, command=mainFormatFunction)

        #Hint image for the button
        self.hint_img = ctk.CTkImage(light_image=Image.open("Pictures/Hint.png"), size=(30,30))

        #Hint button: When clicked, it allows the user to add or changes an assigned hint 
        self.hint_button = ctk.CTkButton(self.frame1, text="Add Hint", image=self.hint_img, command=hintFunction)

        #Solution button: When clicked, it allows the user to add the solution and feedback to that question
        self.solution_and_feedback_button = ctk.CTkButton(self.frame1, text="Add Solutions", command=solutionFunction)

        #Question textbox: This is where the user inserts their question
        self.question = ctk.CTkTextbox(self.window, width=600, text_color="#098bed", wrap="word")
        self.question.focus_set()

        #Option frames
        self.option_frame1 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3",height=50)

        self.option_frame2 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3",height=50)

        #Options variable
        self.options_variable = tk.StringVar()

        #Options button(radio button) and their entries
        self.option_A_button = ctk.CTkRadioButton(self.option_frame1,variable=self.options_variable, value="A", text="", command=selectedOption)

        self.option_A_entry = ctk.CTkEntry(self.option_frame1, border_width=2, width=275)

        self.option_B_button = ctk.CTkRadioButton(self.option_frame1,variable=self.options_variable, value="B", text="", command=selectedOption)

        self.option_B_entry = ctk.CTkEntry(self.option_frame1, border_width=2, width=275)

        self.option_C_button = ctk.CTkRadioButton(self.option_frame2,variable=self.options_variable, value="C", text="", command=selectedOption)

        self.option_C_entry = ctk.CTkEntry(self.option_frame2, border_width=2, width=275)

        self.option_D_button = ctk.CTkRadioButton(self.option_frame2,variable=self.options_variable, value="D", text="", command=selectedOption)

        self.option_D_entry = ctk.CTkEntry(self.option_frame2, border_width=2, width=275)

        #Continue Button
        self.continue_button = ctk.CTkButton(self.window, text="Continue", border_width=0, command=continueFunction)

        #Cancel Button
        self.cancel_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=cancelFunction)

        #Done Button
        self.done_button = ctk.CTkButton(self.window, text="Done", border_width=0, command=doneFunction)

        #Displaying the widgets
        self.frame1.pack(pady=20)
        self.format_menu.pack(side="left", padx=40)
        self.hint_button.pack(side="left", padx=40)
        self.solution_and_feedback_button.pack(side="left", padx=40)
        if self.format_var.get() == "Text":
            self.question.pack(pady=10)
        elif self.format_var.get() == "Image":
            pass
        elif self.format_var.get() == "Video":
            pass

        displayMainWidgets()