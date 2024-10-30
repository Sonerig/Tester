from random import shuffle


class Question:     # Класс вопроса
    def __init__(self, question, answers, right_answer):    # Вопрос состоит из:
        self.question = question                            # Сам вопрос
        self.answers = answers                              # Вариант(ы) ответа
        self.right_answer = right_answer                    # Правильный(ые) ответ(ы)

    def __str__(self):
        return self.question


def get_questions(filename):    # Функция выгрузки вопросов из файла (возращает список объектов класса Question)
    question_list = list()
    with open(filename, "r", encoding="utf8") as file:
        right_answer = list()
        answers = list()
        question = str()
        for line in file:
            if line.strip().__contains__("I:"):
                answers = answers + right_answer
                shuffle(answers)
                question_list.append(Question(question, answers.copy(), right_answer.copy()))
                right_answer.clear()
                answers.clear()
                question = file.readline().strip().replace("S: ", "")
            elif line.strip().__contains__("+:"):
                right_answer.append(line.strip().replace("+: ", ""))
            elif line.strip().__contains__("-:"):
                answers.append(line.strip().replace("-: ", ""))

    del question_list[0]
    return question_list


def multi_answer(question, answer):         # Обработка ответа, если ответов несколько
    global correct_answers, incorrect_answers
    answers_correct = True
    nums_count = 0
    for letter in answer:
        if letter.isnumeric():
            nums_count += 1
            try:
                if not (question.answers[int(letter) - 1] in question.right_answer):
                    answers_correct = False
                    break
            except IndexError:
                print("Такого варианта ответа нет! Ответ будет защитан как неверный!")

    if answers_correct and nums_count == len(question.right_answer):
        correct_answers += 1
        print("Верно")
    else:
        incorrect_answers += 1
        print("Неверно, правильные ответы: ", end='')
        for i in range(len(question.right_answer)):
            print(f"{question.answers.index(question.right_answer[i]) + 1} ", end='')
        print()


def single_answer(question, answer):        # Обработка ответа, если ответ один
    global correct_answers, incorrect_answers
    try:
        if question.answers[int(answer) - 1] in question.right_answer:
            correct_answers += 1
            print("Верно")
        else:
            incorrect_answers += 1
            print("Неверно, правильный ответ:", question.answers.index(*question.right_answer) + 1)
    except IndexError:
        print("Такого варианта ответа нет! Ответ будет защитан как неверный!")
        incorrect_answers += 1


def line_answer(question):                  # Обработка ответа, если ответ письменный
    global correct_answers, incorrect_answers
    answer = input("Введите ответ(ы): ")  # Ввод ответа
    if answer == question.right_answer[0]:
        correct_answers += 1
        print("Верно")
    else:
        incorrect_answers += 1
        print(f"Неверно, правильный ответ: {question.right_answer[0]}")


def run_question():                                 # Функция запуска опросника
    global correct_answers, incorrect_answers
    for question in questions:
        print(f"Вопрос: {question}")                # Вопрос

        # Обработка письменного ответа
        if question.question.__contains__("###") or question.question.__contains__("..."):
            line_answer(question)
            continue

        for count in range(len(question.answers)):  # Отображение возможных вариантов ответа
            print(f"{count + 1}. {question.answers[count]}")

        answer = input("Введите ответ(ы): ")        # Ввод ответа

        if len(question.right_answer) > 1:          # Обработка ответа, если ответов несколько
            multi_answer(question, answer)

        elif len(question.right_answer) == 1:       # Обработка ответа, если ответ один
            single_answer(question, answer)


# Счетчик верных и неверных ответов
correct_answers = 0
incorrect_answers = 0
# Выгрузка вопросов из файла в questions, рандомный перебор (shuffle)
questions = get_questions("questions.txt")          # Указать название файла в get_question("имя_файла.txt")
shuffle(questions)
# Запуск опросника
run_question()

print("\nИТОГ:")
print(f"Правильных ответов: {correct_answers}")
print(f"Неправильных ответов: {incorrect_answers}")
