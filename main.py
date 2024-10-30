"""
This program is a quizz who automatically loads questions after you answer the previous
Author: Carlos NGABA
Date: 29/10/2024
"""

# Import needed libraries
import flet as ft
import time
from quizz_questions import my_questions


# question class represents questions with the list of their answers
class Question:
    def __init__(self, libelle: str, answers: list):
        self.libelle = libelle
        self.answers = answers


# Answer class represents all the possibilities
class Answer:
    def __init__(self, text: str, is_correct: bool):
        self.text = text
        self.is_correct = is_correct


# block_answer is the class who represents visually an answer
class BlockAnswer(ft.Container):
    def __init__(self, cp: object, all_answer: list, answer: Answer):
        super().__init__(
            padding=10, border_radius=8, width=160, height=50,
            scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
            border=ft.border.all(1, "white"),
            on_hover=self.hover_ct, on_click=self.click_ct
        )
        self.cp = cp  # container parent
        self.all_answer = all_answer
        self.answer = answer
        self.content = ft.Row(
            [
                ft.Text(answer.text, size=13, color="white", font_family="Poppins-Medium")
            ], alignment=ft.MainAxisAlignment.CENTER
        )

    # actions when we hover an answer
    def hover_ct(self, e):
        if e.data == "true":
            self.scale = 1.1
            self.update()
        else:
            self.scale = 1
            self.update()

    # Actions when we click on an answer
    def click_ct(self, e):
        # if the answer is correct
        if self.answer.is_correct:
            self.border = ft.border.all(2, ft.colors.LIGHT_GREEN)
            self.content.controls[0].color = ft.colors.LIGHT_GREEN
            self.content.controls[0].update()
            self.update()
            self.cp.result.value = "Bonne réponse"
            self.cp.result.color = ft.colors.LIGHT_GREEN
            self.cp.check.name = ft.icons.CHECK_CIRCLE
            self.cp.check.color = ft.colors.LIGHT_GREEN
            self.cp.check.update()
            self.cp.result.update()
            score = int(self.cp.score.value)
            self.cp.score.value = f"{score + 1}"
            self.cp.progressbar.value = (score + 1) / len(my_questions)

            if self.cp.progressbar.value <= 0.33:
                self.cp.progressbar.color = ft.colors.DEEP_ORANGE
            elif 0.33 < self.cp.progressbar.value <= 0.66:
                self.cp.progressbar.color = ft.colors.AMBER
            elif 0.66 < self.cp.progressbar.value < 1:
                self.cp.progressbar.color = ft.colors.LIGHT_BLUE
            else:
                self.cp.progressbar.color = ft.colors.LIGHT_GREEN

            self.cp.progressbar.update()
            self.cp.score.update()
            self.cp.load_questions_with_time()
            self.cp.question_number.update()
            self.cp.text_question.update()
            self.cp.all_answers.update()
            self.cp.check.update()
            self.cp.result.update()

        # if the answer is incorrect
        else:
            self.border = ft.border.all(2, ft.colors.RED)
            self.content.controls[0].color = ft.colors.RED
            self.content.controls[0].update()
            self.update()
            self.cp.result.value = "Mauvaise réponse"
            self.cp.result.color = ft.colors.RED
            self.cp.check.name = ft.icons.DO_NOT_TOUCH
            self.cp.check.color = ft.colors.RED
            self.cp.check.update()
            self.cp.result.update()
            self.cp.load_questions_with_time()
            self.cp.question_number.update()
            self.cp.text_question.update()
            self.cp.all_answers.update()
            self.cp.check.update()
            self.cp.result.update()


# page to display
class MyQuizz(ft.View):
    def __init__(self, page):
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, route="/"
        )
        self.page = page
        self.item = 0
        self.player = ft.Text(size=16, font_family="Poppins-Bold")
        self.score = ft.Text("0", size=30, font_family="Poppins-ExtraBold")
        self.progressbar = ft.ProgressBar(value=0, color=ft.colors.DEEP_ORANGE, bar_height=15, border_radius=24, width=200)
        self.question_number = ft.Text("", size=16, font_family="Poppins-Bold")
        self.text_question = ft.Text(size=14, font_family="Poppins-Medium")
        self.result = ft.Text(size=18, font_family="Poppins-ExtraBold")
        self.check = ft.Icon(None, None, size=24)
        self.all_answers = ft.Row(controls=[], spacing=25, alignment=ft.MainAxisAlignment.SPACE_AROUND)
        self.content = ft.Column(
            controls=[
                ft.Divider(height=3, color="transparent"),
                ft.Row(
                    [
                        ft.Text("hi", size=16, font_family="Poppins-Italic",
                                color=ft.colors.with_opacity(0.5, "white")),
                        self.player,
                    ], spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(height=1,color="transparent"),
                ft.Row(
                    [
                        ft.Text("Quizz", size=36, font_family="Poppins-ExtraBold", color=ft.colors.INDIGO),
                        ft.Text("Game", size=36, font_family="Poppins-ExtraBold", color=ft.colors.RED),
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(height=3, color="transparent"),
                ft.Row(
                    [
                        ft.Text("Question N°", size=16, weight=ft.FontWeight.BOLD),
                        self.question_number
                    ], spacing=10, alignment=ft.MainAxisAlignment.START
                ),
                ft.Container(
                    expand=True, padding=ft.padding.only(10, 20, 10, 20),
                    border=ft.border.all(1, ft.colors.with_opacity(0.5, "white")),
                    border_radius=12,
                    content=ft.Row([self.text_question], alignment=ft.MainAxisAlignment.CENTER)
                ),
                ft.Divider(height=2, color="transparent"),
                self.all_answers,
                ft.Divider(height=2, color="transparent"),
                ft.Container(
                    expand=True, padding=ft.padding.only(10, 20, 10, 20),
                    border=ft.border.all(1, ft.colors.with_opacity(0.5, "white")),
                    border_radius=12,
                    content=ft.Row([self.result, self.check], alignment=ft.MainAxisAlignment.CENTER)
                ),
                ft.Divider(height=2, color="transparent"),
                ft.Column(
                    controls=[
                        ft.Text("your score", size=16, font_family="Poppins-Bold"),
                        ft.Row(
                            [
                                self.progressbar,
                                self.score,
                                ft.Text(f"/{len(my_questions)}", size=30, font_family="Poppins-ExtraBold")
                            ], alignment=ft.MainAxisAlignment.CENTER
                        )
                    ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.controls=[
            self.content
        ]
        self.box = ft.AlertDialog(
            open=True,
            title=ft.Text("Lancer le quizz", size=16,),
            content=ft.TextField(
                label="Votre nom", label_style=ft.TextStyle(size=12), border_radius=10, width=120
            ),
            actions=[
                ft.TextButton("Lancer", on_click=self.close_box)
            ]
        )
        self.page.overlay.append(self.box)

    # action when we close the welcome box...
    def close_box(self, e):
        self.player.value = self.box.content.value
        self.player.update()
        self.box.open = False
        self.box.update()
        self.load_questions_with_time()
        self.question_number.update()
        self.text_question.update()
        self.all_answers.update()
        self.check.update()
        self.result.update()

    # Loading questions with a delay of 2 seconds...
    def load_questions_with_time(self):
        if self.item < len(my_questions):
            time.sleep(2)
            # print(f"item: {self.item}")
            self.question_number.value = self.item + 1
            # print(f"{self.question_number.value}")
            self.text_question.value = my_questions[self.item]['libelle']

            # remove old possible answers
            for widget in self.all_answers.controls[:]:
                self.all_answers.controls.remove(widget)

            # Put the new possibles answers
            for answer in  my_questions[self.item]['answers']:
                self.all_answers.controls.append(
                    BlockAnswer(
                        self, my_questions[self.item]['answers'], Answer(answer['answer'], answer['is_correct'])
                    )
                )

            # update result
            self.result.value = ""
            self.check.name = None
            self.item += 1

        else:
            for widget in self.all_answers.controls[:]:
                self.all_answers.controls.remove(widget)

            self.all_answers.update()
            self.text_question.value = "Quizz terminé"
            self.text_question.update()

    #Loading questions by a click...
    def load_questions(self, e):
        self.question_number.value = self.item
        self.question_number.update()

        self.text_question.value = my_questions[self.item]['libelle']
        self.text_question.update()

        for widget in self.all_answers.controls[:]:
            self.all_answers.controls.remove(widget)

        for answer in  my_questions[self.item]['answers']:
            self.all_answers.controls.append(
                BlockAnswer(
                    self, my_questions[self.item]['answers'], Answer(answer['answer'], answer['is_correct'])
                )
            )
        self.all_answers.update()

        # for widget in self.all_answers.controls[:]:
        #     widget.on_click = widget.click_ct
        #     widget.update()

        self.result.value = ""
        self.result.update()
        self.check.name = None
        self.check.update()

        if self.item + 1 > len(my_questions):
            pass
        else:
            self.item += 1



def main(page: ft.Page):
    page.fonts = {
        "Poppins-Medium": 'Poppins-Medium.ttf',
        "Poppins-Light": 'Poppins-Light.ttf',
        "Poppins-ExtraBold": 'Poppins-ExtraBold.ttf',
        "Poppins-Bold": 'Poppins-Bold.ttf',
        "Poppins-Italic": 'Poppins-Italic.ttf',
        "Poppins-BoldItalic": 'Poppins-BoldItalic.ttf',
    }
    page.theme_mode = ft.ThemeMode.DARK

    def route_change(route):
        # initial route ...
        page.views.clear()
        page.views.append(MyQuizz(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")




