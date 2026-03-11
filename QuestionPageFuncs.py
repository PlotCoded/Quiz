import customtkinter as ctk
import tkinter as tk
from PIL import Image
import random
import pandas
from ast import literal_eval
from EditorFiles import ExFunc

def displayTopicClickedPage(self):
        # Packing the widgets (again)
        self.instruction.configure(text="Please answer the questions displayed\n after clicking the button below")
        
        self.instruction.pack(expand=True)
        self.arrow_label.pack(expand=True)
        self.start_button.pack(expand=True)

def forgetTopicClickedPage(self):
        # Removing all previos widgets
        self.instruction.pack_forget()
        self.arrow_label.pack_forget()
        self.start_button.pack_forget()

def topicClickedPage(self, topic_name): # Also essentially, the secnod page you see when you click on the question page (when you click a topic button)
        self.topic_name = topic_name

        # Changing the topic label in the header to the topic clicked/choosen
        self.app.header.subject_var.set(value=f"Topic: {topic_name}")

        # Getting all the stored data of the topic's file
        self.pf = pandas.read_csv(fr"..\Quiz\Storage\{topic_name}.csv")

        # Getting number of marks on the topic
        self.total_marks = self.marks_gotten = 0
        for i in (self.pf["Marks"]).tolist():
                self.total_marks += int(i)

        forgetResultsPage(self)
        forgetQuestion(self)
        forgetSolutionPage(self)
        displayTopicClickedPage(self)

def firstPageYouSee(self):
        # Displaying the page: It only has the instruction: "Please answer the questions listed after clicking the button below" at the beginning/at first
        self.frame.grid(row=1, column=0, rowspan=21, columnspan=21,sticky="nsew")

        # Displaying the instruction
        self.instruction.pack(expand=True, fill="both")

def startHereFunc(self):
        self.all_question_indexes = [n for n in range(self.pf.shape[0])]

        if "randomize":
                random.shuffle(self.all_question_indexes)

        forgetTopicClickedPage(self)
        displayQuestions(self)

def forgetQuestion(self):
        # Unpacking the previous widgets
        self.hint_frame.pack_forget()
        self.question_textbox.pack_forget()
        self.solutions_button.pack_forget()
        self.option_frame1.pack_forget()
        self.option_frame2.pack_forget()
        self.without_options_textbox.pack_forget()
        self.footer_frame.pack_forget()

def displayQuestions(self): # Also the solution func
    if "index" in self.__dict__: 
            if not self.pf.at[self.index, "Option Type"] == "Options":
                    self.marks_gotten = self.marks_gotten + self.assign_marks_slider.get()

    forgetSolutionPage(self)

    if self.all_question_indexes:
        self.index = self.all_question_indexes.pop() # Getting the question index

        # Displaying widgets
        self.hint_frame.pack(fill="x")
        self.hint_button.place(relx=0.75, rely=0.25)

        if len(self.pf.at[self.index,"Text Question"]) > 0:
                # Removing the last question to prevent it from reappearing together with the next question
                self.question_textbox.delete("0.0", "end")
                self.question_textbox.insert("0.0",self.pf.at[self.index,"Text Question"]) # Inserting the next question
                self.question_textbox.pack(pady=10)
        else:
                # Image Question
                self.image_question = self.pf.at[self.index, 'Image Question']
                self.image_question_label.pack(pady=10)

        # Options
        options = literal_eval(self.pf.at[self.index, "Options"])
        
        if self.pf.at[self.index, 'Option Type'] == "Options":
                self.option_frame1.pack(fill="x", pady=3, padx=10)
                self.option_frame2.pack(fill="x",pady=3,padx=10)

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
        else:
                self.without_options_textbox.delete("0.0","end")
                self.without_options_textbox.pack()

        self.footer_frame.pack(fill="both")
        self.solutions_button.pack(padx=250)
    else:
        finished(self)

def forgetSolutionPage(self):
        if "display_solutions_label" in self.__dict__.keys(): self.display_solutions_label.pack_forget()
        if "display_solutions_image_label" in self.__dict__.keys(): self.display_solutions_image_label.pack_forget()
        if "next_button" in self.__dict__.keys(): self.next_button.pack_forget()

        self.assign_marks_slider.pack_forget()
        self.footer_frame.pack_forget()

def displayHintFunction(self):
        self.display_hint_window = ctk.CTkToplevel(self.app)
        self.display_hint_window.transient(self.app)
        self.display_hint_window.title("Hint")
        self.display_hint_window.geometry("600x200+300+50")

        # Getting the hint for that question
        hint = self.pf.at[self.index, "Hint"]

        # Displaying the hint in text format
        self.display_hint_label = ctk.CTkLabel(self.display_hint_window, text=f"{hint}")
                    
        # Displaying hint
        self.display_hint_label.pack()

def displaySolution(self):
        forgetQuestion(self)

        # Getting the answer picked and calculating its marks for that question
        options = literal_eval(self.pf.at[self.index, "Options"])

        # Displaying the solution widgets
        self.display_solutions_file_name = self.pf.at[self.index, "Solution Image"]
        self.display_solutions_image = ctk.CTkImage(light_image=Image.open(self.display_solutions_file_name), size=(600,200))
        self.display_solutions_image_label.configure(image=self.display_solutions_image)
        self.display_solutions_image_label.pack(pady=10)

        self.display_solutions_label = ctk.CTkLabel(self.frame, text=f"The solution to question {self.index+1} is {self.pf.at[self.index, "Answer"]}.\n{self.pf.at[self.index, "Solution Text"]}")
        self.display_solutions_label.pack(pady=10)

        if not self.pf.at[self.index, "Option Type"] == "Options":
                self.assign_marks_slider.configure(to=int(self.pf.at[self.index, "Marks"]))
                self.assign_marks_slider.configure(number_of_steps=int(self.pf.at[self.index, "Marks"]))
                self.assign_marks_slider.pack(pady=10)

        self.footer_frame.pack(fill="both")
        self.next_button.pack(expand=True, padx=250)

        # Assinging marks
        if self.pf.at[self.index, "Option Type"] == "Options":
                answer_picked = options[ExFunc.getAnswerChoosenIndex(self,self.options_variable.get())]
                if str(answer_picked) == str(self.pf.at[self.index, "Answer"]):
                        self.marks_gotten = self.marks_gotten + self.pf.at[self.index, "Marks"]

def finished(self):        
        self.congratulations = ctk.CTkLabel(self.frame, text="Congratulations", font=("Comic Sans MS",42))

        percentage = (self.marks_gotten/self.total_marks)*100

        # Marks widget
        self.marks = ctk.CTkLabel(self.frame, text=f"You got a {self.marks_gotten} out of {self.total_marks} or {round (percentage,2)}%", font=("Comic Sans MS",42))

        # Displaying widgets
        self.congratulations.pack()
        self.marks.pack(expand=True)

def forgetResultsPage(self):
        # Getting rid of all previous widgets
        if "congratulations" in self.__dict__.keys() and "marks" in self.__dict__.keys(): # When the question page is first initialised, these two variables aren't initialised along with it
            # It is only initialised when finished(self) has been called, thus checks if the variables has been initialised, if so, remove this widgets from the window
            self.congratulations.pack_forget()
            self.marks.pack_forget()