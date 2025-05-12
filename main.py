import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image
import Storage
import random
from EditorFiles import Search, Add, Edit, Delete

#Applying the theme of the window
ctk.set_default_color_theme("Storage\\Theme.json")

#This class is the main window of the application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

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
        self.subject_var = tk.StringVar(value = f"Subject: {self.subject}")
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
        self.score_var = tk.IntVar(value = f"Marks: {self.marks}")
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

        #Creating an hover effect
        def hover(button_type):
            if button_type == "Search":
                self.search_image = ctk.CTkImage(light_image=Image.open("Pictures\\Hover\\HoverSearch.jpg"),size=(30,30))
                self.search_button.configure(image=self.search_image, fg_color="#098bed")
            elif button_type == "Add":
                self.add_image = ctk.CTkImage(light_image=Image.open("Pictures\\Hover\\HoverAdd.png"),size=(30,30))
                self.add_button.configure(image=self.add_image, fg_color="#098bed")
            elif button_type == "Edit":
                self.edit_image = ctk.CTkImage(light_image=Image.open("Pictures\\Hover\\HoverEdit.png"),size=(30,30))
                self.edit_button.configure(image=self.edit_image, fg_color="#098bed")
            elif button_type == "Delete":
                self.delete_image = ctk.CTkImage(light_image=Image.open("Pictures\\Hover\\HoverDelete.png"),size=(30,30))
                self.delete_button.configure(image=self.delete_image, fg_color="#098bed")

        def leave(button_type):
            if button_type == "Search":
                self.search_image = ctk.CTkImage(light_image=Image.open("Pictures\\Search.jpg"),size=(30,30))
                self.search_button.configure(image=self.search_image, fg_color="#01a9f3")
            elif button_type == "Add":
                self.add_image = ctk.CTkImage(light_image=Image.open("Pictures\\Add.png"),size=(30,30))
                self.add_button.configure(image=self.add_image, fg_color="#01a9f3")
            elif button_type == "Edit":
                self.edit_image = ctk.CTkImage(light_image=Image.open("Pictures\\Edit.png"),size=(30,30))
                self.edit_button.configure(image=self.edit_image, fg_color="#01a9f3")
            elif button_type == "Delete":
                self.delete_image = ctk.CTkImage(light_image=Image.open("Pictures\\Delete.png"),size=(30,30))
                self.delete_button.configure(image=self.delete_image, fg_color="#01a9f3")

        def click(button_type):
            if button_type == "Search":
                self.search_image = ctk.CTkImage(light_image=Image.open("Pictures\\Search.jpg"),size=(30,30))
                self.search_button.configure(image=self.search_image)
            elif button_type == "Add":
                self.add_image = ctk.CTkImage(light_image=Image.open("Pictures\\Add.png"),size=(30,30))
                self.add_button.configure(image=self.add_image)
            elif button_type == "Edit":
                self.edit_image = ctk.CTkImage(light_image=Image.open("Pictures\\Edit.png"),size=(30,30))
                self.edit_button.configure(image=self.edit_image)
            elif button_type == "Delete":
                self.delete_image = ctk.CTkImage(light_image=Image.open("Pictures\\Delete.png"),size=(30,30))
                self.delete_button.configure(image=self.delete_image)

        #Mouse Hover
        self.search_button.bind("<Enter>", lambda event: hover("Search"))
        self.add_button.bind("<Enter>", lambda event: hover("Add"))
        self.edit_button.bind("<Enter>", lambda event: hover("Edit"))
        self.delete_button.bind("<Enter>", lambda event: hover("Delete"))

        #Mouse Leave
        self.search_button.bind("<Leave>", lambda event: leave("Search"))
        self.add_button.bind("<Leave>", lambda event: leave("Add"))
        self.edit_button.bind("<Leave>", lambda event: leave("Edit"))
        self.delete_button.bind("<Leave>", lambda event: leave("Delete"))

        #Mouse Click
        self.search_button.bind("<Button-1>", lambda event: leave("Search"))
        self.add_button.bind("<Button-1>", lambda event: leave("Add"))
        self.edit_button.bind("<Button-1>", lambda event: leave("Edit"))
        self.delete_button.bind("<Button-1>", lambda event: leave("Delete"))

        #Inserting subjects
        for _ in range(10):
            ctk.CTkButton(self.scroll_frame, text="Tom", command=self.app.question_page.starting).pack(pady=50)

class QuestionPage:
    def __init__(self, app):
        self.app = app

    def welcome(self):
        #This frame contains the welcome instruction and tells to choose a topic from the menu
        self.frame = ctk.CTkFrame(self.app, border_width=1, fg_color="#e3e3e3")
        self.frame.grid(row=1, column=0, rowspan=21, columnspan=21,sticky="nsew")

        #Instruction label
        self.instruction = ctk.CTkLabel(self.frame, text="Please choose a topic listed \n after clicking the Menu button", font=("Comic Sans MS",42), width=200,height=50,fg_color="#e3e3e3")
        self.instruction.pack(expand=True, fill="both")

    def starting(self):
        #New Instruction
        self.instruction.configure(text="Please answer the questions listed\n after clicking the button below")
        self.instruction.configure(font=("Comic Sans MS",48))

        #Arrow Image
        self.arrow = ctk.CTkImage(light_image = Image.open("Pictures\\Arrow.jpg"), size=(170,170))

        #arrow label
        self.arrow_label = ctk.CTkLabel(self.frame, text="", image=self.arrow)
        self.arrow_label.pack()

        #Starting Button
        self.starting_button = ctk.CTkButton(self.frame, text="Start Here", width=225, height=105, command=self.start, corner_radius=10, font=("Comic Sans MS",40))
        self.starting_button.pack(expand=True)

    def start(self):
        # Removing all previos widgets
        self.instruction.pack_forget()
        self.arrow_label.pack_forget()
        self.starting_button.pack_forget()

        def displayHintFunction():
            pass

        def nextFunction():
            pass

        def viewSolutionsFunction():
            pass

        # Hint/Header Frame
        self.hint_frame = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3", width=900, height=75)

        # Hint Button
        self.hint_button = ctk.CTkButton(self.hint_frame, text="View Hint", command=displayHintFunction)

        # Widgets that display the question_page
        # Image
        image_width = 1000
        image_height = 400

        self.file_name = "Pictures/AddImage.jpg"
        self.image = ctk.CTkImage(light_image=Image.open(self.file_name), size=(image_width,image_height))
        self.image_label = ctk.CTkLabel(self.frame, text="", image=self.image, width=image_width, height=image_height)

        # Label
        self.text_label = ctk.CTkTextbox(self.frame)

        #Option frames
        self.option_frame1 = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3",height=50)

        self.option_frame2 = ctk.CTkFrame(self.frame, border_width=0, fg_color="#e3e3e3",height=50)

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
        self.without_options_textbox = ctk.CTkTextbox(self.frame, width=600, height=50, text_color="#00FF00")

        # Footer Frame
        self.footer_frame = ctk.CTkFrame(self.frame, border_width=1, fg_color="#e3e3e3")

        # Next Button
        self.next_button = ctk.CTkButton(self.footer_frame, text="Next", command=nextFunction)

        # Solutions Button
        self.solutions_button = ctk.CTkButton(self.footer_frame, text="View Solutions", command=viewSolutionsFunction)

        # Displaying widgets
        self.hint_frame.pack(fill="x")
        self.hint_button.place(relx=0.75, rely=0.25)

        if True:
            self.image_label.pack(expand=False,pady=10)

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

app = App()