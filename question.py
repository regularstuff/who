from random import shuffle

from answers import Answers
from difficulty import Difficulty


class Question:
    def __init__(self, question_string: str, answers: Answers, points: int, difficulty: Difficulty) -> None:
        self._question_string = question_string
        self._answers = answers
        self._points = points
        self._difficulty = difficulty

    def answer_question(self, answer: str) -> bool:
        return answer == self._answers.get_correct_answer()

    @property
    def difficulty(self) -> Difficulty:
        return self._difficulty

    @property
    def points(self) -> int:
        return self._points

    @property
    def question_string(self) -> str:
        return self._question_string

    @property
    def shuffled_answers(self) -> list[str, str, str, str]:
        a1, a2, a3 = self._answers.get_wrong_answers()
        a0 = self._answers.get_correct_answer()
        answers = [a0, a1, a2, a3]
        shuffle(answers)
        return answers
