import sys
from pathlib import Path
from random import shuffle

from answers import Answers
from difficulty import Difficulty
from question import Question


class NoMoreQuestionsForDifficultyError(Exception):
    def __init__(self):
        pass


class QuestionService:
    """Note: 4 Questions per difficulty needed"""
    def __init__(self, path_to_questions: str | Path) -> None:
        self._fresh_questions: list[Question] = []
        self._answered_questions: list[Question] = []
        self._load_questions_from_file(path_to_questions)
        shuffle(self._fresh_questions)

    def _load_questions_from_file(self, path_to_questions: str | Path) -> None:
        with open(path_to_questions, "r", encoding="utf-8") as questions_file:
            question_lines = questions_file.readlines()[3:]
        for line in question_lines:
            fields = line.split("|")

            answers = Answers(correct_answer=fields[1].strip(), wrongs_answers=(
                fields[2].strip(), fields[3].strip(), fields[4].strip()
            ))
            try:
                difficulty = Difficulty(int(fields[5].strip()))
                points = int(fields[6].strip())
            except IndexError:
                print("Error loading questions: A question line does not contain all information.")
                sys.exit(1)
            except KeyError:
                print("Error loading questions: A questions points or difficulty value has a non-integer value.")
                sys.exit(1)

            self._fresh_questions.append(Question(fields[0].strip(), answers, points, difficulty))

    def get_question(self, difficulty: Difficulty) -> Question:
        for idx, q in enumerate(self._fresh_questions):
            if q.difficulty == difficulty:
                question = self._fresh_questions.pop(idx)
                self._answered_questions.append(question)
                return question

        raise NoMoreQuestionsForDifficultyError()

    def reset(self) -> None:
        self._fresh_questions.extend(self._answered_questions)
        self._answered_questions = []
