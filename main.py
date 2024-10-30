import os
from random import shuffle
from sys import argv


class Question:  # Класс вопроса
    def __init__(self, question, answers, right_answer):  # Вопрос состоит из:
        self.question = question  # Сам вопрос
        self.answers = answers  # Вариант(ы) ответа
        self.right_answer = right_answer  # Правильный(ые) ответ(ы)

    def __str__(self):
        return self.question

    @staticmethod
    def right_answer():
        return f"{'=' * 5}\nВерно\n{'=' * 5}\n"

    @staticmethod
    def wrong_answer(right_answer):
        return f"{'=' * 60}\nНеверно, правильный(ые) ответ(ы): {right_answer}\n{'=' * 60}\n"

    @staticmethod
    def wrong_input():
        return (f"{'=' * 35}\nТакого варианта ответа нет!\n"
                f"Ответ будет засчитан как неверный!\n{'=' * 35}\n")


def get_questions(filename):
    """
    Функция выгрузки вопросов из файла
    :param filename: параметр принимает название файла
    :return: возвращает список объектов Question
    """
    question_list = list()
    with open(f"{os.getcwd()}\{filename}", "r", encoding="utf8") as file:
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


def multi_answer(question, answer):  # Обработка ответа, если ответов несколько
    global correct_answers_count, incorrect_answers_count
    answers_correct = True
    nums_count = 0
    for letter in answer:
        if letter.isnumeric():
            nums_count += 1
            try:
                if answer == '':
                    raise ValueError
                if not (question.answers[int(letter) - 1] in question.right_answer):
                    answers_correct = False
                    break
            except IndexError:
                return Question.wrong_input()

    if answers_correct and nums_count == len(question.right_answer):
        correct_answers_count += 1
        return Question.right_answer()
    else:
        def right_answers():
            answers = str()
            for i in range(len(question.right_answer)):
                answers += f"{question.answers.index(question.right_answer[i]) + 1} "
            return answers

        incorrect_answers_count += 1
        return Question.wrong_answer(right_answers())


def single_answer(question, answer):  # Обработка ответа, если ответ один
    global correct_answers_count, incorrect_answers_count
    try:
        if answer == '':
            raise ValueError
        if question.answers[int(answer) - 1] in question.right_answer:
            correct_answers_count += 1
            return Question.right_answer()
        else:
            incorrect_answers_count += 1
            return Question.wrong_answer(question.answers.index(*question.right_answer) + 1)
    except IndexError:
        incorrect_answers_count += 1
        return Question.wrong_input()


def line_answer(question):  # Обработка ответа, если ответ письменный
    global correct_answers_count, incorrect_answers_count
    answer = input("Введите ответ: ")  # Ввод ответа
    if answer == '':
        raise ValueError
    if answer.lower() == question.right_answer[0]:
        correct_answers_count += 1
        return Question.right_answer()
    else:
        incorrect_answers_count += 1
        return Question.wrong_answer(question.right_answer[0])


def run_question(questions):  # Функция запуска опросника
    global correct_answers_count, incorrect_answers_count
    for question in questions:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Вопрос: {question}")  # Вопрос
        try:
            # Обработка письменного ответа
            if question.question.__contains__("###") or question.question.__contains__("..."):
                input(line_answer(question))
                continue

            for count in range(len(question.answers)):  # Отображение возможных вариантов ответа
                print(f"{count + 1}. {question.answers[count]}")

            answer = input("Введите ответ(ы): ")  # Ввод ответа

            if len(question.right_answer) > 1:  # Обработка ответа, если ответов несколько
                input(multi_answer(question, answer))

            elif len(question.right_answer) == 1:  # Обработка ответа, если ответ один
                input(single_answer(question, answer))
        except ValueError:
            input(f"{'=' * 35}\nНеправильный формат ввода!\nОтвет будет засчитан как неверный!\n{'=' * 35}")
        except KeyboardInterrupt:
            break


def main(filename="questions.txt"):         # Главная функция, принимает исходные название файла с вопросами
    # Выгрузка вопросов из файла в переменную "questions"
    questions = get_questions(filename)     # Передать название файла в get_question("имя_файла.txt")
    shuffle(questions)                      # Рандомный перебор (shuffle)

    print("После ввода ответа и отображения результата нажмите Enter")
    print('Для досрочного завершения теста и отображения результата нажмите "Ctrl^C"\n')
    input("Нажмите Enter")

    # Запуск опросника
    run_question(questions)

    os.system("cls" if os.name == "nt" else "clear")
    print(f"{'=' * 25}\nИТОГ:\n")
    print(f"Правильных ответов: {correct_answers_count}")
    print(f"Неправильных ответов: {incorrect_answers_count}\n{'=' * 25}\n")


# Счетчик верных и неверных ответов
correct_answers_count = 0
incorrect_answers_count = 0

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    try:
        if argv[1].endswith(".txt"):
            main(argv[1])
        else:
            print("Неверный формат файла. Используйте текстовый файл (txt)")
    except IndexError:
        main()
    except FileNotFoundError:
        print("Файл не найден, проверьте название")
