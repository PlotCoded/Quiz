import customtkinter as ctk
from PIL import Image
import os

class Menu:
    def __init__(self, app):
        self.app = app

    def menu(self,topic_clicked_page): # topic_clicked_page holds the page that is the be displayed when a topic button is clicked
        #Scroll Frame: Contains the "Topic label", "search", "add","edit","delete" buttons and also topics (buttons) as well
        self.scroll_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0, border_width=1, fg_color="#d3d3d3",orientation="vertical")
        
        #Topic Description Label: This just writes topics making a description that the buttons below are the topics in store
        self.topic_description_label = ctk.CTkLabel(self.scroll_frame, text="Topics",width=200,height=50,fg_color="#a3a3a3")
        self.topic_description_label.pack(fill="x",pady=10,padx=10)

        #Editor frame: Contains the "search", "add", "edit", and "delete" button needed for editing, etc
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

        # Getting the names of each topic
        filenames = os.listdir(r"C:\Users\hp\Documents\Quiz\Storage")

        self.buttons = {}  # store each topic button so you can access them later

        # Displaying the topic buttons
        for file in filenames:
            if file.endswith(".csv"):
                file_name = file[:-4]  # remove ".csv"
                # capture the current file_name in the lambda default
                call = lambda f=file_name: topic_clicked_page(f)
                button = ctk.CTkButton(self.scroll_frame, text=file_name, command=call)
                button.pack(pady=50)
                self.buttons[file_name] = button