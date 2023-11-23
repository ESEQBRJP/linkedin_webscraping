from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyautogui
from logger import XlsxUteis

class linkedinScraping:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://172.22.2.241/index.php")
        time.sleep(2)
        login = self.driver.find_element(By.ID, "name")
        login.send_keys("URUBU_PIX")
        time.sleep(3)

        self.driver.find_element(By.XPATH, "/html/body/div[3]/form/input[2]").click()
        time.sleep(2)

        chat = self.driver.find_element(By.ID, "usermsg")
        time.sleep(3)
        for i in range(1,100):
            chat.send_keys(f"CONTANDO ATÉ 1000: {i}")
            time.sleep(0.5)
            self.driver.find_element(By.ID, "submitmsg").click()


LS = linkedinScraping()