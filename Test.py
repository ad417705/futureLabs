import customtkinter as ctk
from tkinter import messagebox
import json

# Load questions from a JSON file
def load_questions(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Initialize personality scores
personality_scores = {
    "Analytical": 0,
    "Creative": 0,
    "Social": 0,
    "Practical": 0
}

# Load questions from the JSON file
questions = load_questions('questions.json')
current_question_index = 0

def display_question():
    question_data = questions[current_question_index]
    question_label.configure(text=f"Question {current_question_index + 1} of {len(questions)}: {question_data['question']}")

    # Update answer buttons with current options
    for key, value in question_data["answers"].items():
        answer_buttons[key].configure(text=value[0])

def select_answer(choice):
    global current_question_index
    selected_personality = questions[current_question_index]["answers"][choice][1]
    personality_scores[selected_personality] += 1

    # Move to the next question or display the result if it’s the last question
    if current_question_index < len(questions) - 1:
        current_question_index += 1
        display_question()
    else:
        display_result()

def display_result():
    final_personality = max(personality_scores, key=personality_scores.get)
    result_text = f"Your overall personality type is: {final_personality}\n\nDetailed Scores:\n"
    for personality, score in personality_scores.items():
        result_text += f"{personality}: {score} points\n"
    messagebox.showinfo("Test Result", result_text)
    root.quit()

# Set up the main application window
ctk.set_appearance_mode("dark")  # Modes: "light" , "dark", "system"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = ctk.CTk()
root.title("Personality Test")
root.geometry("500x600")

# Center the window on the screen
root.eval('tk::PlaceWindow . center')

# Title label
title_label = ctk.CTkLabel(root, text="Discover Your Personality", font=("Helvetica", 24, "bold"))
title_label.pack(pady=20)

# Question frame for better styling
question_frame = ctk.CTkFrame(root)
question_frame.pack(pady=20, fill="x", padx=20)

# Question number and text
question_label = ctk.CTkLabel(question_frame, text="", font=("Arial", 16), wraplength=450, justify="left")
question_label.pack(pady=10)

# Answer buttons with updated colors and style
answer_buttons = {}
for choice in ["A", "B", "C", "D"]:
    button = ctk.CTkButton(
        root, text="", font=("Arial", 14), width=300, height=40, 
        command=lambda c=choice: select_answer(c)
    )
    button.pack(pady=5)
    answer_buttons[choice] = button

# Display the first question
display_question()

root.mainloop()
