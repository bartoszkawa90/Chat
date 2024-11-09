import time

from Chat import *


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

    questions_and_answers = chat.get_whole_conversation(num_of_questions=2)

    return questions_and_answers


if __name__ == '__main__':

    # TESTING ----------------------------------------------------------------------------------------------------------
    test_input1 = 'what is the weather today'
    test_input2 = 'what is the date today'
    # # ------------------------------------------------------------------------------------------------------------------

    # Test full functionality
    answers = ask_chat_and_collect_answers([test_input1, test_input2])



    print('a')
