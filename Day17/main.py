from qnsmodel import Question
from data import question_data
from quizbrain import QuizBrain

question_bank=[]

for question in question_data:
    question_text= question ["text"]
    question_answer=question["answer"]
    new_question=Question(question_text,question_answer)
    question_bank.append(new_question)

# print(question_bank[0].answer)
quiz= QuizBrain(question_bank)

while quiz.still_has_question():
    quiz.next_question()
print("you've completed the quiz")
print(f"Your final score was :{quiz.score}/{quiz.question_number}")

