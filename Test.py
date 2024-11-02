import customtkinter as ctk
import json
from tkinter import messagebox  

class PersonalityTest:
    def __init__(self, questions_file):
        # Load questions and initialize variables
        self.questions = self.load_questions(questions_file)
        self.current_question_index = 0
        self.personality_scores = {"Analytical": 0, "Creative": 0, "Social": 0, "Practical": 0}

        # Set up the main window and create widgets
        self.root = ctk.CTk()
        self.root.title("Personality Test")
        self.create_widgets()
        self.display_question()

        # Set default theme to dark
        self.toggle_theme(dark_mode=True)

    def load_questions(self, filename):
        with open(filename, 'r') as file:
            return json.load(file)

    def create_widgets(self):
        # Title label with updated styling for dark mode
        self.title_label = ctk.CTkLabel(self.root, text="Discover Your Personality", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=15)

        # Frame for the question
        self.question_frame = ctk.CTkFrame(self.root)
        self.question_frame.pack(pady=20, fill="x", padx=20)

        self.question_label = ctk.CTkLabel(self.question_frame, text="", font=("Arial", 14), wraplength=450, justify="left")
        self.question_label.pack()

        # Answer buttons
        self.answer_buttons = {}
        for choice in ["A", "B", "C", "D"]:
            button = ctk.CTkButton(self.question_frame, text="", 
                                    command=lambda c=choice: self.select_answer(c))
            button.pack(pady=5)
            self.answer_buttons[choice] = button

        # Theme toggle switch
        self.theme_switch = ctk.CTkSwitch(self.root, text="Toggle Dark/Light Theme", command=self.toggle_theme)
        self.theme_switch.pack(pady=10)

    def display_question(self):
        question_data = self.questions[self.current_question_index]
        self.question_label.configure(text=f"Question {self.current_question_index + 1} of {len(self.questions)}: {question_data['question']}")

        # Update answer buttons with current options
        for key, value in question_data["answers"].items():
            self.answer_buttons[key].configure(text=value[0])

    def select_answer(self, choice):
        selected_personality = self.questions[self.current_question_index]["answers"][choice][1]
        self.personality_scores[selected_personality] += 1

        # Move to the next question or display the result if it’s the last question
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.display_question()
        else:
            self.display_result()

    def display_result(self):
        final_personality = max(self.personality_scores, key=self.personality_scores.get)
        result_text = f"Your overall personality type is: {final_personality}\n\nDetailed Scores:\n"
        for personality, score in self.personality_scores.items():
            result_text += f"{personality}: {score} points\n"
        messagebox.showinfo("Test Result", result_text)  # Use tkinter's messagebox
        self.root.quit()

    def toggle_theme(self, dark_mode=None):
        # Check the current mode of the switch
        if dark_mode is None:
            dark_mode = self.theme_switch.get()  # Get the state of the switch

        if dark_mode:
            ctk.set_appearance_mode("dark")
            self.title_label.configure(text_color="white")  # Change text color to white in dark mode
            self.root.configure(bg="#2E2E2E")  # Dark background for the root
        else:
            ctk.set_appearance_mode("light")
            self.title_label.configure(text_color="black")  # Change text color to black in light mode
            self.root.configure(bg="#FFFFFF")  # Light background for the root

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    test = PersonalityTest("questions.json")
    test.run()
