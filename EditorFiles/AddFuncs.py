import tkinter as tk
import customtkinter as ctk
from PIL import Image
from EditorFiles import ExFunc

def destroyCommand(self):
    you_sure = tk.messagebox.askyesno(title="Exit", message="Are you sure you want to exit out of this window?", default="no")

    if you_sure:
        self.window.destroy()
        self.app.window_up = False

def forgetFirstPageWidgets(self): #secondPageQuestionFormat
    self.frameA.pack_forget()
    self.frameB.pack_forget()
    self.answer_format_menu.pack_forget()
    self.continue_details_page_button.pack_forget()
    self.cancel_details_page_button.pack_forget()
    self.exit_button.pack_forget()

def continueFirstPageFunction(self):
    if ExFunc.firstPageValidator(self) != False:
        forgetFirstPageWidgets(self)

        # Opening the next page
        self.secondPage()

        displayPreviousQuestion(self)

def cancelFirstPageFunction(self):
    forgetFirstPageWidgets(self)

    # Changing the question in order to re display the previous data
    self.question_number-=1
    self.question_number_label.configure(text=f"Question {self.question_number}'s time setting and marks:")

    displayPreviousQuestion(self)

    # Opening the previous page
    ExFunc.displayActualQuestionPageWidgets(self,True)

def exitFirstPageFunction(self):
    exit = tk.messagebox.askyesno(title="Exit", message="Are you sure you want to your exit?", default="no")
    if exit:
        self.window.destroy()

def forgetSecondPageWidgets(self):
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

def secondPageQuestionFormat(self):
    ExFunc.forgetActualQuestionPageWidgets(self)

    # Redisplaying the window changes it depending on this question format was choosen/is currently at
    ExFunc.displayActualQuestionPageWidgets(self, True)

def questionImageFunction(event,self):
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

def solutionFunction(self):
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
    self.solution_format_menu = ctk.CTkOptionMenu(self.solution_frame, values=self.solution_question_formats, variable=self.solution_format_var, command=lambda event: solutionFormatFunction(self))
    
    #Textbox widget for text only
    self.solution_textbox = ctk.CTkTextbox(self.solution_and_feedback_window, width=500, height=300, border_width=0, text_color="#c8b800", wrap="word")
    # if self.solution_and_feedback == None: self.solution_and_feedback = "" #print
    self.solution_textbox.insert("0.0", self.solution_and_feedback) #Inserting the solution to the textbox configure
   
    #Add image widget for images only
    self.solution_question_image = ctk.CTkImage(light_image=Image.open(self.solution_image_filename), size=(400,200))
    self.solution_question_image_label = ctk.CTkLabel(self.solution_and_feedback_window, image=self.solution_question_image, text="", width=400, height=200)
    self.solution_question_image_label.bind("<Button-1>", lambda event: ExFunc.solutionQuestionImageFunction(self))

    self.solution_ok_button = ctk.CTkButton(self.solution_and_feedback_window, text="Ok", border_width=0, command=lambda: ExFunc.solutionOkFunction(self))
    self.solution_restart_button = ctk.CTkButton(self.solution_and_feedback_window, text="Restart Solution", border_width=0, command=lambda: ExFunc.restartSolution(self))
    self.solution_cancel_button = ctk.CTkButton(self.solution_and_feedback_window, text="Cancel",border_width=0, command=lambda: ExFunc.solutionCancelFunction(self))

    #Displaying wigets
    ExFunc.displaySolutionWidgets(self)

def solutionFormatFunction(self):
    ExFunc.forgetSolutionWidgets(self)
    ExFunc.displaySolutionWidgets(self)

def secondPageContinueFunction(self): 
    if ExFunc.secondPageValidator(self.option_A_entry, self.option_B_entry, self.option_C_entry, self.option_D_entry, self.option_A_button, self.option_B_button, self.option_C_button, self.option_D_button, self.options_variable, self.answer_format_menu_variable, self.without_options_textbox, self.question, self.image_filename):    
        forgetSecondPageWidgets(self)

        # Recording the data
        recordFunc(self)
        print(self.question_number)
        print(self.record)

        # Updating the question number and its label as you are moving the next question
        self.question_number+=1
        self.question_number_label.configure(text=f"Question {self.question_number}'s time setting and marks:") #Validator

        # Displaying the next page/first page again
        ExFunc.displayFirstPage(self)

def secondPageCancelFunction(self):
    forgetSecondPageWidgets(self)

    # Redisplaying the details page widgets
    ExFunc.displayFirstPage(self)

def doneFunction(self):
    if ExFunc.secondPageValidator(self.option_A_entry, self.option_B_entry, self.option_C_entry, self.option_D_entry, self.option_A_button, self.option_B_button, self.option_C_button, self.option_D_button, self.options_variable, self.answer_format_menu_variable, self.without_options_textbox, self.question, self.image_filename):
        done = tk.messagebox.askyesno(title="Save", message="Are you sure you want to save this topic?")
        if done:
            recordFunc(self)
            self.window.destroy()

            ExFunc.save(self,self.record)
            ExFunc.displayMenuTopics(self.app.menu)

def recordFunc(self):
    options = (self.option_A_entry.get(),self.option_B_entry.get(),self.option_C_entry.get(),self.option_D_entry.get())

    # Recording the time, marks, randomize option, option type, question type, hint, solution text, solution image, question text, question image, options, answer
    if self.question_number > len(self.record["Time"]):
        self.record["Time"].append(self.time_var.get())
        self.record["Marks"].append(self.marks_var.get())
        self.record["Randomize"].append(self.randomize.get())
        self.record["Option Type"].append(self.answer_format_menu_variable.get())
        self.record["Text Question"].append(self.question.get("0.0","end"))
        self.record["Image Question"].append(self.image_filename)
        # self.record["Question No"].append(self.question_number)
        self.record["Hint"].append(self.hint)
        self.record["Solution Text"].append(self.solution_and_feedback)
        self.record["Solution Image"].append(self.solution_image_filename)
        self.record["Options"].append(options)

        if self.record["Option Type"][-1] == "Options":
            self.record["Answer"].append(options[ExFunc.getAnswerChoosenIndex(self,self.options_variable.get())]) 
        else:
            self.record["Answer"].append(self.without_options_textbox.get("0.0","end"))
    else:
        self.record["Time"][self.question_number-1] = (self.time_var.get())
        self.record["Marks"][self.question_number-1] = (self.marks_var.get())
        self.record["Randomize"][self.question_number-1] = (self.randomize.get())
        self.record["Option Type"][self.question_number-1] = (self.answer_format_menu_variable.get())
        self.record["Text Question"][self.question_number-1] = (self.question.get("0.0","end"))
        self.record["Image Question"][self.question_number-1] = (self.image_filename)
        # self.record["Question No"][self.question_number-1] = (self.question_number)
        self.record["Hint"][self.question_number-1] = (self.hint)
        self.record["Solution Text"][self.question_number-1] = self.solution_and_feedback
        self.record["Solution Image"][self.question_number-1] = (self.solution_image_filename)
        self.record["Options"][self.question_number-1] = (options)

        if self.record["Option Type"][self.question_number-1] == "Options":
            self.record["Answer"][self.question_number-1] = (options[ExFunc.getAnswerChoosenIndex(self,self.options_variable.get())])
        else:
            self.record["Answer"][self.question_number-1] = (self.without_options_textbox.get("0.0","end"))

def displayPreviousQuestion(self):
    if self.question_number <= len(self.record["Time"]):
        options = self.record["Options"][self.question_number-1]
        answer = self.record["Answer"][self.question_number-1]

        (self.time_var.set(self.record["Time"][self.question_number-1]))
        (self.marks_var.set(self.record["Marks"][self.question_number-1]))
        # (self.randomize.configure(self.record["Randomize"][self.question_number-1]))
        (self.answer_format_menu_variable.set(self.record["Option Type"][self.question_number-1]))
        self.question.delete("0.0","end")
        (self.question.insert("0.0",f"{self.record["Text Question"][self.question_number-1]}"))
        (self.image_filename) = self.record["Image Question"][self.question_number-1]
        # self.record["Question No"][self.question_number-1] = (self.question_number)
        (self.hint) = self.record["Hint"][self.question_number-1]
        self.solution_and_feedback = self.record["Solution Text"][self.question_number-1]
        (self.solution_image_filename) = self.record["Solution Image"][self.question_number-1]

        self.option_A_entry.delete(0,last_index=tk.END); self.option_B_entry.delete(0,last_index=tk.END); self.option_C_entry.delete(0,last_index=tk.END); self.option_D_entry.delete(0,last_index=tk.END)    
        self.option_A_entry.insert(0,options[0]); self.option_B_entry.insert(0,options[1]); self.option_C_entry.insert(0,options[2]); self.option_D_entry.insert(0,options[3])

        if answer in options:
            d = {0:"A",1:"B",2:"C",3:"D"}

            index = options.index(answer)
            self.options_variable.set(d[index])

        else:
            (self.without_options_textbox.delete("0.0","end"))
            (self.without_options_textbox.insert("0.0",f"{answer}"))