import os
import shutil
import time
from typing import Optional

from difficulty import Difficulty
from question import Question
from string_helper import color_string
from ansi_color_codes import Color

from question_service import QuestionService, NoMoreQuestionsForDifficultyError


class WhoWantsToBeAMillionaire:
    def __init__(self, question_service: QuestionService) -> None:
        self._question_service = question_service
        self._answered_questions = 0
        self._points = 0
        self._terminal_width = shutil.get_terminal_size()[0]

    def start_game(self) -> int:
        self._clear_screen()
        print("Welcome to 'Who wants to be a millionaire?'".center(self._terminal_width), end="\n\n\n")
        print("Each round will be more difficult than the rounds before. Your goal is to reach one million points.")
        try:
            input("Press any key to continue to the first round...")
            while True:
                next_round_should_be_played = self._play_round(None)
                if not next_round_should_be_played or self._points > 1_000_000:
                    self._end_game()
                    break
        except KeyboardInterrupt:
            print("\n\nGoodbye and thanks for playing...")
            time.sleep(1)
            self._clear_screen()
            return 0
        return 0

    def _end_game(self) -> None:
        self._clear_screen()
        if not self._points > 1_000_000:
            print("That was not the correct answer. You lost :(")
        else:
            print(color_string("You've made it to one million points. You've won!\n", Color.LIGHT_GREEN),
                  color_string("Thank you for playing :)\n\n", Color.LIGHT_GREEN))

        input("Press any key to exit...")
        self._clear_screen()

    def _play_round(self, question: Optional[Question]) -> bool:
        self._clear_screen()
        if question:
            new_question = question
        else:
            new_question = self._get_question_based_on_current_points()
        question_string, option_mapping = self._build_question_string(new_question)
        print(question_string, end="\n\n")
        user_choice = input("SELECT [A - D]: ").upper().strip()
        if user_choice not in ["A", "B", "C", "D"]:
            return self._play_round(new_question)

        selected_answer = option_mapping[ord(user_choice) - 65]  # Uses ASCII value to map ABCD to answer index
        self._clear_screen()
        if new_question.answer_question(selected_answer):
            print(color_string("Correct!", Color.GREEN))
            time.sleep(0.3)
            self._points += new_question.points
            self._answered_questions += 1
            return True
        print(color_string("Wrong!", Color.RED))
        time.sleep(0.3)
        return False

    def _build_question_string(self, question: Question) -> tuple[str, list[str, str, str, str]]:
        answers = question.shuffled_answers
        question_string = f"QUESTION NUMBER {self._answered_questions + 1} FOR {question.points} POINTS"
        question_string += "\n"
        question_string += f"Current points: {color_string(str(self._points), Color.CYAN)}"
        question_string += "\n"
        question_string += f"{question.question_string}"
        question_string += "\n\n"
        question_string += f"{color_string('[A]', Color.RED)} {answers[0]} " \
                           f"{color_string('[B]', Color.BLUE)} {answers[1]}\n"
        question_string += f"{color_string('[C]', Color.YELLOW)} {answers[2]} " \
                           f"{color_string('[D]', Color.GREEN)} {answers[3]}"
        return question_string, answers

    def _get_question_based_on_current_points(self) -> Question:
        """ Room-for-improvement: Get rid of magic numbers """
        try:
            if self._points < 4_000:
                return self._question_service.get_question(Difficulty.VERY_EASY)
            elif self._points < 84_000:
                return self._question_service.get_question(Difficulty.EASY)
            elif self._points < 284_000:
                return self._question_service.get_question(Difficulty.MEDIUM)
            elif self._points < 604_000:
                return self._question_service.get_question(Difficulty.HARD)
            return self._question_service.get_question(Difficulty.VERY_HARD)
        except NoMoreQuestionsForDifficultyError:
            # I chose to reset the questions in this case
            self._question_service.reset()
            return self._get_question_based_on_current_points()

    @staticmethod
    def _clear_screen() -> int:
        if os.name == "nt":
            return os.system("cls")
        return os.system("clear")
