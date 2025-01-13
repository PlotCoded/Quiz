import customtkinter as ctk
import tkinter as tk
from PIL import Image

from EditorFiles import ExFunc

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

        global displayDetailsPageWidgets
        def displayDetailsPageWidgets():
            self.frameA.pack(pady=10)
            self.topic.pack(padx=10, side="left")
            self.randomize.pack(side="right", pady=20, padx=20)
            self.question_number_label.pack(pady=20)
            self.frameB.pack(pady=30)
            self.time.pack(padx=10, side="left")
            self.marks.pack(padx=10,side="left")
            self.answer_format_menu.pack(pady=20, padx=20)
            self.continue_details_page_button.pack(side="left", padx=20, pady=20, expand=True)

            #Displaying the "cancel button" when the user is just starting to add questions, in other words when the question number is 1
            if self.question_number > 1:
                self.cancel_details_page_button.pack(side="left", padx=20, pady=20, expand=True)

            self.exit_button.pack(side="left", padx=20, pady=20, expand=True)

        def forgetDetailsPageWidgets():
            self.frameA.pack_forget()
            self.frameB.pack_forget()
            self.answer_format_menu.pack_forget()
            self.continue_details_page_button.pack_forget()
            self.cancel_details_page_button.pack_forget()
            self.exit_button.pack_forget()

        def continueFunction():
            if ExFunc.Validator(self.topic, self.time, self.marks) != False:
                forgetDetailsPageWidgets()

                #Opening the next page
                self.actualQuestionPage()

        def cancelDetailsPageFunction():
            forgetDetailsPageWidgets()

            #Opening the previous page
            self.actualQuestionPage()

        def exitFunction():
            exit = tk.messagebox.askyesno(title="Exit", message="Are you sure you want to your exit?", default="no")
            if exit:
                self.window.destroy()

        #Variable to keep track of the question
        self.question_number = 1

        #Contains the option menu and randomize checkbox
        self.frameA = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

        #Allowing the user to enter the name of their topic
        self.topic_var = tk.StringVar(value="TopicName") #This value is for testing
        self.topic = ctk.CTkEntry(self.frameA, textvariable=self.topic_var, border_width=0, corner_radius=10, width=200, justify="center", placeholder_text="Topic Name", placeholder_text_color="#c3c3c3")

        #Randomize checkbox
        self.randomize = ctk.CTkCheckBox(self.frameA, text="Randomize", offvalue=0, onvalue=1,command=randomize)

        #Details frame: Contains the question number, subject name, subject time an subject 
        self.frameB = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

        #Creating title label
        self.question_number_label = ctk.CTkLabel(self.frameB, text=f"Question {self.question_number}'s time setting and marks:")

        #Allowing the user to enter the time boundry for their an individual question
        # self.hours = "01" 
        # self.minutes = "00" 
        # self.seconds = "00" 
        self.time_var = tk.StringVar(value="00:00:10")
        self.time = ctk.CTkEntry(self.frameB, textvariable=self.time_var, border_width=0, corner_radius=10, width=200, justify="center",placeholder_text_color="#c3c3c3", placeholder_text="00:00:00")

        #Allowing the user to enter the total marks for their an individual question
        self.marks_var = tk.IntVar(value=1)
        self.marks = ctk.CTkEntry(self.frameB, textvariable=self.marks_var, border_width=0, corner_radius=10, width=200, justify="center", placeholder_text="0", placeholder_text_color="#c3c3c3")

        #Option Menu
        self.answer_format = ["Options","Without Options"]
        self.answer_format_menu_variable = tk.StringVar(value=self.answer_format[0])
        self.answer_format_menu = ctk.CTkOptionMenu(self.window, values=self.answer_format, variable=self.answer_format_menu_variable)

        #Continue Button
        self.continue_details_page_button = ctk.CTkButton(self.window, text="Continue", border_width=0, command=continueFunction)

        #Cancel Button
        self.cancel_details_page_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=cancelDetailsPageFunction)

        #Exit Button
        self.exit_button = ctk.CTkButton(self.window, text="Exit", border_width=0, command=exitFunction)

        displayDetailsPageWidgets()

    def actualQuestionPage(self):
        self.hint = "" #Making an attribute to store the 
        print(self.hint, "when clicked the hint buton")

        def hintFunction():
            print(self.hint, "when clicked the hint buton")

            ExFunc.createHintWidgets(self)

        self.solution_and_feedback = "" #Making an attribute to store the solution and feedback 
        self.solution_image_filename = "Pictures/AddImage.jpg" #Making an attribute to store the solution image 

        def solutionFunction():
            def solutionQuestionImageFunction(event):
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

            def solutionFormatFunction(event):
                forgetSolutionWidgets()
                displaySolutionWidgets()

            def forgetSolutionWidgets():
                #Getting rid of widgets
                self.solution_frame.pack_forget()
                self.solution_format_menu.pack_forget()
                self.solution_title.pack_forget()
                self.solution_textbox.pack_forget()
                self.solution_question_image_label.pack_forget()
                self.solution_ok_button.pack_forget()
                self.solution_restart_button.pack_forget()
                self.solution_cancel_button.pack_forget()

            def displaySolutionWidgets():
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

            def solutionOkFunction():
                if (self.solution_textbox.get('0.0', tk.END) == "" or self.solution_textbox.get('0.0', tk.END).isspace()) and self.solution_image_filename == "Pictures/AddImage.jpg":
                    tk.messagebox.showinfo(title="Invalid Solution and Feedback", message="You have no real characters in your solution and feedback")
                else:
                    #Deleting any previous solution and feedback and storing the current solution and feedback
                    self.solution_and_feedback = self.solution_textbox.get('0.0', tk.END)

                    self.solution_and_feedback_button.configure(text="Solutions Added")
                    self.solution_and_feedback_window.destroy()

            def restartSolution():
                solution_restart = tk.messagebox.askyesno(title="Restart Solution and Feedback", message="Are you sure you want to delete your solution and feedback?")
                if solution_restart:
                    #Deleting/Restarting the solution and feedback and feedback
                    self.solution_and_feedback = ""
                    self.solution_image_filename = "Pictures/AddImage.jpg"

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
            self.solution_format_menu = ctk.CTkOptionMenu(self.solution_frame, values=self.solution_question_formats, variable=self.solution_format_var, command=solutionFormatFunction)
            
            #Textbox widget for text only
            self.solution_textbox = ctk.CTkTextbox(self.solution_and_feedback_window, width=500, height=300, border_width=0, text_color="#c8b800", wrap="word")
            self.solution_textbox.insert("0.0", self.solution_and_feedback) #Inserting the solution to the textbox
           
            #Add image widget for images only
            self.solution_question_image = ctk.CTkImage(light_image=Image.open(self.solution_image_filename), size=(400,200))
            self.solution_question_image_label = ctk.CTkLabel(self.solution_and_feedback_window, image=self.solution_question_image, text="", width=400, height=200)
            self.solution_question_image_label.bind("<Button-1>", solutionQuestionImageFunction)

            self.solution_ok_button = ctk.CTkButton(self.solution_and_feedback_window, text="Ok", border_width=0, command=solutionOkFunction)
            self.solution_restart_button = ctk.CTkButton(self.solution_and_feedback_window, text="Restart Solution", border_width=0, command=restartSolution)
            self.solution_cancel_button = ctk.CTkButton(self.solution_and_feedback_window, text="Cancel",border_width=0, command=solutionCancelFunction)

            #Displaying wigets
            displaySolutionWidgets()

        def forgetActualQuestionPageWidgets():
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

        def actualQuestionFormatFunction(event):
            ExFunc.forgetActualQuestionPageWidgets(self.frame1, self.question, self.question_image_label, self.without_options_textbox, self.option_frame1, self.option_frame2, self.continue_actual_question_page_button, self.cancel_actual_question_page_button, self.done_button)

            ExFunc.displayActualQuestionPageWidgets(self.frame1, self.format_menu, self.hint_button, self.solution_and_feedback_button, self.format_var, self.question_image_label, self.question, self.answer_format_menu_variable, self.option_frame1, self.option_frame2, self.option_A_button, self.option_A_entry, self.option_B_button, self.option_B_entry, self.option_C_button, self.option_C_entry, self.option_D_button, self.option_D_entry, self.without_options_textbox, self.cancel_actual_question_page_button, self.done_button, False, None)

        def questionImageFunction(event):
            self.image_filename = ctk.filedialog.askopenfilename()

            #Handling potential errors. Eg, when the user chooses a non-image file, i.e exe, mp4, py
            try:
                #Displaying the image on the question image label
                self.question_image.configure(light_image=Image.open(self.image_filename))
            except:
                if self.image_filename != "":
                    #Error message when the user chooses a non-image file
                    tk.messagebox.showerror(title="Invalid File", message="Please insert a valid image")
                
                #Making the image file to be its default "Pictures/AddImage.jpg"
                self.image_filename = "Pictures/AddImage.jpg"

        def continueActualQuestionPageFunction(): 
            if ExFunc.actualQuestionValidation(self.option_A_entry, self.option_B_entry, self.option_C_entry, self.option_D_entry, self.option_A_button, self.option_B_button, self.option_C_button, self.option_D_button, self.options_variable, self.answer_format_menu_variable, self.without_options_textbox, self.question, self.image_filename):
                #Incrementing the question to allow the user to move to the next question
                self.question_number+=1
                self.question_number_label.configure(text=f"Question {self.question_number} time settings and marks")
                
                forgetActualQuestionPageWidgets()
                displayDetailsPageWidgets()

        def cancelActualQuestionPageFunction():
            forgetActualQuestionPageWidgets()

            #Decrementing the question number by 1 only if the number is greater than one and displaying the question number
            if self.question_number > 1:
                self.question_number-=1
            self.question_number_label.configure(text=f"Question {self.question_number}'s time setting and marks:")


            #Redisplaying the details page widgets
            displayDetailsPageWidgets()

        def doneFunction():
            done = tk.messagebox.askyesno(title="Exit", message="Are you sure you want to save this topic?")
            if done:
                self.window.destroy()

        #This frame is used as a container for the "format menu" and the "hint button"
        self.frame1 = ctk.CTkFrame(self.window, border_width=0, fg_color="#c3c3c3")

        #Question Format Menu
        self.question_formats = ["Text","Image","Video"]
        self.format_var = tk.StringVar(value=self.question_formats[0])
        self.format_menu = ctk.CTkOptionMenu(self.frame1, values=self.question_formats, variable=self.format_var, command=actualQuestionFormatFunction)

        #Hint image for the button
        self.hint_img = ctk.CTkImage(light_image=Image.open("Pictures/Hint.png"), size=(30,30))

        #Hint button: When clicked, it allows the user to add or changes an assigned hint 
        self.hint_button = ctk.CTkButton(self.frame1, text="Add Hint", image=self.hint_img, command=hintFunction)

        #Solution button: When clicked, it allows the user to add the solution and feedback to that question
        self.solution_and_feedback_button = ctk.CTkButton(self.frame1, text="Add Solutions", command=solutionFunction)

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
        self.question_image_label.bind("<Button-1>", questionImageFunction)

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

        #Continue Button
        self.continue_actual_question_page_button = ctk.CTkButton(self.window, text="Continue", border_width=0, command=continueActualQuestionPageFunction)

        #Cancel Button
        self.cancel_actual_question_page_button = ctk.CTkButton(self.window, text="Cancel", border_width=0, command=cancelActualQuestionPageFunction)

        #Done Button
        self.done_button = ctk.CTkButton(self.window, text="Done", border_width=0, command=doneFunction)

        ExFunc.displayActualQuestionPageWidgets(self.frame1, self.format_menu, self.hint_button, self.solution_and_feedback_button, self.format_var, self.question_image_label, self.question, self.answer_format_menu_variable, self.option_frame1, self.option_frame2, self.option_A_button, self.option_A_entry, self.option_B_button, self.option_B_entry, self.option_C_button, self.option_C_entry, self.option_D_button, self.option_D_entry, self.without_options_textbox, self.cancel_actual_question_page_button, self.done_button, True, self.continue_actual_question_page_button)