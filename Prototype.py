#Please, note if I refer to backend, I mean Storage.py

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image
import Storage

#Applying the theme of the window
ctk.set_default_color_theme("Gray.json")

#This class is the main window of the application
class Page(ctk.CTk):
    def __init__(self):
        super().__init__()

        #Adding a title
        self.title("QuizApp")

        #Getting maximum the size of the screen
        self.width = self.winfo_screenwidth() #Getting the user screen width
        self.height = self.winfo_screenheight()  #Getting the user screen height

        #Setting the width and height of the app to max
        self.geometry(f"{self.width}x{self.height}+{-10}+{0}") 

        #Creating grids for widgets placements
        self.columnconfigure(tuple(range(0,21)),weight=1)
        self.rowconfigure(tuple(range(0,21)),weight=1)

        #Note: These classes has to be called excatly as they are right now
        self.menuframe = MenuFrame(self)
        self.tophorizontalframe = TopHorizontalFrame(self)

        self.mainloop()

#Contains the instruction, start here and questions, etc
class QuestionFrame: 
    def __init__(self,app):
        self.app = app #The main window or the class "Page"
        self.review_has_been_made = False #This variable is true if the review page has been created before. 
        #The use of this variable is to clear the question page when the user wants to take another quiz only is the variable is True.
        self.times_up = False #Helps to change the timer widget once the time is up
        self.doing_the_test = True #Made to stop the timer. This variable tells if the user is still on the test. 
        #If not, eg,pressing "Quit" or "Submit", the timer will stop as the variable becomes False.
        self.subject_choosen = None

    def welcome(self):
        #This frame contains the welcome instruction to choose a topic from the Menu Button
        self.question_frame = ctk.CTkFrame(self.app, border_width=1, fg_color="#e3e3e3")
        self.question_frame.grid(row=1, column=0, rowspan=21, columnspan=21,sticky="nsew")

        #Instruction label
        self.instruction_label = ctk.CTkLabel(self.question_frame, text="Please choose a topic listed \n after clicking the Menu button", font=("Comic Sans MS",42), width=200,height=50,fg_color="#e3e3e3")
        self.instruction_label.pack(expand=True, fill="both")

    #Changing the content of the question frame in other to get ready to start the quiz
    def about_to_start(self):
        #Clearing the previous page
        self.instruction_label.pack_forget()

        if self.review_has_been_made == True: #Clearing the question page is there is a review page
            self.grade_image_label.pack_forget()
            self.your_score.pack_forget()

        #New Instruction Label
        self.new_instruction_label = ctk.CTkLabel(self.question_frame, width=200,height=50,fg_color="#e3e3e3")
        self.new_instruction_label.pack(expand=True, fill="both")
        self.new_instruction_label.configure(text="Please answer the questions listed\n after clicking the button below")
        self.new_instruction_label.configure(font=("Comic Sans MS",48))

        #Arrow Image
        self.arrow = ctk.CTkImage(light_image = Image.open("Arrow.jpg"), size=(170,170))

        #arrow label
        self.arrow_label = ctk.CTkLabel(self.question_frame, text="", image=self.arrow)
        self.arrow_label.pack()

        #Bringing the question page and also starting the timer
        def start():
            self.doing_the_test = True
            self.timer()
            self.actual_question()

            if self.last_number == 1:
                self.next_question_button.pack_forget()

        #Start Here Button: This button start the questions for the user to answer
        self.starting_button = ctk.CTkButton(self.question_frame, text="Start Here",width=225,height=105,corner_radius=10, font=("Comic Sans MS",40), command=start)
        self.starting_button.pack(expand=True)

    #Giving the user the actual questions/quiz
    def actual_question(self):
        self.doing_the_test = True #Starting the timer
        self.last_number = int(Storage.last_question(self.subject_choosen)) #This value is for testing for now. Record the number of questions the user has to do. Works with the backend
        self.answers_choosen = [] #Stores all the answers choosen
        self.question_number = 1 #Keeps track of the question the user is on

        #Disabling the subject buttons, eg, Math, Chemistry, Biology, etc but closing the menu frame
        self.app.tophorizontalframe.menu_button.configure(state="disabled")
        self.question_frame.grid(column=0, columnspan=21)
        self.app.menuframe.menu_frame.grid_forget()
        
        #Removing previous widgets in the about to start page
        self.new_instruction_label.pack_forget()
        self.arrow_label.pack_forget()
        self.starting_button.pack_forget()

        #Making the question number label
        self.question_no_label = ctk.CTkLabel(self.question_frame, text=f"Question {self.question_number}", font=("Cosmic Sans MS",36))
        self.question_no_label.pack(pady=20)

        #Displaying the question
        self.questions = {}
        for x,y in enumerate(Storage.get_questions(self.subject_choosen, "questions")):
            self.questions.update({x+1:y}) 
        self.question_label = ctk.CTkLabel(self.question_frame, text_color="#098bed",font=("Cosmic Sans MS",36))
        self.question_label.pack(pady=20)
        self.question_label.configure(text=self.questions[1])

        #Getting the options for each question
        self.questions_option = {}
        for x,y in enumerate(Storage.get_option_type(self.subject_choosen)):
            self.questions_option.update({x+1:y})
        self.option = self.questions_option[self.question_number]
        
        #Getting the options for all the questions that have options
        self.if_options = {}
        num_of_options = []
        for x,y in enumerate(Storage.get_option_type(self.subject_choosen)):
            if y == "Options":
                num_of_options.append(x+1)
        for x,y in enumerate(num_of_options):
            self.if_options.update({y:Storage.get_options(self.subject_choosen)[x]})

        #Storing the picked answer for a particular question in a variable
        self.answer_choosen = ""

        self.options = [] #This list stores the option choosen for a question(if the question choice of answer is options)

        global store_answer
        def store_answer(): #Storing the answer given in the self.answers_choosen variable
            if self.option == "Options": #If the question at that moment is an options only question
                for _ in self.options: #Looping through all the possible options(A,B,C and D)
                    if _.cget("fg_color") == "#afe1af": #Getting the option that was picked as the right option
                        self.answer_choosen = f"{_.cget('text')[3::]}" #Getting only the value of the option that was choosen which means excluding the A ., B ., etc parts
                        self.answers_choosen.append(self.answer_choosen) #Storing the answer

                        #Clearing the previous answer and unhighligthing the option
                        _.configure(fg_color="#e3e3e3")
                        _.configure(hover_color="#c3c3c3")
                        self.options.clear()
                        break
                else:
                    self.answer_choosen = ""
                    self.answers_choosen.append(self.answer_choosen) #Storing nothng as the answer if nothing was picked
            elif self.option == "Without Options": #The the question at that moment is a without options only question
                self.answer_choosen = self.answer_box.get("1.0","end-1c") #Getting the answer that was typed in
                self.answers_choosen.append(self.answer_choosen) #Storing the answer including nothing if no answers was picked

                #Cleaing the previous written answer
                self.answer_box.delete("0.0", "end") #Clearing the textbox when the user was to answer another without options answer

        #Creating the widgets where one answers the question 
        self.option_frame = ctk.CTkFrame(self.question_frame, border_width=0,fg_color="#4ee3e3")
        
        #Creating grids for widgets placements
        self.option_frame.columnconfigure(0,weight=1)
        self.option_frame.rowconfigure(tuple(range(0,4)),weight=1)

        #Creating options containers that host the values
        self.option1 = ctk.CTkButton(self.option_frame, fg_color="#e3e3e3", text_color="#23ccb2",border_width=0, hover_color="#c3c3c3", anchor="nsew", font=("Cosmic Sans MS",36), command=lambda: right_answer(self.option1))
        self.option2 = ctk.CTkButton(self.option_frame, fg_color="#e3e3e3", text_color="#23ccb2",border_width=0, hover_color="#c3c3c3", anchor="nsew", font=("Cosmic Sans MS",36), command=lambda: right_answer(self.option2))
        self.option3 = ctk.CTkButton(self.option_frame, fg_color="#e3e3e3", text_color="#23ccb2",border_width=0, hover_color="#c3c3c3", anchor="nsew", font=("Cosmic Sans MS",36), command=lambda: right_answer(self.option3))
        self.option4 = ctk.CTkButton(self.option_frame, fg_color="#e3e3e3", text_color="#23ccb2",border_width=0, hover_color="#c3c3c3", anchor="nsew", font=("Cosmic Sans MS",36), command=lambda: right_answer(self.option4))
        
        #Placing the options in the option frame
        self.option1.grid(row=0, column=0, sticky="nsew")
        self.option2.grid(row=1, column=0, sticky="nsew")
        self.option3.grid(row=2, column=0, sticky="nsew")
        self.option4.grid(row=3, column=0, sticky="nsew") 

        #Highlighting an answer as the answer the user picked  
        def right_answer(option):                
            if option in self.options and len(self.options) == 1: #This condition checks if an option was picked to unhighlight the option
                option.configure(fg_color="#e3e3e3") #Unhighlight the option
                option.configure(hover_color="#c3c3c3") 
                self.options.remove(option)
            elif option not in self.options and len(self.options) == 0: #This condition checks if an option was not picked to highlight an answer
                option.configure(fg_color="#afe1af") #Highlighting an option
                option.configure(hover_color="#afe1af")
                self.options.append(option) #Storing the option
            else:
                pass

        #Creating the textbox for the user to insert their answer for non-options/without options question
        self.answer_box = ctk.CTkTextbox(self.question_frame, width=750, height=75, text_color="#23ccb2", wrap="word", fg_color="#d3d3d3")
        
        #If it is an options question
        if self.option == "Options":
            #Option Frame: Contains all the options
            self.option_frame.pack(expand=False, fill="both") #Placing the container for the options

            #Assigning values to each options
            self.opt1 = self.if_options[self.question_number][0]
            self.option1.configure(text=f"A. {self.opt1}")

            self.opt2 = self.if_options[self.question_number][1]
            self.option2.configure(text=f"B. {self.opt2}")

            self.opt3 = self.if_options[self.question_number][2]
            self.option3.configure(text=f"C. {self.opt3}")

            self.opt4 = self.if_options[self.question_number][3]
            self.option4.configure(text=f"D. {self.opt4}")
                    
        #If it is an non-options question
        elif self.option == "Without Options":
            self.answer_box.pack(expand=True) #Placing the textbox

        #Adding the reset and submit button
        #End Frame: Contains the functionalities to "END" the test/quiz which are "reset" and "submit" buttons
        self.end_frame = ctk.CTkFrame(self.question_frame, border_width=0, fg_color="#e3e3e3")
        self.end_frame.pack(expand=True, fill="both" ,pady=10)

        #Functionality for the quit button
        def quit():
            #Displaying a message box
            quit = tk.messagebox.askyesno(title="Quit", message="Are you sure you want to quit?")

            if quit == True:
                self.doing_the_test = False #Stoping the timer

                #Enabling the menu button and expanding the menu frame
                self.app.tophorizontalframe.menu_button.configure(state="enabled")
                self.question_frame.grid(column=5, columnspan=17)
                self.app.menuframe.menu_frame.grid(row=1, column=0, rowspan=21, columnspan=5,sticky="nsew")

                self.welcome()

        #Next question button functionality
        def next_question():
            store_answer() #Storing the answer of the previous questions

            self.question_number+=1 #Increase the question number to go to the next question

            #Checking if the next question requires options or not
            self.option = self.questions_option[self.question_number]
            self.previous_option = self.questions_option[self.question_number-1]

            #Removing the previous widgets contents
            #Changing the question number label
            self.question_no_label.configure(text=f"Question {self.question_number}")

            #Changing the question to the next question
            self.question_label.configure(text=self.questions[self.question_number])

            #Removing the options or without option widget based on the previous question answering type(option or non-options)
            if self.previous_option == "Options":
                self.option_frame.pack_forget()
            elif self.previous_option == "Without Options":
                self.answer_box.pack_forget()

            #Removing the end frame
            self.end_frame.pack_forget()

            #Changing the options(if the next question if of options answering type)
            if self.question_number in self.if_options.keys():
                self.opt1 = self.if_options[self.question_number][0]
                self.opt2 = self.if_options[self.question_number][1]
                self.opt3 = self.if_options[self.question_number][2]
                self.opt4 = self.if_options[self.question_number][3]

            #Changing the options or without option widget based on the next question answering type(option or non-options)
            if self.option == "Options":
                self.option_frame.pack(expand=False, fill="both")

                #Changing each option contents
                self.option1.configure(text=f"A. {self.opt1}")
                self.option2.configure(text=f"B. {self.opt2}")
                self.option3.configure(text=f"C. {self.opt3}")
                self.option4.configure(text=f"D. {self.opt4}")
            elif self.option == "Without Options":
                self.answer_box.pack(expand=True)

            #Displaing the end frame
            self.end_frame.pack(expand=True, fill="both" , pady=10)

            if self.question_number == self.last_number:
            #Removing the next question because that is the last question so the button will useless
                self.next_question_button.pack_forget()
                self.question_no_label.configure(text=f"Last Question: Number {self.question_number}")

        #Submit button functionality
        def submit():
            submit = tk.messagebox.askyesno(title="Submit", message="Are you sure you want to submit")
        
            if submit == True:
                if self.times_up == False: #Preventing the review page from displaying twice once the time if up when the user clicked submit(yes) 
                #and the review page is already there because the time was up
                    store_answer() #Storing the answer for the last question
                    self.review() #Displaying the resultss

        #Adding the quit button
        self.quit_button = ctk.CTkButton(self.end_frame, text="Quit",height=75,width=150, corner_radius=10,command=quit)
        self.quit_button.pack(side="left", expand=True)

        #Adding the next question button
        self.next_question_button = ctk.CTkButton(self.end_frame, text="Next Question",height=75,width=150, corner_radius=10,command=next_question)
        self.next_question_button.pack(side="left", expand=True)

        #Adding the submit button
        self.submit_button = ctk.CTkButton(self.end_frame, text="Submit",height=75,width=150, corner_radius=10, command=submit)
        self.submit_button.pack(side="left", expand=True)

    #Adding the review page: This page gives the user the results such as score and grading remarks(eg, great job, excellent work,etc)
    def review(self):
        #Filling the answers that weren't answered with nothing
        if len(self.answers_choosen) < self.last_number:
            for _ in range(self.last_number - len(self.answers_choosen)):
                self.answers_choosen.append("")

        #Stoping the timer
        self.doing_the_test = False

        self.review_has_been_made = True #Preventing the review from displaying twice or more

        #Clearing the previous page(the actual question page)
        self.question_no_label.pack_forget()
        self.question_label.pack_forget()
        self.option_frame.pack_forget()
        self.answer_box.pack_forget()
        self.end_frame.pack_forget()

        #This are the grades given to the user based on their results
        self.grades = {"100":"Excellent Work", "75":"Great Job","60":"Good Job","50":"Well Done","40":"Nice Result","<40":"Good Attempt"}

        self.got_right_marks = 0 #The number of marks he got. This variable works with the backend. This value is for testing for now
        self.total_marks = Storage.get_marks(self.subject_choosen) #Total number of marks. This variable works with the backend. This value is for testing for now

        #Processing marks
        self.each_mark = int(self.total_marks) / int(self.last_number)

        for _ in range(len(Storage.get_answers(self.subject_choosen))):
            if self.answers_choosen[_] == Storage.get_answers(self.subject_choosen)[_]:
                self.got_right_marks+=self.each_mark

        #Getting the percantage
        self.got_right_marks = int(self.got_right_marks)
        self.total_marks = int(self.total_marks)
        self.percentage_scored = round((self.got_right_marks / self.total_marks) * 100)

        #Grade image
        self.grade_image = ctk.CTkImage(light_image=Image.open("Great Job.jpg"), size=(750,300))
        
        #Grade image container
        self.grade_image_label = ctk.CTkLabel(self.question_frame, text="", image=self.grade_image, width=750, height=300)

        #Getting the grade based on the score of the user
        if self.percentage_scored <= 100 and self.percentage_scored >= 75:
            self.grade = self.grades["100"]
            self.grade_image.configure(light_image=Image.open("Excellent Work.jpg"))
        elif self.percentage_scored < 75 and self.percentage_scored >= 60:
            self.grade = self.grades["75"]
            self.grade_image.configure(light_image=Image.open("Great Job.jpg"))
        elif self.percentage_scored < 60 and self.percentage_scored >= 50:
            self.grade = self.grades["60"]
            self.grade_image.configure(light_image=Image.open("Good Job.png"))
        elif self.percentage_scored < 50 and self.percentage_scored > 40:
            self.grade = self.grades["50"]
            self.grade_image.configure(light_image=Image.open("Well Done.jpg"))
        elif self.percentage_scored == 40:
            self.grade = self.grades["40"]
            self.grade_image.configure(light_image=Image.open("Nice Result.jpg"))
        elif self.percentage_scored < 40:
            self.grade = self.grades["<40"]
            self.grade_image.configure(light_image=Image.open("Good Attempt.png"))

        #Displaying grade image
        self.grade_image_label.pack(pady=20)

        #Displaying the score
        self.your_score = ctk.CTkLabel(self.question_frame, font=("Cosmic Sans MS",44), text_color="#cc397b")
        self.your_score.pack(pady=20)
        if self.times_up == False: #If the time never ran out, display this message
            self.your_score.configure(text=f"{self.grade}.\nYou got a {self.got_right_marks} out of {self.total_marks} or {self.percentage_scored}%")
        elif self.times_up == True: #If the time ran out, display this message
            self.your_score.configure(text=f"Sorry, your time is up but {self.grade}.\nYou got a {self.got_right_marks} out of {self.total_marks} or {self.percentage_scored}%")
        
        #Enabling the Menu button because the test has ended and expanding the menu subjects frame
        self.app.tophorizontalframe.menu_button.configure(state="enabled")
        self.question_frame.grid(column=5, columnspan=17)
        self.app.menuframe.menu_frame.grid(column=0,row=1)

    #Creatng the timer
    def timer(self):
        #Getting the time given for the subject. For now, this is testing. Works with the backend
        self.time = Storage.get_time(self.subject_choosen)

        #Getting each time format as hours, minutes and seconds
        self.hours = int(self.time.split(":")[0])
        self.minutes = int(self.time.split(":")[1])
        self.seconds = int(self.time.split(":")[2])

        def time_update():
            #Changing the time back to integers
            self.hours = int(self.hours)
            self.minutes = int(self.minutes)
            self.seconds = int(self.seconds)

            if self.doing_the_test == True:
                if self.hours + self.minutes + self.seconds > 0:
                    self.times_up = False

                    if self.hours == 0 and self.minutes == 0 and self.seconds > 0:
                        self.seconds-=1
                    elif self.hours == 0 and self.minutes > 0 and self.seconds == 0:
                        self.seconds = 59
                        self.minutes-=1
                    elif self.hours == 0  and self.minutes > 0 and self.seconds > 0:
                        self.seconds-=1
                    elif self.hours > 0 and self.minutes == 0 and self.seconds == 0:
                        self.hours-=1
                        self.minutes = 59
                        self.seconds = 59
                    elif self.hours > 0 and self.minutes > 0 and self.seconds == 0:
                        self.minutes-=1
                        self.seconds = 59
                    elif self.hours > 0 and self.minutes > 0 and self.seconds > 0:
                        self.seconds-=1
                    elif self.hours > 0 and self.minutes == 0  and self.seconds > 0:
                        self.seconds-=1
                    else:
                        pass

                    #Making the timer look more like a timer only when the digits are 1. Eg, 1:2:9 to 01:02:09
                    if (self.hours >= 0 and self.hours < 10):
                        self.hours = "0" + str(self.hours)
                    if (self.minutes >= 0 and self.minutes < 10):
                        self.minutes = "0" + str(self.minutes)
                    if (self.seconds >= 0 and self.seconds < 10):
                        self.seconds = "0" + str(self.seconds)

                    #Displaying the timer in the time widget located in the top horizontal frame
                    self.app.tophorizontalframe.time_variable.set(f"{self.hours}: {self.minutes}: {self.seconds}")
                    self.app.after(1000, time_update)
                else:
                    self.times_up = True
                    self.review() #Displaying the result because the time is up
            else:
                pass

        time_update()

#This is the vertical frame placed at the left side of the app
class MenuFrame: 
    def __init__(self, app):
            self.app = app

            self.Menu_frame()
            self.scroll_frame()
            self.topic_label()
            self.editor_frame()

            #This attributes are to be used later on in the program
            self.add_question_choice = None #This is the question answering type format such as options and non-options
            self.right_answer_picked = False #Checks if an answer has been picked for only option questions

            #Storage variables
            self.storage_details = {}
            self.storage_questions = {}
            self.storage_option_type = {}
            self.storage_options = {}
            self.storage_answers = {}

    def Menu_frame(self):
        #Menu Frame: Contains Scrollable frame
        self.menu_frame = ctk.CTkFrame(self.app, fg_color="#fff", border_width=2)

    def scroll_frame(self):
        #Scrollable frame: Contains Topic label, editor widgets like add, edit, delete and also the topics buttons such as Math, Chemistry
        self.scroll_frame = ctk.CTkScrollableFrame(self.menu_frame, corner_radius=0, border_width=1, fg_color="#fff",orientation="vertical",)
        self.scroll_frame.pack(expand=True, fill="both")

    def topic_label(self):
        #Topics label
        self.topics_label = ctk.CTkLabel(self.scroll_frame, text="Topics",width=200,height=50,fg_color="#a3a3a3")
        self.topics_label.pack(fill="x",pady=10,padx=10)

    def editor_frame(self): #Contains the search, add, edit and delete
        def disable_editor_buttons():
            #Ensuring another Editor(Search, Add, Edit or Delete) Window cannot be created at the same time if any of the editor buttons(search, add, etc) have been clicked and created
            self.search_button.configure(state="disabled")
            self.add_button.configure(state="disabled")
            self.edit_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")

        def editor_window_func():
            #Check if the topic inputed has been created before
            self.check_topic = False

            #Keeps track of which question number the user is on at that moment
            self.question_number = 1 

            #Creating a new window to add a new subject and its details
            self.editor_window = ctk.CTkToplevel()

            #Getting the user screen width
            self.width = self.editor_window.winfo_screenwidth() 

            #Creating its geometry and specifying a position
            self.editor_window.geometry(f"750x500+{self.width//2}+{100}")

            #Ensuring the toplevel window sit above all other windows
            self.editor_window.attributes("-topmost", True)

            #Window closing event: Runs a function when the window is closed
            self.editor_window.protocol("WM_DELETE_WINDOW", self.enable_again)
        
        #Enabling functions again
        def enable_again():
            #Closing the window
            self.editor_window.destroy()
            
            #Enabling the buttons again
            self.search_button.configure(state="enabled")
            self.add_button.configure(state="enabled")
            self.edit_button.configure(state="enabled")
            self.delete_button.configure(state="enabled")

            #Reloading the subject again
            self.scroll_frame.pack_forget()

            #Scroll frame
            self.scroll_frame = ctk.CTkScrollableFrame(self.menu_frame, corner_radius=0, border_width=1, fg_color="#fff",orientation="vertical",)
            self.scroll_frame.pack(expand=True, fill="both")

            #Topics label
            self.topics_label = ctk.CTkLabel(self.scroll_frame, text="Topics",width=200,height=50,fg_color="#a3a3a3")
            self.topics_label.pack(fill="x",pady=10,padx=10)

            #Editor buttons
            self.display_editor()

            #Subjects
            self.display_subjects()
        #<<<<<<<<<<<<<-----------------Search and Delete---------------------------->>>>>>>>>>>
        def search_delete():
            #Creating the window for the widgets to be placed in it
            self.editor_window_func()

            self.editor_window.title("Search")

            #Search-Delete Label
            self.search_delete_label = ctk.CTkLabel(self.editor_window, text="Kindly please enter a topic")
            self.search_delete_label.pack(pady=20)

            #Search-Delete Entry
            self.search_delete_entry = ctk.CTkEntry(self.editor_window, border_width=2, width=300, corner_radius=10)
            self.search_delete_entry.pack(pady=20)

            #Invalid Input label
            self.search_delete_invalid_label = ctk.CTkLabel(self.editor_window, text_color="red", text="Sorry, this topic does not exist. \n Please enter a topic that has been created")

            #Container that contains the ok and cancel buttons
            self.search_delete_frame = ctk.CTkFrame(self.editor_window,border_width=0, fg_color="#c3c3c3")
            self.search_delete_frame.pack(pady=20)

            #Search-Delete ok
            self.search_delete_ok = ctk.CTkButton(self.search_delete_frame, text="OK", border_width=0)
            self.search_delete_ok.pack(side="left",expand=True,padx=20)

            #Search-Delete delete
            self.search_delete_cancel = ctk.CTkButton(self.search_delete_frame, text="Cancel", border_width=0)
            self.search_delete_cancel.pack(side="left",expand=True,padx=20)
        
        def search_delete_checker(user_input, use):
            if user_input in self.subjects_list: #Checking if the user's subject is actually an existing subect
                self.search_delete_invalid_label.pack_forget() #Removing the invalid label if the user enter an invalid topic previously

                if use == "Delete": #If the user used the delete editor button
                    you_sure = tk.messagebox.askyesno(title="Delete Topic", message="Are you sure you want to delete this topic?")
                    
                    if you_sure == True:
                        self.editor_window.destroy()
                    elif you_sure == False:
                        pass
                else: #If the user used the search editor button
                    self.editor_window.destroy()
            elif user_input not in self.subjects_list: #If the user inputed an invalid topic or the topic doesn't exists
                self.search_delete_invalid_label.pack(pady=40)
        
        #The Search and Delete cancel button functions
        def search_delete_cancel_func():
            self.editor_window.destroy()

        #<<<<<<<<<<<<<<<<<<<<<----------------Add------------------------------------>>>>>>>>>>>>>>>>>>>>>>>>>>
        def question_info():
            #Creating title label
            self.title = ctk.CTkLabel(self.editor_window, text="Please add a subject name, time and marks respectively", font=("Cosmic Sans MS",24))
            self.title.pack(pady=10)

            #Details frame: Contains the question number, subject name, subject time an subject 
            self.detail_frame = ctk.CTkFrame(self.editor_window, border_width=0, fg_color="#c3c3c3")
            self.detail_frame.pack(pady=10)

            #Creating title label
            self.question_number_label = ctk.CTkLabel(self.detail_frame, text=f"Question: {self.question_number}-->")
            self.question_number_label.pack(padx=10,side="left")

            #Naming entry: This give the name of the subject that is about to be added
            self.subject_name_var = tk.StringVar(value="Mathematics") #This value is for testing
            self.subject_name = ctk.CTkEntry(self.detail_frame, border_width=0, corner_radius=10, width=200, justify="center", textvariable=self.subject_name_var)
            self.subject_name.pack(padx=10,side="left")

            #Naming entry: This give the name of the subject that is about to be added
            self.hours = "01" #This value is for testing
            self.minutes = "00" #This value is for testing
            self.seconds = "00" #This value is for testing
            self.time_var = tk.StringVar(value=f"{self.hours}:{self.minutes}:{self.seconds}")
            self.time_number = ctk.CTkEntry(self.detail_frame, border_width=0, corner_radius=10, width=200, justify="center", textvariable=self.time_var)
            self.time_number.pack(padx=10, side="left")

            #Naming entry: This give the name of the subject that is about to be added
            self.marks_var = tk.StringVar(value=100) #This value is for testing
            self.marks_number = ctk.CTkEntry(self.detail_frame, border_width=0, corner_radius=10, width=200, justify="center", textvariable=self.marks_var)
            self.marks_number.pack(padx=10,side="left")

            #Option Menu
            self.option_menu_values = ["Options","Without Options"]
            self.option_menu_variable = tk.StringVar(value=self.option_menu_values[1])
            self.option_menu = ctk.CTkOptionMenu(self.editor_window, values=self.option_menu_values, variable=self.option_menu_variable)
            self.option_menu.pack(pady=20)

            #Continue Button
            self.continue_button = ctk.CTkButton(self.editor_window, text="Continue", border_width=0)
            self.continue_button.pack(side="left", padx=20, pady=20, expand=True)

            #Save and Exit Button
            self.save_button = ctk.CTkButton(self.editor_window, text="Save and Exit", border_width=0)
            self.save_button.pack(side="left", padx=20, pady=20, expand=True)

            #Cancel Button
            self.cancel_button = ctk.CTkButton(self.editor_window, text="Cancel/Exit", border_width=0)
            self.cancel_button.pack(side="left", padx=20, pady=20, expand=True)
        
        def forget_question_info():
            #Removing the previous widgets to for new ones to come along
            self.title.pack_forget()
            self.detail_frame.pack_forget()
            self.option_menu.pack_forget()
            self.continue_button.pack_forget()
            self.save_button.pack_forget()
            self.cancel_button.pack_forget()
        
        def question_widget():
            #Question Label
            self.question_label = ctk.CTkLabel(self.editor_window, text="Please add your question in the textbox below", font=("Cosmic Sans MS", 24))
            self.question_label.pack()

            #Question textbox: This is where the user inserts their question
            self.question = ctk.CTkTextbox(self.editor_window, width=600, text_color="#098bed", wrap="word")
            self.question.pack(pady=10)
            self.question.focus_set()

            #Variable to check if the question widget has a question inside.
            #It also reset the variable everytime a new question is about to be created.
            #The reason for this variable is to ensure the user input a question before moving on to the next questions
            self.question_filled = False
        
        def option_question_widget():            
            #Option Frame
            self.option_frame = ctk.CTkFrame(self.editor_window, fg_color="#c3c3c3", border_width=0)
            self.option_frame.pack()

            self.right_answer_picked = False #This variable ensures an answer is always picked before moving on the another question
            
            self.options = [] #This list stores the option choosen as the right answer for a question(if the question type is of options)
            
            #Right Answer func
            def right_answer(option): #This function is used to highlight/unhighlight and store an option as a right answer
                if option in self.options and len(self.options) == 1: #If there is an option that was picked for a right answer. 
                #This "if" block is used when the user wants to remove an option that was picked as the right answer
                    option.configure(fg_color="#d3d3d3") #Unhighlighting the option
                    self.options.remove(option) 
                    self.answer_picked = None #Removing the option that was picked as the right answer
                    self.right_answer_picked = False #Remembering that a right answer wasn't picked
                elif option not in self.options and len(self.options) == 0: #If there isn't an option that was picked for a right answer
                #This "elif" block is used when the user wants to add an option to be picked as the right answer
                    option.configure(fg_color="#ADD8E6") #Highlighting the option
                    self.options.append(option)
                    self.answer_picked = option.get() #Adding the option that is to be picked as the right answer
                    self.right_answer_picked = True #Remembering that a right answer was picked
                else:
                    pass

            #Option 1
            self.option1 = ctk.CTkEntry(self.option_frame, fg_color="#d3d3d3", border_width=0, placeholder_text="A", placeholder_text_color="#c1c1c1", text_color="#23ccb2")
            self.option1.pack(side="left", padx=10)
            self.option1.bind("<Double-Button-1>", lambda event: right_answer(self.option1))
            self.option1.bind("<Button-3>", lambda event: right_answer(self.option1))

            #Option 2
            self.option2 = ctk.CTkEntry(self.option_frame, fg_color="#d3d3d3", border_width=0, placeholder_text="B", placeholder_text_color="#c1c1c1", text_color="#23ccb2")
            self.option2.pack(side="left", padx=10)
            self.option2.bind("<Double-Button-1>", lambda event: right_answer(self.option2))
            self.option2.bind("<Button-3>", lambda event: right_answer(self.option2))

            #Option 3
            self.option3 = ctk.CTkEntry(self.option_frame, fg_color="#d3d3d3", border_width=0, placeholder_text="C", placeholder_text_color="#c1c1c1", text_color="#23ccb2")
            self.option3.pack(side="left", padx=10)
            self.option3.bind("<Double-Button-1>", lambda event: right_answer(self.option3))
            self.option3.bind("<Button-3>", lambda event: right_answer(self.option3))

            #Option 4
            self.option4 = ctk.CTkEntry(self.option_frame, fg_color="#d3d3d3", border_width=0, placeholder_text="D", placeholder_text_color="#c1c1c1", text_color="#23ccb2")
            self.option4.pack(side="left", padx=10)
            self.option4.bind("<Double-Button-1>", lambda event: right_answer(self.option4))
            self.option4.bind("<Button-3>", lambda event: right_answer(self.option4))

            #Continue Button
            self.continue_button2 = ctk.CTkButton(self.editor_window, text="Continue", border_width=0)
            self.continue_button2.pack(pady=10,side="left", padx=20, expand=True)

            #Finished Button
            self.finished_button = ctk.CTkButton(self.editor_window, text="Finished", border_width=0)
            self.finished_button.pack(pady=10, side="left",padx=20, expand=True)

            #Cancel Button
            self.cancel_button2 = ctk.CTkButton(self.editor_window, text="Cancel", border_width=0)
            self.cancel_button2.pack(pady=10,side="left", padx=20, expand=True)
        
        def without_option_question_widget():
            #Question Label
            self.answer_label = ctk.CTkLabel(self.editor_window, text="Add your answer below", font=("Cosmic Sans MS", 24))
            self.answer_label.pack(pady=10)
            
            #Answer textbox
            self.answer = ctk.CTkTextbox(self.editor_window, width=600, height=30, text_color="#23ccb2", wrap="word")
            self.answer.pack(pady=10)

            #Continue Button
            self.continue_button2 = ctk.CTkButton(self.editor_window, text="Continue", border_width=0)
            self.continue_button2.pack(pady=10,side="left", padx=20, expand=True)

            #Finished Button
            self.finished_button = ctk.CTkButton(self.editor_window, text="Finished", border_width=0)
            self.finished_button.pack(pady=10, side="left",padx=20, expand=True)

            #Cancel Button
            self.cancel_button2 = ctk.CTkButton(self.editor_window, text="Cancel", border_width=0)
            self.cancel_button2.pack(pady=10,side="right", padx=20, expand=True)
        
        def forget_question_page():
            if self.option_menu_variable.get() == "Options":
                #Removing Page2 widgets for Page1 widgets to come again but only for a question page with options
                self.question_label.pack_forget()
                self.question.pack_forget()
                self.option_frame.pack_forget()
                self.continue_button2.pack_forget()
                self.finished_button.pack_forget()
                self.cancel_button2.pack_forget()
            
            elif self.option_menu_variable.get() == "Without Options":
                #Removing Page2 widgets for Page1 widgets to come again but only for a question page without options
                self.question_label.pack_forget()
                self.question.pack_forget()
                self.answer_label.pack_forget()
                self.answer.pack_forget()
                self.continue_button2.pack_forget()
                self.finished_button.pack_forget()
                self.cancel_button2.pack_forget()
        
        def display_question_info_again():
            #Displaying Page1 widgets again
            self.title.pack(pady=10)
            self.detail_frame.pack(pady=10)
            self.option_menu.pack(pady=10)
            self.continue_button.pack(side="left", padx=20, pady=80, expand=True)
            self.save_button.pack(side="left", padx=20, pady=80, expand=True)
            self.cancel_button.pack(side="left", padx=20, pady=80, expand=True)
        
        #<<<<<<<<<<<<<<<<<<<<-----------------------Edit---------------------->>>>>>>>>>>>>>>>>>>>>
        def edit_subject_list():
            #This scoll frame contains all the subjects that the user has made
            self.subjects_scroll_frame = ctk.CTkScrollableFrame(self.editor_window, corner_radius=0, border_width=1, fg_color="#c3c3c3",orientation="vertical",)
            self.subjects_scroll_frame.pack(expand=True, fill="both")

            #Title
            self.edit_subject_title = ctk.CTkLabel(self.editor_window, text="Please select a topic to edit", font=("Cosmic Sans MS",20))
            self.edit_subject_title.pack(pady=10)

            #Displaying the subjects in the scroll frame
            subject_list_widget = [
                f"{self.subjects_list[_]} = ctk.CTkButton(self.subjects_scroll_frame, text=f'{self.subjects_list[_]}',fg_color='#d3d3de',width=200,height=50,corner_radius=10,border_width=2,hover_color='#b3b3be',command=lambda: edit_subjects_clicked(f'{self.subjects_list[_]}'))" 
                for _ in range(len(self.subjects_list))
                ] 
            subject_widget_packed = [f"{self.subjects_list[_]}.pack(expand=True,fill='x',padx=10,pady=10)" for _ in range(len(self.subjects_list))]
            
            #Executing each functions in the lists to make and display each subject buttons
            for _ in subject_list_widget:
                exec(_)

            for _ in subject_widget_packed:
                exec(_)
            
        global edit_subjects_clicked
        def edit_subjects_clicked(sub):            
            self.subject = sub

            self.forget_edit_subject_list()
            self.title_or_question()
        
        def forget_edit_subject_list():
            self.subjects_scroll_frame.pack_forget()
            self.edit_subject_title.pack_forget() 
        
        def title_or_question():
            #Container for all the buttons on that page
            self.title_or_question_frame = ctk.CTkFrame(self.editor_window, fg_color="#c3c3c3", border_width=0)
            self.title_or_question_frame.pack(expand=True, fill="both")

            #This button will give a pge that will change the subject's name
            self.change_subject_name_button = ctk.CTkButton(self.title_or_question_frame, text="Change Subject Name", command=self.change_subject_name_page, width=400, anchor="justify")
            self.change_subject_name_button.pack(expand=True, side="top")

            #This button will give a page that will change the subject's details(Subject's Name, Time, Marks)
            self.change_subject_details_button = ctk.CTkButton(self.title_or_question_frame, text="Change Subject Details", command=self.change_subject_details_page, width=400, anchor="justify")
            self.change_subject_details_button.pack(expand=True, side="top")

            #This button will give a page to change the selected question
            self.change_question_button = ctk.CTkButton(self.title_or_question_frame, text="Change Question", command=lambda: self.add_question("none"), width=400, anchor="justify")
            self.change_question_button.pack(expand=True, side="top")

            #This button will give a page to add a question before the selected question
            self.add_question_before_button = ctk.CTkButton(self.title_or_question_frame, text="Add new question before a question", command=lambda: self.add_question("before"), width=400, anchor="justify")
            self.add_question_before_button.pack(expand=True, side="top")

            #This button will give a page to add a question after the selected question
            self.add_question_after_button = ctk.CTkButton(self.title_or_question_frame, text="Add new question after a question", command=lambda: self.add_question("after"), width=400, anchor="justify")
            self.add_question_after_button.pack(expand=True, side="top")

            #This button will give a page to delete the selected question
            self.delete_question_button = ctk.CTkButton(self.title_or_question_frame, text="Delete Question", command=self.delete_question_page, width=400, anchor="justify")
            self.delete_question_button.pack(expand=True, side="top")

            #Cancel Button
            self.title_or_question_cancel_button = ctk.CTkButton(self.editor_window, text="Cancel", border_width=0, command=self.title_or_question_cancel_func)
            self.title_or_question_cancel_button.pack(expand=True, side="bottom", pady=20)

        def forget_title_or_question():
            self.title_or_question_frame.pack_forget()
            self.title_or_question_cancel_button.pack_forget() 
        
        def title_or_question_cancel_func():
            self.forget_title_or_question()
            self.edit_subject_list()

        def change_subject_name_page(): 
            self.forget_title_or_question()

            #Tip Label
            self.tip_label = ctk.CTkLabel(self.editor_window, text="Change the subject name", font=("Cosmic Sans MS",24))
            self.tip_label.pack(pady=10)

            #Details frame: Contains the ssubject's title, time and marks
            self.detail_frame = ctk.CTkFrame(self.editor_window, border_width=0, fg_color="#c3c3c3")
            self.detail_frame.pack(pady=20, fill="both")

            #This give the name of the current subject which name will be changed
            self.current_subject_name_var = tk.StringVar(value="Subject") #This value is for testing
            self.current_subject_name = ctk.CTkEntry(self.detail_frame, border_width=0, corner_radius=10, width=200, justify="center", textvariable=self.current_subject_name_var)
            self.current_subject_name.pack(padx=10,side="left", fill="both", expand=True)

            #This give the name of the future/new subject name
            self.new_subject_name_var = tk.StringVar(value="NewSubject") #This value is for testing
            self.new_subject_name = ctk.CTkEntry(self.detail_frame, border_width=0, corner_radius=10, width=200, justify="center", textvariable=self.new_subject_name_var)
            self.new_subject_name.pack(padx=10,side="left", fill="both", expand=True)

            #Save and Exit Button
            self.edit_save_button = ctk.CTkButton(self.editor_window, text="Save", border_width=0, command=self.subject_save_func)
            self.edit_save_button.pack(side="left", padx=20, pady=20, expand=True)

            #Cancel Button
            self.edit_cancel_button = ctk.CTkButton(self.editor_window, text="Cancel", border_width=0, command=self.subject_cancel_func)
            self.edit_cancel_button.pack(pady=10,side="right", padx=20, expand=True)

        def forget_subject_name_page():
            self.tip_label.pack_forget()
            self.detail_frame.pack_forget()
            self.edit_save_button.pack_forget()
            self.edit_cancel_button.pack_forget()

        def subject_save_func():
            def exist(topic):
                if topic in self.subjects_list:
                    Storage.change_subject_name(self.current_subject_name_var.get(), self.new_subject_name_var.get())
                    self.subjects_list = Storage.subject_list()
                    self.subject_cancel_func()
                elif topic not in self.subjects_list:
                    ques = tk.messagebox.showinfo(title="Topic Existed", message="It is noticed that this topic doesn't exist. Please, change the subject name?")
            
            #Ensuring the time is a valid time
            self.valid_subject_bool = True

            subject = self.new_subject_name_var.get()

            try:
                if subject.isidentifier() == False:
                    raise Exception("This name cannot be used")
            except:
                self.valid_subject_bool = False
                tk.messagebox.showerror(title="Invalid Subject Format", message="Sorry, this subject name cannot be used. Please, use a one word name for your subject that doesn't contain symbols")

            def same_subjects():
                if self.current_subject_name_var.get() == self.new_subject_name_var.get():
                    tk.messagebox.showerror(title="Invalid Subject Input", message="Sorry but both subject's name cannot be the same")
                else:
                    exist(self.current_subject_name_var.get())

            if self.valid_subject_bool == True: 
                same_subjects()

        def subject_cancel_func():
            self.forget_subject_details_page()
            self.title_or_question()

        def change_subject_details_page():
            self.forget_title_or_question()

            #Tip Label
            self.tip_label = ctk.CTkLabel(self.editor_window, text="Click any of the details you wish to change and save it", font=("Cosmic Sans MS",24))
            self.tip_label.pack(pady=10)

            #Details frame: Contains the ssubject's title, time and marks
            self.detail_frame = ctk.CTkFrame(self.editor_window, border_width=0, fg_color="#c3c3c3")
            self.detail_frame.pack(pady=20, fill="both")

            #Naming entry: This give the name of the subject that is to be changed
            self.subject_name_var = tk.StringVar(value="Subject") #This value is for testing
            self.subject_name = ctk.CTkEntry(self.detail_frame, border_width=0, corner_radius=10, width=200, justify="center", textvariable=self.subject_name_var)
            self.subject_name.pack(padx=10,side="left", fill="both", expand=True)

            #Naming entry: This give the name of the subject that is to be changed
            self.hours = "01" #This value is for testing
            self.minutes = "00" #This value is for testing
            self.seconds = "00" #This value is for testing
            self.time_var = tk.StringVar(value="Time") #This value is for testing
            self.time_number = ctk.CTkEntry(self.detail_frame, border_width=0, corner_radius=10, width=200, justify="center", textvariable=self.time_var)
            self.time_number.pack(padx=10, side="left", fill="both", expand=True)

            #Naming entry: This give the name of the subject that is to be changed
            self.marks_var = tk.StringVar(value="Marks")
            self.marks_number = ctk.CTkEntry(self.detail_frame, border_width=0, corner_radius=10, width=200, justify="center", textvariable=self.marks_var)
            self.marks_number.pack(padx=10,side="left", fill="both", expand=True)

            #Save and Exit Button
            self.edit_save_button = ctk.CTkButton(self.editor_window, text="Save", border_width=0, command=self.detail_save_func)
            self.edit_save_button.pack(side="left", padx=20, pady=20, expand=True)

            #Cancel Button
            self.edit_cancel_button = ctk.CTkButton(self.editor_window, text="Cancel", border_width=0, command=self.detail_cancel_func)
            self.edit_cancel_button.pack(pady=10,side="right", padx=20, expand=True)

        def forget_subject_details_page():
            self.tip_label.pack_forget()
            self.detail_frame.pack_forget()
            self.edit_save_button.pack_forget()
            self.edit_cancel_button.pack_forget()
        
        def detail_save_func():
            self.valid_time()
            self.valid_marks()

            if self.valid_time_bool == True and self.valid_marks_bool == True:
                def exist(topic):
                    if topic in self.subjects_list:
                        #Storing-Backend
                        Storage.change_subject_details(self.subject_name_var.get(), self.time_var.get(), self.marks_var.get())
                        self.detail_cancel_func()
                        
                    elif topic not in self.subjects_list:
                        ques = tk.messagebox.showinfo(title="Topic Existed", message="It is noticed that this topic doesn't exist. Please, change the subject name?")
                exist(self.subject_name_var.get())
        
        def detail_cancel_func():
            self.forget_subject_details_page()
            self.title_or_question()
        
        def edit_question_info():
            self.forget_treeview()
            self.question_info()

            #Removing the detail of the subject(name, time and marks) and also the question number label as it is not required
            self.detail_frame.pack_forget()

            #Changing the content of the title from (add subject name, time and marks) to question number as the previous title(add a subject title, time and marks respectively) will be confusing as the stage
            self.title.configure(text=f"Question {self.question_number}")

            #Removing the save button as it is not required
            self.save_button.pack_forget()

            #Implementing a function to the buttons
            self.continue_button.configure(command=self.edit_question_info_continue_func)
            self.cancel_button.configure(command=self.edit_question_info_cancel_func)

        def edit_question_info_continue_func():
            def finished_func():
                if self.add_question_choice == "none":
                    self.question_option_filled([self.forget_question_page, self.edit_question_page])
                    
                    Storage.change_question(self.subject, self.storage_questions)
                    Storage.change_option_type(self.subject, self.storage_option_type)
                    if self.option_menu_variable.get() == "Options":
                        Storage.change_option(self.subject, self.storage_options)
                    Storage.change_answer(self.subject,self.storage_answers)
                
                elif self.add_question_choice == "before":
                    self.question_option_filled([self.forget_question_page, self.edit_question_page])
                    print(self.question_number-1, self.storage_questions,self.storage_answers, self.storage_option_type)
                    Storage.add_before(self.subject, self.question_number-1, question=self.storage_questions, option_type=self.storage_option_type, option=self.storage_options, answer=self.storage_answers)
                
                elif self.add_question_choice == "after":
                    self.question_option_filled([self.forget_question_page, self.edit_question_page])
                    print(self.question_number-2, self.storage_questions,self.storage_answers, self.storage_option_type)
                    Storage.add_after(self.subject, self.question_number-2, question=self.storage_questions, option_type=self.storage_option_type, option=self.storage_options, answer=self.storage_answers)

            def cancel_func():
                self.forget_question_page()
                self.question_info()

                #Removing the detail of the subject(name, time and marks) and also the question number label as it is not required
                self.detail_frame.pack_forget()

                #Changing the content of the title from (add subject name, time and marks) to question number as the previous title(add a subject title, time and marks respectively) will be confusing as the stage
                self.title.configure(text=f"Question {self.question_number}")

                #Removing the save button as it is useless here
                self.save_button.pack_forget()

                #Implementing a function to the buttons
                self.continue_button.configure(command=self.edit_question_info_continue_func)
                self.cancel_button.configure(command=self.edit_question_info_cancel_func)

            #Clearing the page
            self.forget_question_info()
            
            #Going to the page that will allow the user to input the question, options and answer
            if self.option_menu_variable.get() == "Options":
                self.question_widget()
                self.option_question_widget()

            elif self.option_menu_variable.get() == "Without Options":
                self.question_widget()
                self.without_option_question_widget()

            #Removing the Continue Button2 as it is useless here
            self.continue_button2.pack_forget()
            
            #Implementing functions to the buttons
            self.finished_button.configure(command=finished_func)
            self.cancel_button2.configure(command=cancel_func)
        
        def edit_question_info_cancel_func():
            self.forget_question_info()
            self.treeview()

        def edit_question_page():
            self.forget_title_or_question()
            self.treeview()
        
        def treeview():
            #Creating a treeview
            self.table = ttk.Treeview(self.editor_window, column=("Question No","Choice"), show="headings")
            self.table.pack(expand=True, fill="both")

            #Centering the text
            self.table.column("Question No",anchor="center")
            self.table.column("Choice",anchor="center")

            #Changing the font and colour
            style = ttk.Style()
            style.configure("Treeview", background="#c3c3c3")
            style.configure("Treeview.Heading", font=("Cosmic Sans MS", 14))
            style.configure("Treeview", font=("Cosmic Sans MS", 14))

            #Giving th treeview a heading
            self.table.heading("Question No",text="Question No")
            self.table.heading("Choice",text="Choice")

            #Inserting question and its choice
            for _ in range(0,Storage.get_questions(self.subject, "length")):
                __ = _ + 1
                self.table.insert(parent="", index=_, values=(__, Storage.get_option_type(self.subject)[_- 1]))

            #Treeview scrollbar
            self.scrollbar = ttk.Scrollbar(self.editor_window, orient="vertical", command=self.table.yview)
            self.table.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.place(relx=1,rely=0, relheight=1,anchor="ne")

            #Implementing a functionality when a question is double clicked
            self.table.bind("<Double -1>", self.table_clicked)
            #Adding a tip label
            self.treeview_label = ctk.CTkLabel(self.editor_window, text="Double click on a question to change it")
            self.treeview_label.pack()

            #cancel
            self.treeview_cancel_button = ctk.CTkButton(self.editor_window, text="Cancel", border_width=0, command=self.treeview_cancel_func)
            self.treeview_cancel_button.pack()
        
        def table_clicked(event):
            #Getting the question no that was clicked
            self.question_number = self.table.item(self.table.selection()[0])["values"][0]
            
            if self.add_question_choice == "before":
                self.edit_question_info()    
            
            elif self.add_question_choice == "after":
                self.question_number+=1
                self.edit_question_info()

            elif self.add_question_choice == "none":
                #Getting the question no that was clicked
                self.question_number = self.table.item(self.table.selection()[0])["values"][0]

                self.edit_question_info()
            
        def treeview_cancel_func():
            self.forget_treeview()
            self.title_or_question()
        
        def forget_treeview():
            self.table.pack_forget()
            self.treeview_label.pack_forget()
            self.treeview_cancel_button.pack_forget()
            self.scrollbar.place_forget()

        def add_question(choice):
            self.forget_title_or_question()
            self.treeview()

            #This variable tells whether the user picked before, after or the question itself
            self.add_question_choice = choice
    
        def delete_question_page():
            self.forget_title_or_question()
            self.treeview()

            #Changing the functionality of the treeview binding
            self.table.bind("<Double -1>", delete_question_page_func)
            
        def delete_question_page_func(event):
            #Getting the question no that was clicked
            self.question_number = self.table.item(self.table.selection()[0])["values"][0]

            Storage.delete_question(self.subject, self.question_number)

            #Ensuring the message box sits above the window
            self.editor_window.attributes("-topmost", False)
            
            #Asking the user if they actually want to delete the question
            tk.messagebox.askokcancel(title="Delete Question", message=f"Do you wish to delete question {self.question_number}")

            #Ensuring the message box sits above the window once again
            self.editor_window.attributes("-topmost", True)
        
        def question_option_filled(func):
            #Determning if the question widget is filled with a question
            if self.question.get("0.0","end") == "\n":
                self.question_filled = False
            elif self.question.get("0.0","end") != "\n":
                self.question_filled = True

            #Determing if the options are filled
            if self.option_menu_variable.get() == "Options":
                for _ in [self.option1, self.option2, self.option3, self.option4]:
                    if _.get() == "":
                        self.right_answer_picked == False
                    elif _.get() != "":
                        self.right_answer_picked == True

            #Determing if the answer box is filled
            elif self.option_menu_variable.get() == "Without Options":
                if self.answer.get("0.0","end") == "\n":
                    self.right_answer_picked = False
                elif self.answer.get("0.0","end") != "\n":
                    self.right_answer_picked = True


            #Running the program as long as the required conditions are attained
            if self.right_answer_picked == True and self.question_filled == True:
                self.record()

                #Changing the question number to indicate it is the next question 
                self.question_number+=1
                
                for _ in func:
                    _()
            
            #This elif block runs if the user doesn't fill all the required spaces
            elif self.right_answer_picked == False or self.question_filled == False:
                #Allowing this message to be displayed above the window
                self.editor_window.attributes("-topmost", False)
                
                #Displaying a message telling the user to fill in the unfilled spaces
                tk.messagebox.showinfo("Empty Textbox/Unselected Answer", "Please fill in all the necessary details in the textbox provided in the window. Perhaps you forgot to double click/right click on an option to select a right answer")
                
                #Puting the message as the top window 
                self.editor_window.attributes("-topmost", True)

        def valid_subject():
            #Ensuring the time is a valid time
            self.valid_subject_bool = True

            subject = self.subject_name_var.get()

            try:
                if subject.isidentifier() == False:
                    raise Exception("This name cannot be used")
            except:
                self.valid_subject_bool = False
                tk.messagebox.showerror(title="Invalid Subject Format", message="Sorry, this subject name cannot be used. Please, use a one word name for your subject that doesn't contain symbols")

        def valid_time():
            #Ensuring the time is a valid time
            self.valid_time_bool = True

            time = self.time_var.get()

            splited = time.split(":")

            try:
                hours = int(splited[0])
                minutes = int(splited[1])
                seconds = int(splited[2])

                if len(splited) != 3:
                    raise Exception("Invalid Time Format")
                if ((hours >= 0 and hours <= 24) and (minutes >= 0 and minutes <= 60) and (seconds >= 0 and seconds <= 60)) == False:
                    raise Exception("Invalid Time Format")
            except:
                self.valid_time_bool = False
                tk.messagebox.showerror(title="Invalid Time Format", message="Sorry, your time format is invalid, please insert a proper time format")

        def valid_marks():
            #Ensuring the user input marks that is an integer
            self.valid_marks_bool = True
            marks = self.marks_var.get()

            try:
                marks = int(marks)
            except:
                self.valid_marks_bool = False
                tk.messagebox.showerror(title="Invalid Number of Marks", message="The number of marks is invalid. Please enter a valid number of marks")

        def record():
            self.storage_option_type.update({f"Question {self.question_number}":self.option_menu_variable.get()})
            self.storage_questions.update({f"Question {self.question_number}":self.question.get("0.0","end-1c")})
            if self.option_menu_variable.get() == "Options":
                self.storage_options.update({f"Question {self.question_number}":[self.option1.get(), self.option2.get(), self.option3.get(), self.option4.get()]})
                for _ in [self.option1, self.option2, self.option3, self.option4]:
                    if _.cget("fg_color") == "#ADD8E6":
                        self.answer_picked = _.get()
                        self.storage_answers.update({f"Question {self.question_number}": self.answer_picked})
            elif self.option_menu_variable.get() == "Without Options":
                self.storage_answers.update({f"Question {self.question_number}": self.answer.get("0.0", "end-1c")})
        
        #Creating a method for each function, making them accessable to all classes
        self.disable_editor_buttons = disable_editor_buttons
        self.editor_window_func = editor_window_func
        self.enable_again = enable_again
        #<<<<<<<<<<<<<<<<<<<<--------------Search and Delete------------->>>>>>>>>>>>>>>
        self.search_delete = search_delete
        self.search_delete_checker = search_delete_checker
        self.search_delete_cancel_func = search_delete_cancel_func
        #<<<<<<<<<<<<<<<<<<------------------Add-------------------------->>>>>>>>>>>>>>
        self.question_info = question_info
        self.forget_question_info = forget_question_info
        self.question_widget = question_widget
        self.option_question_widget = option_question_widget
        self.without_option_question_widget = without_option_question_widget
        self.forget_question_page = forget_question_page
        self.display_question_info_again = display_question_info_again
        #<<<<<<<<<<<<<<<<<<------------------Edit-------------------------->>>>>>>>>>>>>>
        self.edit_subject_list = edit_subject_list
        self.edit_subjects_clicked = edit_subjects_clicked
        self.forget_edit_subject_list = forget_edit_subject_list
        self.title_or_question = title_or_question
        self.title_or_question_cancel_func = title_or_question_cancel_func
        self.forget_title_or_question = forget_title_or_question
        self.change_subject_name_page = change_subject_name_page
        self.forget_subject_name_page = forget_subject_name_page
        self.subject_save_func = subject_save_func
        self.subject_cancel_func = subject_cancel_func
        self.change_subject_details_page = change_subject_details_page
        self.detail_save_func = detail_save_func
        self.detail_cancel_func = detail_cancel_func
        self.forget_subject_details_page = forget_subject_details_page
        self.edit_question_page = edit_question_page
        self.edit_question_info = edit_question_info
        self.forget_treeview = forget_treeview
        self.treeview = treeview
        self.table_clicked = table_clicked
        self.edit_question_info_continue_func = edit_question_info_continue_func
        self.edit_question_info_cancel_func = edit_question_info_cancel_func
        self.treeview_cancel_func = treeview_cancel_func
        self.add_question = add_question
        self.delete_question_page = delete_question_page
        self.question_option_filled = question_option_filled
        self.valid_subject = valid_subject
        self.valid_time = valid_time
        self.valid_marks = valid_marks
        self.record = record

        #This function is ran when any of the editor buttons are clicked such as search, edit, etc
        def editor_clicked_func(button):
            #<<<<<<<<<<<<<<<<<<------------------Search-------------------------->>>>>>>>>>>>>>
            if button == "Search Button":
                self.search_delete()

                def search_ok():
                    self.search_delete_checker(self.search_delete_entry.get(),"Search")

                #Implementing function to the buttons
                self.search_delete_cancel.configure(command=self.search_delete_cancel_func)
                self.search_delete_ok.configure(command=search_ok)

            #<<<<<<<<<<<<<<<<<<------------------Add-------------------------->>>>>>>>>>>>>>
            elif button == "Add Button":
                #Reseting the question number
                self.question_number = 1

                def info():
                    def exist(topic):
                        if topic not in self.subjects_list:
                            question_page()

                        elif topic in self.subjects_list:
                            ques = tk.messagebox.askyesno(title="Topic Existed", message="It is noticed that this topic already exist. Do you wish to coninue from where you left off")
                            if ques == True:
                                self.check_topic = True

                                #Disabling the subject title entry and changing the text_color to grey
                                self.subject_name.configure(state="disabled", text_color="#d1d1d1")
                                self.time_number.configure(state="disabled", text_color="#d1d1d1")
                                self.marks_number.configure(state="disabled", text_color="#d1d1d1")
                                
                                self.question_number = int(Storage.last_question(self.subject_name_var.get())) + 1
                                self.question_number_label.configure(text=f"Question: {self.question_number} -->")
                            else:
                                pass

                    #Continue function
                    def continue_func():
                        self.valid_subject()
                        self.valid_time()
                        self.valid_marks()

                        if self.valid_subject_bool == True and self.valid_time_bool == True and self.valid_marks_bool == True:
                            if self.check_topic == False:
                                exist(self.subject_name_var.get())
                            elif self.check_topic == True:
                                question_page()

                    #Save and Exit function
                    def save_func():
                        if self.subject_name_var.get() not in self.subjects_list:
                            Storage.add_subject(self.subject_name_var.get())
                        self.storage_details.update({"name":self.subject_name_var.get(), "time":self.time_var.get(), "marks":self.marks_var.get()})
                        #Storing the questions, option type, options, etc
                        Storage.add_details(self.subject_name_var.get(), self.storage_details)
                        Storage.add_option_type(self.subject_name_var.get(), self.storage_option_type)
                        Storage.add_questions(self.subject_name_var.get(), self.storage_questions)
                        Storage.add_options(self.subject_name_var.get(), self.storage_options)
                        Storage.add_answers(self.subject_name_var.get(), self.storage_answers)
                        
                        #Window closing event: Runs a function to close the window
                        self.editor_window.destroy()
                        self.enable_again()

                    def title_or_question_cancel_func():
                        self.forget_title_or_question()
                        self.question_info()

                        #Implementing the commands when the buttons are clicked
                        self.continue_button.configure(command=continue_func)
                        self.save_button.configure(command=save_func)
                        self.cancel_button.configure(command=cancel_func)

                        #Disabling the subject title entry and changing the text_color to grey
                        self.subject_name.configure(state="disabled", text_color="#d1d1d1")
                        self.time_number.configure(state="disabled", text_color="#d1d1d1")
                        self.marks_number.configure(state="disabled", text_color="#d1d1d1")

                    #Cancel function
                    def cancel_func():
                        save_or_not = tk.messagebox.askyesno(title="Save", message="Are you sure you don't want to save?")
                        
                        if save_or_not == True: 
                            #Window closing event: Runs a function when the window is closed
                            self.editor_window.destroy()
                            self.enable_again()

                    #Creating the Page
                    self.disable_editor_buttons()
                    self.editor_window_func()
                    self.question_info()

                    #Adding a title
                    self.editor_window.title("Add")

                    #Removing the save/exit and edit button at the first sight of viewing the page
                    self.save_button.pack_forget()

                    #Implementing the commands when the buttons are clicked
                    self.continue_button.configure(command=continue_func)
                    self.save_button.configure(command=save_func)
                    self.cancel_button.configure(command=cancel_func)

                def question_page():
                    #Clearing the page
                    self.forget_question_info()

                    #Continue function
                    def continue_func2():
                        #Displaying the previous page(question_info)
                        self.question_option_filled([cancel_func2])

                        if self.question_number != 1:
                            #Disabling the subject title entry and changing the text_color to grey
                            self.subject_name.configure(state="disabled", text_color="#d1d1d1")
                            self.time_number.configure(state="disabled", text_color="#d1d1d1")
                            self.marks_number.configure(state="disabled", text_color="#d1d1d1")

                    #Finished Function
                    def finished_func():        
                        if self.subject_name_var.get() not in self.subjects_list:
                            Storage.add_subject(self.subject_name_var.get())
                            
                        #Recording the last question
                        self.storage_details.update({"name":self.subject_name_var.get(), "time":self.time_var.get(), "marks":self.marks_var.get()})
                        self.record()

                        #Storing the questions, option type, options, etc
                        Storage.add_details(self.subject_name_var.get(), self.storage_details)
                        Storage.add_option_type(self.subject_name_var.get(), self.storage_option_type)
                        Storage.add_questions(self.subject_name_var.get(), self.storage_questions)
                        Storage.add_options(self.subject_name_var.get(), self.storage_options)
                        Storage.add_answers(self.subject_name_var.get(), self.storage_answers)

                        self.question_option_filled([self.editor_window.destroy, self.enable_again])

                    #Cancel Function
                    def cancel_func2():
                        self.forget_question_page()
                        self.display_question_info_again()

                        #Changing the question number 
                        self.question_number_label.configure(text=f"Question: {self.question_number}-->")

                        if self.question_number == 1:
                            self.save_button.pack_forget()

                    if self.option_menu_variable.get() == "Options":
                        self.question_widget()
                        self.option_question_widget()
                        
                    elif self.option_menu_variable.get() == "Without Options":
                        self.question_widget()
                        self.without_option_question_widget()

                    #Implementing the commands when the buttons are clicked
                    self.continue_button2.configure(command=continue_func2)
                    self.finished_button.configure(command=finished_func)
                    self.cancel_button2.configure(command=cancel_func2)       

                info()
            
            #<<<<<<<<<<<<<<<<<<------------------Edit-------------------------->>>>>>>>>>>>>>
            elif button == "Edit Button":
                def edit_window():
                    self.disable_editor_buttons()
                    self.editor_window_func()
                    self.edit_subject_list()

                    #Adding a title
                    self.editor_window.title("Edit")
                
                edit_window()
                      
            #<<<<<<<<<<<<<<<<<<------------------Delete-------------------------->>>>>>>>>>>>>>
            elif button == "Delete Button": 
                self.search_delete()

                self.editor_window.title("Delete")

                def delete_func():
                    self.search_delete_checker(self.search_delete_entry.get(),"Delete")

                #Implementing function to the buttons
                self.search_delete_cancel.configure(command=self.search_delete_cancel_func)
                self.search_delete_ok.configure(command=delete_func)

        def display_editor():
            #Editor frame: Contains the search, add, edit, and delete button
            self.editor_frame = ctk.CTkFrame(self.scroll_frame)
            self.editor_frame.pack(fill="x")

            #These are images in the search, add, edit and delete button
            self.search_image = ctk.CTkImage(light_image=Image.open("Search.jpg"),size=(30,30))
            self.add_image = ctk.CTkImage(light_image=Image.open("Add.png"),size=(30,30))
            self.edit_image = ctk.CTkImage(light_image=Image.open("Edit.png"),size=(30,30))
            self.delete_image = ctk.CTkImage(light_image=Image.open("Delete.png"),size=(30,30))

            #These are the editor button. These are kept in the editor frame
            self.search_button = ctk.CTkButton(self.editor_frame,text="",anchor="center",width=30,height=30,border_width=0,image=self.search_image, corner_radius=0,hover_color="#01a9f3", command=lambda: editor_clicked_func("Search Button"))
            self.add_button = ctk.CTkButton(self.editor_frame,text="",anchor="center",width=30,height=30,border_width=0,image=self.add_image, corner_radius=0,hover_color="#01a9f3", command=lambda: editor_clicked_func("Add Button"))
            self.edit_button = ctk.CTkButton(self.editor_frame,text="",anchor="center",width=30,height=30,border_width=0,image=self.edit_image, corner_radius=0,hover_color="#01a9f3", command=lambda: editor_clicked_func("Edit Button"))
            self.delete_button = ctk.CTkButton(self.editor_frame,text="",anchor="center",width=30,height=30,border_width=0,image=self.delete_image, corner_radius=0,hover_color="#01a9f3", command=lambda: editor_clicked_func("Delete Button"))

            #Displaing the editor buttons(search,add,edit,delete)
            self.search_button.pack(expand=True,fill="x",side="left")
            self.add_button.pack(expand=True,fill="x",side="left")
            self.edit_button.pack(expand=True,fill="x",side="left")
            self.delete_button.pack(expand=True,fill="x",side="left")

            #This variable tells if the instruction page has been displayed or not
            self.about_to_start_present = False

            #This function makes the About to Start page appear and the Welcome page to disappear
            global about_to_start_appear
            def about_to_start_appear(sub):
                #Storing which subjects button has been pressed
                self.subject_choosen = sub

                self.app.tophorizontalframe.subject_variable.set(self.subject_choosen)
                self.Question_frame.subject_choosen = self.subject_choosen

                if self.about_to_start_present == False:
                    self.Question_frame.about_to_start()
                    self.about_to_start_present = True
                elif self.about_to_start_present == True:
                    #Removing the question frame (about to start page)
                    self.Question_frame.new_instruction_label.pack_forget()
                    self.Question_frame.arrow_label.pack_forget()
                    self.Question_frame.starting_button.pack_forget()

                    #Bringing the question frame (about to start page)
                    self.Question_frame.about_to_start()

                    #Doing this does absolutly nothing other than update what subject is to be run
                    #And letting the user see that the subject they clicked loaded
        
        self.display_editor = display_editor
        self.display_editor()

        def display_subjects():
            self.subjects_list = Storage.subject_list()

            self.subject_list_widget = [
                f"{self.subjects_list[_]} = ctk.CTkButton(self.scroll_frame, text=f'{self.subjects_list[_]}',fg_color='#d3d3de',width=200,height=50,corner_radius=10,border_width=2,hover_color='#b3b3be',command=lambda:about_to_start_appear('{self.subjects_list[_]}'))" 
                for _ in range(len(self.subjects_list))
                ]
            self.subject_widget_packed = [f"{self.subjects_list[_]}.pack(expand=True,fill='x',padx=10,pady=10)" for _ in range(len(self.subjects_list))]
            #self.disable_subjects = [f"{self.subjects_list[_]}.configure(state='disabled')" for _ in range(len(self.subjects_list))]
            #self.subject_pack_forget = [f"{self.subjects_list[_]}.pack_forget()" for _ in range(len(self.subjects_list))]
            #elf.global_subject = [f"global {self.subjects_list[_]}" for _ in range(len(self.subjects_list))]
            #Executing each statement
            for _ in self.subject_list_widget:
                exec(_)

            for _ in self.subject_widget_packed:
                exec(_)

        self.display_subjects = display_subjects
        self.display_subjects()

        #Initializing the QuestionFrame: This would display the "question_frame"
        self.Question_frame = QuestionFrame(self.app)
        self.Question_frame.welcome()

#Note: This class has to be created last because it has to inherit the class MenuFrame and QuestionFrame
#If it wasn't done last, trying the inherit the MenuFrame and Question Frame classes will return-
#undefined classes as an error.
#Top horizontal Frame Widget(contains subject, time, score widgets)
class TopHorizontalFrame(MenuFrame, QuestionFrame):
        def __init__(self, app):
            self.app = app

            self.horizontal_frame()
            self.menu_button()
            self.subject_widget()
            self.time_widget()
            self.score_widget()

            #Inheriting the attributes of the MenuFrame and QuestionFrame
            super().__init__(app)
        
        def horizontal_frame(self):
            #Top horizontal Frame(contains subject, time, score labels)
            self.horizontal_frame = ctk.CTkFrame(self.app, fg_color="#c3c3c3", border_width=2)
            self.horizontal_frame.grid(row=0,column=0, columnspan=21, sticky="nsew")

        def menu_button(self):
            #This variable tells if either the Menu Frame is displayed or not
            self.menu_present = False

            #Menu Function: This function makes the menu frame appear and disappear
            def menu_appear():
                if self.menu_present == False: 
                    #Shrinking the question frame when the Menu Button is clicked to make-
                    #space for the Menu frame
                    self.Question_frame.question_frame.grid(column=5,columnspan=16)
                    
                    #Placing the Menu frame
                    self.menu_frame.grid(row=1, column=0, rowspan=21, columnspan=5,sticky="nsew") #Displaying frame
                    self.menu_present = True

                elif self.menu_present == True:
                    #Removing the Menu frame to make space for the Question frame to expand
                    self.menu_frame.grid_forget()

                    #Expanding the Question frame
                    self.Question_frame.question_frame.grid(column=0,columnspan=21)
                    self.menu_present = False

            #Menu Button
            self.menu_button = ctk.CTkButton(self.horizontal_frame, text="Menu",width=165,height=85,corner_radius=10,command=menu_appear) 
            self.menu_button.pack(side="left", padx=10)

        def subject_widget(self):
            #subject_label: Note: This label is actually an entry widget. 
            #This is done because a label doesn't have the feature of a corner_radius but an entry does,
            #So using corner_radius makes it look better than just having a staight corner
            self.subject = "Maths"
            self.subject_variable = tk.StringVar(value = f"Subject: {self.subject}")
            self.subject_label= ctk.CTkEntry(self.horizontal_frame, textvariable=self.subject_variable, width=250,height=65, corner_radius=100,border_width=3, justify="center",state="disabled")
            self.subject_label.pack(expand=True, side="left")

        def time_widget(self):
            #time_label: Note: This label is actually an entry widget. 
            #This is done because a label doesn't have the feature of a corner_radius but an entry does,
            #So using corner_radius makes it look better than just having a staight corner
            self.time = 60
            self.time_variable = tk.StringVar(value = f"Time: {self.time} mins")
            self.time_label= ctk.CTkEntry(self.horizontal_frame, textvariable=self.time_variable, width=250,height=65, corner_radius=100,border_width=3, justify="center",state="disabled")
            self.time_label.pack(expand=True, side="left")

        def score_widget(self):
            #score_label: Note: This label is actually an entry widget. 
            #This is done because a label doesn't have the feature of a corner_radius but an entry does,
            #So using corner_radius makes it look better than just having a staight corner
            self.marks = 100
            self.score_variable = tk.IntVar(value = f"Marks: {self.marks}")
            self.score_label= ctk.CTkEntry(self.horizontal_frame, textvariable=self.score_variable, width=250,height=65, corner_radius=100,border_width=3, justify="center",state="disabled")
            self.score_label.pack(expand=True, side="left")

        def next_button(self):
            #This is an image of an arrow pointing right seen in the button on the top right page
            self.next_image = ctk.CTkImage(light_image = Image.open("Forward.jpg"), size=(30,30))

            #Next Page button
            self.next_button = ctk.CTkButton(self.horizontal_frame, text="", image=self.next_image,width=20,height=20,corner_radius=20,hover_color="#01a9f3")
            self.next_page_button.pack(expand=True, side="left")
Page()

"""Further documentation is described in the README files"""
