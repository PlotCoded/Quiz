import os
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image
import random
from EditorFiles import Search, Add, Edit, Delete, ExFunc
import pandas
from ast import literal_eval

#Applying the theme of the window
ctk.set_default_color_theme("Storage\\Theme.json")

#This class is the main window of the application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.window_up = False
        
        #Adding a title
        self.title("Quiz")

        #Getting maximum the size of the screen
        self.width = self.winfo_screenwidth() #Getting the user screen width
        self.height = self.winfo_screenheight()  #Getting the user screen height

        #Setting the width and height of the app to max
        self.geometry(f"{self.width}x{self.height}+{0}+{0}") 

        #Creating grids for widgets placements
        self.columnconfigure(tuple(range(0,21)),weight=1)
        self.rowconfigure(tuple(range(0,21)),weight=1)

        #Initializing imported classes
        self.search = Search.Search(self)
        self.add = Add.Add(self)
        self.edit = Edit.Edit(self)
        self.delete = Delete.Delete(self)

        #Initializing external classes
        self.header = Header(self)
        self.header.header()

        self.question_page = QuestionPage(self)
        self.question_page.welcome()

        self.menu = Menu(self)
        self.menu.menu()

        self.mainloop()

class Header:
    def __init__(self, app):
        self.app = app

    def header(self):
        def animation(): # This function allows the menu to be opened and closed after pressing the button
            if self.app.menu.menuOpened == True:
                self.app.menu.scroll_frame.grid_forget()
                self.app.question_page.frame.grid(row=1,column=0, rowspan=21,columnspan=21, sticky="nsew")
                self.app.menu.menuOpened = False
            else:
                self.app.menu.scroll_frame.grid(row=1, column=0, rowspan=21, columnspan=5,sticky="nsew")
                self.app.question_page.frame.grid(row=1,column=5, rowspan=21,columnspan=16,sticky="nsew")
                self.app.menu.menuOpened = True

        #Header scroll_frame
        self.scroll_frame = ctk.CTkFrame(self.app)
        self.scroll_frame.grid(row=0,column=0, columnspan=21, sticky="nsew")

        #Menu Button
        self.menu_button = ctk.CTkButton(self.scroll_frame, text="Menu",width=165,height=85,corner_radius=10, command=animation)
        self.menu_button.pack(side="left", padx=10)

        #Creating the subject label
        #Note: This is an entry acting as a label because labels don't have a border
        self.subject = "None"
        self.subject_var = tk.StringVar(value = f"Topic: {self.subject}")
        self.topic_label= ctk.CTkEntry(self.scroll_frame, textvariable=self.subject_var, width=250,height=65, corner_radius=100,border_width=3, justify="center",state="disabled")
        self.topic_label.pack(expand=True, side="left")

        #Creating the time label
        #Note: This is an entry acting as a label because labels don't have a border
        self.time = "00:00:00"
        self.time_var = tk.StringVar(value = f"Time: {self.time}")
        self.time_label= ctk.CTkEntry(self.scroll_frame, textvariable=self.time_var, width=250,height=65, corner_radius=100,border_width=3, justify="center",state="disabled")
        self.time_label.pack(expand=True, side="left")

        #Creating the marks label
        #Note: This is an entry acting as a label because labels don't have a border        
        self.marks = 0
        self.score_var = tk.StringVar(value = f"Marks: {self.marks}")
        self.score_label= ctk.CTkEntry(self.scroll_frame, textvariable=self.score_var, width=250, height=65, corner_radius=100,border_width=3, justify="center",state="disabled")
        self.score_label.pack(expand=True, side="left")

class Menu:
    def __init__(self, app):
        self.app = app

    def menu(self):
        #This variable controls the menu opening and closing. If False, opens up, else if True, closes up
        self.menuOpened = False

        #Scroll Frame: Contains the "Subject label", "search", "add","edit","delete" button and subjects
        self.scroll_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0, border_width=1, fg_color="#d3d3d3",orientation="vertical")
        
        #Label
        self.label = ctk.CTkLabel(self.scroll_frame, text="Topics",width=200,height=50,fg_color="#a3a3a3")
        self.label.pack(fill="x",pady=10,padx=10)

        #Editor frame: Contains the "search", "add", "edit", and "delete" button needed for editing
        self.editor_frame = ctk.CTkFrame(self.scroll_frame)
        self.editor_frame.pack(fill="x")

        #These are images in the search, add, edit and delete button
        self.search_image = ctk.CTkImage(light_image=Image.open("Pictures\\Search.jpg"),size=(30,30))
        self.add_image = ctk.CTkImage(light_image=Image.open("Pictures\\Add.png"),size=(30,30))
        self.edit_image = ctk.CTkImage(light_image=Image.open("Pictures\\Edit.png"),size=(30,30))
        self.delete_image = ctk.CTkImage(light_image=Image.open("Pictures\\Delete.png"),size=(30,30))

        #These are the editor button. These are kept in the editor frame
        self.search_button = ctk.CTkButton(self.editor_frame,text="",anchor="center",width=30,height=30,border_width=0,image=self.search_image, corner_radius=0,hover_color="#01a9f3", command=self.app.search.window)
        self.add_button = ctk.CTkButton(self.editor_frame,text="",anchor="center",width=30,height=30,border_width=0,image=self.add_image, corner_radius=0,hover_color="#01a9f3",command=self.app.add.detailsPage)
        self.edit_button = ctk.CTkButton(self.editor_frame,text="",anchor="center",width=30,height=30,border_width=0,image=self.edit_image, corner_radius=0,hover_color="#01a9f3",command=self.app.edit.mainWindow)
        self.delete_button = ctk.CTkButton(self.editor_frame,text="",anchor="center",width=30,height=30,border_width=0,image=self.delete_image, corner_radius=0,hover_color="#01a9f3",command=self.app.delete.window)

        #Displaying the editor buttons(search,add,edit,delete)
        self.search_button.pack(expand=True,fill="x",side="left")
        self.add_button.pack(expand=True,fill="x",side="left")
        self.edit_button.pack(expand=True,fill="x",side="left")
        self.delete_button.pack(expand=True,fill="x",side="left")

        # Getting the names of the topics
        filenames = os.listdir(r"C:\Users\hp\Documents\Quiz\Storage")

        # for file in filenames:
        #     if ".csv" in file:
        #         # Displaying the topic on the menu
        #         exec(f"self.{file[::-4]} = ctk.CTkButton(self.scroll_frame, text='{file[:-4]}', command=lambda: self.app.question_page.starting(f'self.{file[::-4]}') )")
        #         exec(f"self.{file[::-4]}.pack(pady=50)")

        self.buttons = {}  # store buttons so you can access them later

        # Displaying the new buttons
        for file in filenames:
            if file.endswith(".csv"):
                file_name = file[:-4]  # remove ".csv"
                # capture the current file_name in the lambda default
                call = lambda f=file_name: self.app.question_page.starting(f)
                button = ctk.CTkButton(self.scroll_frame, text=file_name, command=call)
                button.pack(pady=50)
                self.buttons[file_name] = button

class QuestionPage:
    def __init__(self, app):
        self.app = app
        
        self.finished_before = False

        #This frame contains the welcome instruction and tells to choose a topic from the menu
        self.frame = ctk.CTkFrame(self.app, border_width=1, fg_color="#e3e3e3")
        
        #Instruction label
        self.instruction = ctk.CTkLabel(self.frame, text="Please choose a topic listed \n after clicking the Menu button", font=("Comic Sans MS",42), width=200,height=50,fg_color="#e3e3e3")

        #New Instruction
        self.instruction.configure(text="Please answer the questions listed\n after clicking the button below")
        self.instruction.configure(font=("Comic Sans MS",48))

        #Arrow Image
        self.arrow = ctk.CTkImage(light_image = Image.open("Pictures\\Arrow.jpg"), size=(170,170))

        #arrow label
        self.arrow_label = ctk.CTkLabel(self.frame, text="", image=self.arrow)

        #Starting Button
        self.starting_button = ctk.CTkButton(self.frame, text="Start Here", width=225, height=105, command=self.start, corner_radius=10, font=("Comic Sans MS",40))

    def welcome(self):
        self.frame.grid(row=1, column=0, rowspan=21, columnspan=21,sticky="nsew")

        self.instruction.pack(expand=True, fill="both")

    def starting(self, topic_name):
        # Getting rid of all previous widgets
        if self.finished_before == True:
            self.congratulations.pack_forget()
            self.marks.pack_forget()

        self.topic_name = topic_name # Storing the topic name
        self.app.header.subject_var.set(value=f"Topic: {self.topic_name}")

        self.data = pandas.read_csv(fr"C:\Users\hp\Documents\Quiz\Storage\{self.topic_name}.csv")

        for column, items in self.data.items():
            if column == "Time":
                self.app.header.time_var.set(value=f"Time: {items[0]}")
            if column == "Marks":
                self.app.header.score_var.set(value=f"Marks: {items[0]}")
            break

        self.question_number = 0 # Needs to keep track on which question you are on

        # Updating widgets that needs to be updated

        # Ensuring the widgets doesn't get placed again and again
        self.instruction.pack_forget()
        self.arrow_label.pack_forget()
        self.starting_button.pack_forget()

        # Packing the widgets
        self.instruction.pack(expand=True)
        self.arrow_label.pack(expand=True)
        self.starting_button.pack(expand=True)

    def start(self):
        # Updating the question 
        self.question_number = 0

        # Questions
        self.questions = []
        # Options
        self.options = []
        #Answers
        self.answers = []
        # Option types
        self.option_types = []

        for column, items in self.data.items():
            if column == "Time":
                self.app.header.time_var.set(value=f"Time: {items[self.question_number]}")
            if column == "Marks":
                self.app.header.score_var.set(value=f"Marks: {items[self.question_number]}")
            if column == "Text Question":
                self.questions = items
            if column == "Options":
                self.options = items
            if column == "Answer":
                self.answers  = items
            if column == "Option Type":
                self.option_types = items

        self.answer_inserted = []
        self.questions = tuple(self.questions)
       
        __ = []
        for _ in self.options:
            __.append(tuple(literal_eval(_)))

        self.options = tuple(__)
        self.answers = tuple(self.answers)
        self.option_types = tuple(self.option_types)

        # Removing all previos widgets
        self.instruction.pack_forget()
        self.arrow_label.pack_forget()
        self.starting_button.pack_forget()

        def displayHintFunction():
            self.display_hint_window = ctk.CTkToplevel(self.app)
            self.display_hint_window.transient(self.app)
            self.display_hint_window.title("Hint")
            self.display_hint_window.geometry("600x200+300+50")

            # Displaying the hint in text format
            self.display_hint_label = ctk.CTkLabel(self.display_hint_window, text="This is the hint")

            # Displaying the hint in picture format
            # self.display_hint_file_name = "Pictures/Hint.png"

            for column, items in self.data.items():
                if column == "Hint":
                    self.display_hint_label = ctk.CTkLabel(self.display_hint_window, text="{items[question_number-1]}")
                            
            # self.display_hint_image = ctk.CTkImage(light_image=Image.open(self.display_hint_file_name), size=(600,200))
            # self.display_hint_image_label = ctk.CTkLabel(self.display_hint_window, text="", image=self.display_hint_image, width=600, height=200)

            # Displaying hint
            self.display_hint_label.pack()

        def nextFunction():
            print(self.question_number)
            print(self.options_variable.get())
            print(self.answers)
            self.answer_inserted.append(self.answers[ExFunc.getAnswerChoosenIndex(self,self.options_variable.get())])
            print(f"Answer to the question: {self.answers[self.question_number]}")
            print(f"Answer inserted: {self.answer_inserted[self.question_number]}")
            if self.question_number+1 == len(self.questions):
                self.finished()
            else:
                self.question_number = self.question_number + 1

                question = self.questions[self.question_number]
                options = self.options[self.question_number]

                self.text_label.insert("0.0",question)

                self.option_A_entry.delete(0,last_index=300)
                self.option_B_entry.delete(0,last_index=300)
                self.option_C_entry.delete(0,last_index=300)
                self.option_D_entry.delete(0,last_index=300)

                self.option_A_entry.insert(0,options[0])
                self.option_B_entry.insert(0,options[1])
                self.option_C_entry.insert(0,options[2])
                self.option_D_entry.insert(0,options[3])

        def viewSolutionsFunction():
            self.display_solutions_window = ctk.CTkToplevel(self.app)
            self.display_solutions_window.transient(self.app)
            self.display_solutions_window.title("Solution")
            self.display_solutions_window.geometry("600x200+300+50")

            # Displaying the hint in text format
            self.display_solutions_label = ctk.CTkLabel(self.display_solutions_window, text="This is the solution")

            # Displaying the hint in picture format
            self.display_solutions_file_name = "Pictures/Hint.png"
            self.display_solutions_image = ctk.CTkImage(light_image=Image.open(self.display_solutions_file_name), size=(600,200))
            self.display_solutions_image_label = ctk.CTkLabel(self.display_solutions_window, text="", image=self.display_solutions_image, width=600, height=200)

            # Displaying hint
            if False:
                self.display_solutions_image_label.pack()
            elif True:
                self.display_solutions_label.pack()

        # Hint/Header Frame
        self.hint_frame = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3", width=900, height=75)

        # Hint Button
        self.hint_button = ctk.CTkButton(self.hint_frame, text="View Hint", command=displayHintFunction)

        # Widgets that display the question_page
        # Image
        image_width = 900
        image_height = 400

        self.file_name = "Pictures/AddImage.jpg"
        self.image = ctk.CTkImage(light_image=Image.open(self.file_name), size=(image_width,image_height))
        self.image_label = ctk.CTkLabel(self.frame, text="", image=self.image, width=image_width, height=image_height)

        # Label
        self.text_label = ctk.CTkTextbox(self.frame, width=900, height=350, fg_color="#c3c3c3", wrap="word", border_width=4,)

        #Option frames
        self.option_frame1 = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3",height=70)

        self.option_frame2 = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3",height=70)

        #Options variable
        self.options_variable = tk.StringVar(value="A")

        #Options button(radio button) and their entries
        radio_button_width = 35
        radio_button_height = 35

        self.option_A_button = ctk.CTkRadioButton(self.option_frame1, corner_radius=10, radiobutton_width=radio_button_width, radiobutton_height=radio_button_height, variable=self.options_variable, value="A", text="")

        self.option_A_entry = ctk.CTkEntry(self.option_frame1, border_width=2, width=325, height=35, corner_radius=10,placeholder_text="Option A", placeholder_text_color="#b3b3b3", state="normal")

        self.option_B_button = ctk.CTkRadioButton(self.option_frame1, corner_radius=10, radiobutton_width=radio_button_width, radiobutton_height=radio_button_height, variable=self.options_variable, value="B", text="")

        self.option_B_entry = ctk.CTkEntry(self.option_frame1, border_width=2, width=325, height=35, corner_radius=10, placeholder_text="Option B", placeholder_text_color="#b3b3b3", state="normal")

        self.option_C_button = ctk.CTkRadioButton(self.option_frame2, corner_radius=10, radiobutton_width=radio_button_width, radiobutton_height=radio_button_height, variable=self.options_variable, value="C", text="")

        self.option_C_entry = ctk.CTkEntry(self.option_frame2, border_width=2, width=325, height=35, corner_radius=10, placeholder_text="Option C", placeholder_text_color="#b3b3b3", state="normal")

        self.option_D_button = ctk.CTkRadioButton(self.option_frame2, corner_radius=10, radiobutton_width=radio_button_width, radiobutton_height=radio_button_height, variable=self.options_variable, value="D", text="")

        self.option_D_entry = ctk.CTkEntry(self.option_frame2, border_width=2, width=325, height=35, corner_radius=10, placeholder_text="Option D", placeholder_text_color="#b3b3b3", state="normal")

        #Without Options Textbox
        self.without_options_textbox = ctk.CTkTextbox(self.frame, width=600, height=50, text_color="#00FF00")

        # Footer Frame
        self.footer_frame = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3")

        # Next Button
        self.next_button = ctk.CTkButton(self.footer_frame, text="Next", command=nextFunction)

        # Solutions Button: This button is only displayed when one has answered a question
        self.solutions_button = ctk.CTkButton(self.footer_frame, text="View Solutions", command=viewSolutionsFunction)

        # Displaying widgets
        self.hint_frame.pack(fill="x")
        self.hint_button.place(relx=0.75, rely=0.25)

        question = self.questions[self.question_number]
        options = self.options[self.question_number]

        if True:
            self.text_label.insert("0.0",question) # Inseting the question 
            self.text_label.pack(pady=10)
        else:
            self.image_label.pack(pady=10)

        if True:
            self.option_frame1.pack(fill="x", pady=3, padx=10)
            self.option_frame2.pack(fill="x",pady=3,padx=10)
            self.option_A_button.place(relx=0.15, rely=0.1)
            self.option_A_entry.place(relx=0.19,rely=0.1)
            self.option_B_button.place(relx=0.5,rely=0.1,)
            self.option_B_entry.place(relx=0.54,rely=0.1)
            self.option_C_button.place(relx=0.15,rely=0.1)
            self.option_C_entry.place(relx=0.19,rely=0.1)
            self.option_D_button.place(relx=0.5,rely=0.1)
            self.option_D_entry.place(relx=0.54,rely=0.1)

            # Inserting the options
            self.option_A_entry.insert(0,options[0])
            self.option_B_entry.insert(0,options[1])
            self.option_C_entry.insert(0,options[2])
            self.option_D_entry.insert(0,options[3])

        self.footer_frame.pack(fill="both")
        self.next_button.pack(side="left", padx=250)
        self.solutions_button.pack(side="right", padx=250)
    
    def finished(self):
        # Getting rid of previous widgets
        self.hint_frame.pack_forget()
        self.text_label.pack_forget()
        self.image_label.pack_forget()
        self.option_frame1.pack_forget()
        self.option_frame2.pack_forget()
        self.footer_frame.pack_forget()

        self.congratulations = ctk.CTkLabel(self.frame, text="Congratulations", font=("Comic Sans MS",42))

        # Marks info
        marks_gotten = 0
        total_marks = len(self.answers)

        for i in range(len(self.answer_inserted)):
            if str(self.answer_inserted[i]) == str(self.answers[i]):
                marks_gotten+=1

        percentage = (marks_gotten/total_marks)*100

        # Marks widget
        self.marks = ctk.CTkLabel(self.frame, text=f"You got a {marks_gotten} out of {total_marks} or {round (percentage,2)}%", font=("Comic Sans MS",42))

        # Displaying widgets
        self.congratulations.pack()
        self.marks.pack(expand=True)

        self.finished_before = True # Allowing the frame to be cleared of previous widgets allowing for a new topic

app = App()