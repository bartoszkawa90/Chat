from dataclasses import dataclass
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from copy import deepcopy
import time
from Logger import Logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import ssl
from functools import wraps
from random import randint


class Locator:
    def __init__(self, type: str, title: str, value: str) -> None:
        self.type = type
        self.title = title
        self.value = value


@dataclass
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
    def __init__(self, run_headless=False):
        self.logger = Logger()
        ssl._create_default_https_context = ssl._create_stdlib_context
        self.driver = uc.Chrome()

    #     @retry_on_exception(max_retries=2, delay=1, exceptions=(TimeoutException,))
    def click(self, locator: Locator):
        """ Wait until locator visible and click it """
        self.wait_until_visible(locator, 30)
        element = self.driver.find_element(locator.type, locator.value)
        element.click()
        self.logger.info(f"{locator.title} clicked")

    @wait_random_delay()
    def click_enter(self, locator: Locator):
        """ Wait until locator visible and click enter button """
        self.wait_until_visible(locator, 20)
        element = self.driver.find_element(locator.type, locator.value)
        element.send_keys(Keys.ENTER)

    @wait_random_delay()
    def send_text(self, locator: Locator, text_input: str) -> None:
        """ Wait until locator visible and sent text there """
        self.wait_until_visible(locator, 20)
        element = self.driver.find_element(locator.type, locator.value)
        element.send_keys(text_input)
        self.logger.info(f"text passed to {locator.title}")

    def get_text(self, locator: Locator) -> str:
        """ Wait until locator visible and get its text """
        self.wait_until_visible(locator, 20)
        element = self.driver.find_element(locator.type, locator.value)
        return element.text

    def wait_until_visible(self, locator: Locator, timeout: int):
        """ Wait until locator is visible """
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((locator.type, locator.value)))
        time.sleep(2)

# Randomize to avoid CAPTCHA
    def random_refresh(self):
        """ Randomly refresh page // used only when it does not disturb login pipeline """
        choice = randint(0, 1)
        if choice == 1:
            self.logger.info("Random refresh")
            self.driver.refresh()
        else:
            time.sleep(randint(randint(1, 4), randint(5, 8)))

    def random_back_and_forward(self):
        """ Move on page back and forward and wait some time or just wait random timeout """
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
        """ Scroll down and up random amount of pixels or wait random timeout """
        choice = randint(0, 1)
        if choice == 1:
            scroll = randint(randint(10, 100), randint(101, 600))
            self.driver.execute_script(f"window.scrollBy({scroll}, {scroll});")
            self.driver.execute_script(f"window.scrollBy({scroll}, -{scroll});")
        else:
            time.sleep(randint(randint(2, 7), randint(8, 12)))


class ChatGPT(PageOperations):
    url = 'https://chat.openai.com/chat'
    email = 'bartekkawa2021@gmail.com'
    password = 'MADAfaka2001!'
    status = ''

    def __init__(self, run_headless=False):
        super().__init__(run_headless=run_headless)

    def open_chat_page(self):
        """ Open ChatGPT page """
        self.driver.get(self.url)
        self.status = "Open-not-logged"
        self.logger.info(f"Page opened, {self.status}")

    def login_chat(self):
        """
        Full login with additional random actions to avoid CAPTCHA puzzels
        """
        self.random_scroll()
        self.random_back_and_forward()
        self.click(Locators.login_button)
        self.random_back_and_forward()
        self.random_scroll()

        # proceed with logging in
        try:
            self.send_text(locator=Locators.email_input, text_input=self.email)
        except:
            self.send_text(locator=Locators.username_input, text_input=self.email)
        self.random_scroll()

        try:
            self.click(Locators.continue_logging_button)
        except:
            self.click(Locators.continue_logging)
        self.random_refresh()
        self.random_scroll()

        self.send_text(locator=Locators.password_input, text_input=self.password)

        # try to finish logging to chat
        self.random_scroll()
        try:
            self.click(Locators.submit_login)
        except:
            self.click(Locators.submit_continue)
        time.sleep(randint(randint(6, 12), randint(14, 30)))
        self.random_refresh()
        self.random_scroll()

        self.logger.info("Logged in")
        # create new chat and capture name
        time.sleep(5)
        self.click(Locators.create_next_chat)
        self.status = "Opened-ready-for-questions"
        self.logger.info(f"Chat is ready, {self.status}")

    def ask_chat(self, locator: Locator = Locators.text_input, input: str = '') -> str:
        """ Send text and click enter """
        self.send_text(locator=locator, text_input=input)
        self.click_enter(locator)

    def get_answers(self, num_od_questions: int = 1):
        """ Collect all answers from current chat """
        answers = []
        for i in range(3, 2*(num_od_questions+1), 2):
            locator = deepcopy(Locators.answer)
            locator.value = Locators.answer.value.format(i)
            text = self.get_text(locator)
            answers.append(text)

        return answers

    def delete_chat(self):
        """  """
        pass
