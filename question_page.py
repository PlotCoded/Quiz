import customtkinter as ctk
from PIL import Image
import pandas
from ast import literal_eval
import tkinter as tk
from EditorFiles import Search, Add, Edit, Delete, ExFunc
import random
import QuestionPageFuncs

class QuestionPage:
    def __init__(self, app):
        self.app = app
        
        self.total_marks = 0
        self.marks_gotten = 0

        #This frame contains the welcome instruction and tells to choose a topic from the menu
        self.frame = ctk.CTkFrame(self.app, border_width=1, fg_color="#e3e3e3")
        self.instruction = ctk.CTkLabel(self.frame, text="Please click a topic in the menu to get started", font=("Comic Sans MS",48), width=200,height=50,fg_color="#e3e3e3")

        # #Arrow Image
        self.arrow = ctk.CTkImage(light_image = Image.open("Pictures\\Arrow.jpg"), size=(170,170))

        #arrow label
        self.arrow_label = ctk.CTkLabel(self.frame, text="", image=self.arrow)

        # Start Button
        self.start_button = ctk.CTkButton(self.frame, text="Start Here", width=225, height=105, command=lambda: QuestionPageFuncs.startHereFunc(self), corner_radius=10, font=("Comic Sans MS",40))

        # Hint/Header Frame
        self.hint_frame = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3", width=900, height=75)

        # Hint Button
        self.hint_button = ctk.CTkButton(self.hint_frame, text="View Hint", command=lambda: QuestionPageFuncs.displayHintFunction(self))

        # Widgets that display the question page's frame:
        # Image
        image_width = 900
        image_height = 400

        self.image = ctk.CTkImage(light_image=Image.open(fr"..\Quiz\Pictures\AddImage.jpg"), size=(image_width,image_height))
        self.image_question_label = ctk.CTkLabel(self.frame, text="", image=self.image, width=image_width, height=image_height)

        # Question
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

        self.option_A_button.place(relx=0.15, rely=0.1)
        self.option_A_entry.place(relx=0.19,rely=0.1)
        self.option_B_button.place(relx=0.5,rely=0.1,)
        self.option_B_entry.place(relx=0.54,rely=0.1)
        self.option_C_button.place(relx=0.15,rely=0.1)
        self.option_C_entry.place(relx=0.19,rely=0.1)
        self.option_D_button.place(relx=0.5,rely=0.1)
        self.option_D_entry.place(relx=0.54,rely=0.1)

        #Without Options Textbox
        self.without_options_textbox = ctk.CTkTextbox(self.frame, width=900, height=70, text_color="#000", wrap="word", border_width=4)

        # Footer Frame
        self.footer_frame = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3")

        # Next Button
        self.next_button = ctk.CTkButton(self.footer_frame, text="Next", command=lambda: QuestionPageFuncs.displayQuestions(self))

        # Solutions Button: This button is only displayed when one has answered a question
        self.solutions_button = ctk.CTkButton(self.footer_frame, text="View Solutions", command=None)
        self.solutions_button.configure(command=lambda: QuestionPageFuncs.displaySolution(self))

        self.display_solutions_image = ctk.CTkImage(light_image=Image.open(fr"..\Quiz\Pictures\AddImage.jpg"), size=(600,200))
        self.display_solutions_image_label = ctk.CTkLabel(self.frame, text="", image=self.display_solutions_image, width=600, height=200)

        self.assign_marks_slider = ctk.CTkSlider(self.frame, from_=0,orientation="horizontal")