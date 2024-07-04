import os
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
import csv


def fetch_stackoverflow_answers(url):
    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    answer_div = soup.find_all(
        'div', id=lambda x: x and x.startswith('answer-'), limit=3)
    complete_answer = ""
    all_answers = []
    if answer_div:
        for answers in answer_div:
            answer_builder = ""
            answer_div = answers.find(
                'div', class_='s-prose js-post-body')
            answer_texts = answer_div.find_all()
            for answer_text in answer_texts:
                answer_builder += " " + answer_text.text
            complete_answer = answer_builder
            all_answers.append(complete_answer)
    return all_answers


def fetch_stackoverflow_question_answersurl(url):
    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    question_div = soup.find_all(
        'div', id=lambda x: x and x.startswith('question-summary-'), limit=1)
    question_text = "No question found."
    question_answers_tuple = []
    if question_div:
        for questions in question_div:
            question_text = questions.find('h3').text
            a = questions.find('h3').find('a').get('href')
            answer_url = 'https://stackoverflow.com' + a
            question_answers_tuple.append((question_text, answer_url))
    return question_answers_tuple


def save_to_csv(question, answers):
    file_exists = os.path.isfile('stackoverflow_answers.csv')
    with open('stackoverflow_answers.csv',
              mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Question', 'Answer'])
        writer.writerow([question, answers])


def show_answer():

    question = text_entry.get("1.0", "end-1c")
    if question.strip():
        url = "https://stackoverflow.com/questions/tagged/"+question+"?tab=Votes"
        question_answers = fetch_stackoverflow_question_answersurl(url)
        answer_text.delete("1.0", tk.END)
        for index, (question_text, answer_url) in enumerate(question_answers):
            question_text = question_text.replace('\n', '')
            answers = fetch_stackoverflow_answers(answer_url)
            for i, answer in enumerate(answers):
                answer_text.insert(
                    tk.END, f"Answer {index*3 + i + 1}: {question_text} \n\n{answer}\n\n")
                save_to_csv(question_text, answer)
    else:
        answer_text.delete("1.0", tk.END)
        answer_text.insert(tk.END, "Please enter a question.")


root = tk.Tk()
root.title("Question and Answer App")

style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12), padding=5)
style.configure('TText', font=('Helvetica', 12))

entry_label = ttk.Label(root, text="Enter your question:")
entry_label.pack(pady=(10, 0))

text_entry = tk.Text(root, height=5, width=50, font=('Helvetica', 12))
text_entry.pack(pady=5)

button = ttk.Button(root, text="Get Answer", command=show_answer)
button.pack(pady=10)

scrollable_frame = ttk.Frame(root)
scrollable_frame.pack(pady=0, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(scrollable_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

answer_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=answer_frame, anchor="nw")

answer_text = tk.Text(answer_frame, wrap=tk.WORD, font=('Helvetica', 12))
answer_text.pack(pady=3, padx=3, fill=tk.BOTH, expand=True)

root.mainloop()
