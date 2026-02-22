import customtkinter as ctk

from EditorFiles import Search, Add, Edit, Delete, ExFunc
from menu import Menu
from header import Header
from question_page import QuestionPage

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

        # Position of the center of the page
        centerx = 0
        centery = 0

        #Setting the width and height of the app to max
        self.geometry(f"{self.width}x{self.height}+{centerx}+{centery}") 

        # Creating grids for widgets placements
        self.columnconfigure(tuple(range(0,21)),weight=1)
        self.rowconfigure(tuple(range(0,21)),weight=1)

        #Initializing imported classes
        self.search = Search.Search(self)
        self.add = Add.Add(self)
        self.edit = Edit.Edit(self)
        self.delete = Delete.Delete(self)

        # Initializing external classes
        self.header = Header(self)
        self.header.header()

        self.question_page = QuestionPage(self)
        self.question_page.firstPageYouSee()

        self.menu = Menu(self)
        self.menu.menu(self.question_page.topicClickedPage)

    def createMenuAnimation(self):
        # Creating the menu animation/movement/closing and opening
        self.menuOpened = False
        self.scroll_frame_to_open = self.menu.scroll_frame
        self.question_page_frame = self.question_page.frame

        def menu_animation(): # This function allows the menu to be opened and closed after pressing the button
            if self.menuOpened == True:
                self.scroll_frame_to_open.grid_forget()
                self.question_page_frame.grid(row=1,column=0, rowspan=21,columnspan=21, sticky="nsew")
                self.menuOpened = False
            else:
                self.scroll_frame_to_open.grid(row=1, column=0, rowspan=21, columnspan=5,sticky="nsew")
                self.question_page_frame.grid(row=1,column=5, rowspan=21,columnspan=16,sticky="nsew")
                self.menuOpened = True

        # Changing the command of the button from None to menu_animation
        self.header.menu_button.configure(command=lambda: menu_animation())

# Initializing the app/Running the program
app = App()
app.createMenuAnimation()

app.mainloop()