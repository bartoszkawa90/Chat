import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from Chat import *



class MainApp(App):
    # TODO asynchronius chat running ?
    # chat = ChatGPT(run_headless=True)

    def __init__(self):
        super().__init__()
        self.question_field = None
        self.answer_field = None

    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        self.question_field = TextInput(
            multiline=True, readonly=False, halign="center", font_size=40,
        )
        self.answer_field = Label(
            text="Answers:\n", font_size=42, size_hint=(1.0, 3.0), pos=(200, 200)
        )

        main_layout.add_widget(self.question_field)
        main_layout.add_widget(self.answer_field)
        buttons = [[
            "ASK", "Clear", "Email", "Download",
        ]]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                # button = Button(text=label, pos_hint={"center_x": 0.2, "center_y": 0.5}, size=(10, 100)) #TODO ogarnąć rozmiar przycisków
                button = Button(size_hint=(0.2, 0.4), pos=(200, 200), text=label)
                # button.bind(on_press=funkcja co ma sie wywołąć) #TODO add action to button
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        # self.operators = ["/", "*", "+", "-"]
        # self.last_was_operator = None
        # self.last_button = None
        # main_layout = BoxLayout(orientation="vertical")
        # self.solution = TextInput(
        #     multiline=False, readonly=True, halign="right", font_size=55
        # )
        # main_layout.add_widget(self.solution)
        # buttons = [
        #     ["7", "8", "9", "/"],
        #     ["4", "5", "6", "*"],
        #     ["1", "2", "3", "-"],
        #     [".", "0", "C", "+"],
        # ]
        # for row in buttons:
        #     h_layout = BoxLayout()
        #     for label in row:
        #         button = Button(
        #             text=label,
        #             pos_hint={"center_x": 0.5, "center_y": 0.5},
        #         )
        #         button.bind(on_press=self.on_button_press)
        #         h_layout.add_widget(button)
        #     main_layout.add_widget(h_layout)
        #
        # equals_button = Button(
        #     text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        # )
        # equals_button.bind(on_press=self.on_solution)
        # main_layout.add_widget(equals_button)

        return main_layout

    def ask_chat_and_collect_answers(questions: list) -> list[QA]:
        """ Open Chat write questions and collect answers """
        chat = ChatGPT()
        chat.open_chat_page()
        try:
            chat.login_chat()
        except:
            chat.click(Locators.verify_checkbox)
            time.sleep(randint(3, 6))
            chat.login_chat()

        for question in questions:
            chat.ask_chat(input=question)

        QAs = chat.get_whole_conversation(num_of_questions=2)

        return QAs



chatapp = MainApp()
chatapp.run()