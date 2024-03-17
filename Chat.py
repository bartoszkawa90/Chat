import dataclasses
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from copy import deepcopy
import time
import requests
from Logger import Logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import ssl
from functools import wraps
from selenium.webdriver.support.wait import TimeoutException
from random import randint


class Locator:
    def __init__(self, type: str, title: str, value: str) -> None:
        self.type = type
        self.title = title
        self.value = value


@dataclasses.dataclass
class Locators:
    # bing
    close_pop_up_button = Locator(By.ID, 'close pop up', 'bnp_btn_reject')
    text_input = Locator(By.ID, 'text input', 'searchbox')

    # chatgpt
    login_button = Locator(By.XPATH, 'login', '//*[@id="__next"]/div[1]/div[2]/div[1]/div/div/button[1]')

    email_input = Locator(By.ID, 'email', 'email-input')
    username_input = Locator(By.ID, 'username', 'username')

    continue_logging_button = Locator(By.XPATH, 'continue logging', '/html/body/div/main/section/div/div/div/div[1]/div/form/div[2]/button')
    continue_logging = Locator(By.XPATH, 'continue login', '//*[@id="root"]/div/main/section/div[2]/button')

    password_input = Locator(By.ID, 'password', 'password')
    submit_login = Locator(By.CSS_SELECTOR, 'submit login', 'body > div.oai-wrapper > main > section > div > div > div > form > div.c60ff0df8 > button')
    submit_continue = Locator(By.XPATH, 'submit continue', '/html/body/div[1]/main/section/div/div/div/form/div[2]/button')
    text_input = Locator(By.ID, 'input text', 'prompt-textarea')

    create_next_chat = Locator(By.XPATH, 'create new chat', '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[1]/div/a/div[2]')
    answer = Locator(By.XPATH, 'answer', '// *[ @ id = "__next"] / div[1] / div[2] / main / div[2] / div[1] / div / div / div / div[{}]')
    # collect answer
    # // *[ @ id = "__next"] / div[1] / div[2] / main / div[2] / div[1] / div / div / div / div[3]       // first answer
    # // *[ @ id = "__next"] / div[1] / div[2] / main / div[2] / div[1] / div / div / div / div[5]       // second answer

# Decorators
def retry_on_exception(max_retries=3, delay=1, backoff=2, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries, _delay = max_retries, delay
            while retries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Retrying in {_delay} seconds due to {e}, {retries-1} retries left...")
                    time.sleep(_delay)
                    retries -= 1
                    _delay *= backoff
            return func(*args, **kwargs)  # Last attempt without catching exceptions
        return wrapper
    return decorator


def wait_random_delay():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(randint(randint(randint(1, 4), randint(4, 9)), randint(randint(10, 19),
                                                                              randint(19, 40))))  # triple randint
            return func(*args, **kwargs)  # Last attempt without catching exceptions
        return wrapper
    return decorator


class PageOperations:
    def __init__(self):
        self.logger = Logger()
        ssl._create_default_https_context = ssl._create_stdlib_context
        self.driver = uc.Chrome()

    #     @retry_on_exception(max_retries=2, delay=1, exceptions=(TimeoutException,))
    def click(self, locator: Locator):
        self.wait_until_visible(locator, 30)
        element = self.driver.find_element(locator.type, locator.value)
        element.click()
        self.logger.info(f"{locator.title} clicked")

    @wait_random_delay()
    def click_enter(self, locator: Locator):
        self.wait_until_visible(locator, 20)
        element = self.driver.find_element(locator.type, locator.value)
        element.send_keys(Keys.ENTER)

    @wait_random_delay()
    def send_text(self, locator: Locator, text_input: str) -> None:
        self.wait_until_visible(locator, 20)
        element = self.driver.find_element(locator.type, locator.value)
        element.send_keys(text_input)
        self.logger.info(f"text passed to {locator.title}")

    def get_text(self, locator: Locator) -> str:
        self.wait_until_visible(locator, 20)
        element = self.driver.find_element(locator.type, locator.value)
        return element.text

    def wait_until_visible(self, locator: Locator, timeout: int):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((locator.type, locator.value)))
        time.sleep(2)

    def random_refresh(self):
        choice = randint(0, 1)
        if choice == 1:
            self.logger.info("Random refresh")
            self.driver.refresh()
        else:
            time.sleep(randint(randint(1, 4), randint(5, 8)))

    def random_back_and_forward(self):
        choice = randint(0, 1)
        if choice == 1:
            self.logger.info("Random back and forward")
            time.sleep(randint(randint(1, 4), randint(5, 10)))
            self.driver.back()
            time.sleep(randint(randint(10, 13), randint(14, 19)))
            self.driver.forward()
            time.sleep(randint(randint(2, 6), randint(9, 17)))
        else:
            time.sleep(randint(randint(5, 10), randint(11, 19)))

    def random_scroll(self):
        pass


class ChatBING(PageOperations):
    url = 'https://www.bing.com/chat?q=Bing+AI&FORM=hpcodx'
    logger = Logger()

    def open_chat_page(self):
        self.driver.get(self.url)
        self.click(Locators.close_pop_up_button)
        self.logger.info("Page opened")

    def ask_chat(self, locator: Locator = Locators.text_input, text: str = ''):
        self.send_text(locator, text)
        self.click_enter(locator)


class ChatGPT(PageOperations):
    url = 'https://chat.openai.com/chat'
    email = 'bartekkawa2021@gmail.com'
    password = 'MADAfaka2001!'

    def __init__(self):
        super().__init__()
        # ssl._create_default_https_context = ssl._create_stdlib_context
        # # options = webdriver.ChromeOptions()
        # # options.add_argument("--headless")
        # # self.driver = uc.Chrome(options=options)
        # self.driver = uc.Chrome()

    def open_chat_page(self):
        self.driver.get(self.url)

        self.logger.info("Page opened")

    def login_chat(self, tries: int = 3):
        self.random_back_and_forward()
        self.click(Locators.login_button)
        self.random_back_and_forward()

        # proceed with logging in
        try:
            self.send_text(locator=Locators.email_input, text_input=self.email)
        except:
            self.send_text(locator=Locators.username_input, text_input=self.email)

        try:
            self.click(Locators.continue_logging_button)
        except:
            self.click(Locators.continue_logging)
        self.random_refresh()

        self.send_text(locator=Locators.password_input, text_input=self.password)

        # try to finish logging to chat
        time.sleep(30)
        try:
            self.click(Locators.submit_login)
        except:
            self.click(Locators.submit_continue)
        time.sleep(randint(randint(6, 12), randint(14, 30)))
        self.random_refresh()

        self.logger.info("Logged in")
        # create new chat and capture name
        time.sleep(5)
        self.click(Locators.create_next_chat)
        self.logger.info("Chat is ready")

    def ask_chat(self, locator: Locator = Locators.text_input, input: str = '') -> str:
        # put text and press enter
        self.send_text(locator=locator, text_input=input)
        self.click_enter(locator)

    def get_answers(self, num_od_questions: int = 1):
        answers = []
        for i in range(3, 2*(num_od_questions+1), 2):
            locator = deepcopy(Locators.answer)
            locator.value = Locators.answer.value.format(i)
            text = self.get_text(locator)
            answers.append(text)

        return answers





