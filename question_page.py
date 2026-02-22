import customtkinter as ctk
from PIL import Image
import pandas
from ast import literal_eval
import tkinter as tk
from EditorFiles import Search, Add, Edit, Delete, ExFunc

class QuestionPage:
    def __init__(self, app):
        self.app = app
        
        #This frame contains the welcome instruction and tells to choose a topic from the menu
        self.frame = ctk.CTkFrame(self.app, border_width=1, fg_color="#e3e3e3")
        
    def firstPageYouSee(self):
        # Displaying the page: It only has the instruction: "Please answer the questions listed after clicking the button below" at the beginning/at first
        self.frame.grid(row=1, column=0, rowspan=21, columnspan=21,sticky="nsew")

        # Displaying the instruction
        self.instruction = ctk.CTkLabel(self.frame, text="Please click a topic in the menu to get started", font=("Comic Sans MS",48), width=200,height=50,fg_color="#e3e3e3")
        self.instruction.pack(expand=True, fill="both")

    def topicClickedPage(self, topic_name): # Also essentially, the secnod page you see when you click on the question page (when you click a topic button)
        # Getting rid of all previous widgets
        if "congratulations" in self.__dict__.keys() and "marks" in self.__dict__.keys(): # When the question page is first initialised, these two variables aren't initialised along with it
            # It is only initialised when finished(self) has been called, thus checks if the variables has been initialised, if so, remove this widgets from the window
            self.congratulations.pack_forget()
            self.marks.pack_forget()

        # Changing the topic label in the header to the topic clicked/choosen
        self.app.header.subject_var.set(value=f"Topic: {topic_name}")

        # Getting all the stored data of the topic's file
        self.file = pandas.read_csv(fr"C:\Users\hp\Documents\Quiz\Storage\{topic_name}.csv")

        self.question_number = 1 # Needs to keep track on which question you are on

        # Ensuring the widgets doesn't get placed again and again if you clicked the topic multiple times
        if  "arrow_label" in self.__dict__.keys() or "start_button" in self.__dict__.keys():
            self.arrow_label.pack_forget()
            self.start_button.pack_forget()

        #Instruction label
        self.instruction.configure(text="Please answer the questions displayed\n after clicking the button below")

        #Arrow Image
        self.arrow = ctk.CTkImage(light_image = Image.open("Pictures\\Arrow.jpg"), size=(170,170))

        #arrow label
        self.arrow_label = ctk.CTkLabel(self.frame, text="", image=self.arrow)

        # Start Button
        self.start_button = ctk.CTkButton(self.frame, text="Start Here", width=225, height=105, command=self.start, corner_radius=10, font=("Comic Sans MS",40))

        # Packing the widgets (again)
        self.instruction.pack(expand=True)
        self.arrow_label.pack(expand=True)
        self.start_button.pack(expand=True)

    def start(self):
        # Updating the question
        self.question_number = 1

        self.data = {}

        self.fields = ["Time","Marks","Option Type","Text Question","Image Question","Hint","Solution Text","Solution Image","Options","Answer"]

        for _ in self.fields:
            if _ == "Options": 
                __ = []
                for i in self.file[_]:
                    __.append(literal_eval(i))
                self.data[_] = __
            else:
                self.data[_] = self.file[_].tolist()

        self.answer_inserted = []

        # Removing all previos widgets
        self.instruction.pack_forget()
        self.arrow_label.pack_forget()
        self.start_button.pack_forget()

        def displayHintFunction():
            self.display_hint_window = ctk.CTkToplevel(self.app)
            self.display_hint_window.transient(self.app)
            self.display_hint_window.title("Hint")
            self.display_hint_window.geometry("600x200+300+50")

            # Displaying the hint in text format
            self.display_hint_label = ctk.CTkLabel(self.display_hint_window, text="This is the hint")

            # Displaying the hint in picture format
            # self.display_hint_file_name = "Pictures/Hint.png"

            for column, items in self.file.items():
                if column == "Hint":
                    self.display_hint_label = ctk.CTkLabel(self.display_hint_window, text="{items[question_number-1-1]}")
                            
            # self.display_hint_image = ctk.CTkImage(light_image=Image.open(self.display_hint_file_name), size=(600,200))
            # self.display_hint_image_label = ctk.CTkLabel(self.display_hint_window, text="", image=self.display_hint_image, width=600, height=200)

            # Displaying hint
            self.display_hint_label.pack()

        def nextFunction():
            # Getting the answer picked and storing it into a list
            answer_picked_index = ExFunc.getAnswerChoosenIndex(self,self.options_variable.get())
            options = self.data["Options"][self.question_number-1]

            self.answer_inserted.append(options[answer_picked_index])

            if self.question_number == len(self.data["Text Question"]):
                self.finished()
            else:
                self.question_number = self.question_number + 1

                question = self.data["Text Question"][self.question_number-1]
                options = self.data["Options"][self.question_number-1]
                
                # Removing the last question to prevent it from reappearing together with the next question
                self.question_textbox.delete("0.0", "end")

                # Inserting the next question
                self.question_textbox.insert("0.0",question)

                # Removing the last options to prevent it from reappearing together with the next options
                self.option_A_entry.delete(0,last_index=tk.END)
                self.option_B_entry.delete(0,last_index=tk.END)
                self.option_C_entry.delete(0,last_index=tk.END)
                self.option_D_entry.delete(0,last_index=tk.END)

                # Inserting the next options
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

        # Widgets that display the question page's frame:
        # Image
        image_width = 900
        image_height = 400

        self.file_name = "Pictures/AddImage.jpg"
        self.image = ctk.CTkImage(light_image=Image.open(self.file_name), size=(image_width,image_height))
        self.image_label = ctk.CTkLabel(self.frame, text="", image=self.image, width=image_width, height=image_height)

        # Label
        self.question_textbox = ctk.CTkTextbox(self.frame, width=900, height=350, fg_color="#c3c3c3", wrap="word", border_width=4,)

        #Option frames
        self.option_frame1 = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3",height=70) # Option A and B

        self.option_frame2 = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3",height=70) #Option C and D

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

        question = self.data["Text Question"][self.question_number-1]
        options = self.data["Options"][self.question_number-1]

        if True:
            self.question_textbox.insert("0.0",question) # Inseting the question 
            self.question_textbox.pack(pady=10)
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
        self.question_textbox.pack_forget()
        self.image_label.pack_forget()
        self.option_frame1.pack_forget()
        self.option_frame2.pack_forget()
        self.footer_frame.pack_forget()

        self.congratulations = ctk.CTkLabel(self.frame, text="Congratulations", font=("Comic Sans MS",42))

        # Marks info
        marks_gotten = 0
        total_marks = sum(self.data["Marks"])

        # Getting the overall score
        for i in range(len(self.answer_inserted)):
            if str(self.answer_inserted[i]) == str(self.data["Answer"][i]):
                marks_gotten = marks_gotten + self.data["Marks"][i]

        percentage = (marks_gotten/total_marks)*100

        # Marks widget
        self.marks = ctk.CTkLabel(self.frame, text=f"You got a {marks_gotten} out of {total_marks} or {round (percentage,2)}%", font=("Comic Sans MS",42))

        # Displaying widgets
        self.congratulations.pack()
        self.marks.pack(expand=True)