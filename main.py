import time

from Chat import *


if __name__ == '__main__':
    chat = ChatBING()

    chat.open_chat_page()

    # chat.login_chat()

    # TESTING ----------------------------------------------------------------------------------------------------------
    test_input1 = 'what is the weather today'
    test_input2 = 'what is the date today'
    # # ------------------------------------------------------------------------------------------------------------------

    chat.ask_chat(text=test_input1)

    # time.sleep(3)
    # chat.ask_chat(input=test_input1)
    # time.sleep(3)
    # chat.ask_chat(input=test_input2)
    # time.sleep(5)
    #
    # answers = chat.get_answers(2)
    # print(answers)



    print('a')
