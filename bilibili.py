from io import BytesIO
import time

import cv2 as cv
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random

js = """
document.querySelector('canvas[class="geetest_canvas_fullbg geetest_fade geetest_absolute"]').style = ""
"""


class Bilibili(object):
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.browser = None
        self.wait = None

    def send_key(self):
        us = self.browser.find_element_by_id('login-username')
        us.send_keys(self.username)
        time.sleep(1)

        pwd = self.browser.find_element_by_id('login-passwd')
        pwd.send_keys(self.password)

        login = self.browser.find_element_by_xpath('//a[@class="btn btn-login"]')
        login.click()

    def shot_screen(self):

        screenshot = self.browser.get_screenshot_as_png()
        # BytesIO(screenshot) 写入内存的二进制文件
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def shot_origin_screen(self):
        self.browser.execute_script(js)

    def get_position(self):
        img = WebDriverWait(self.browser, 20, 0.5).until(
            ec.presence_of_element_located((By.XPATH, '//div[@class="geetest_canvas_img geetest_absolute"]')))
        print('图片的位置：', img.location)
        location = img.location
        location['x'] += 163
        location['y'] += 67
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return top, bottom, left, right

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :param name:
        :return:  图片验证码
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.shot_screen()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def mouse_action(self, desc=25):
        """
        拖动元素
        """
        dragger = self.browser.find_element_by_xpath('//div[@class="geetest_slider_button"]')
        ActionChains(self.browser).click_and_hold(dragger).perform()

        for x in range(self.get_gap()-desc):
            ActionChains(self.browser).move_by_offset(xoffset=1, yoffset=0).perform()
            time.sleep(random.choice([0.01, 0.02]))
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def get_gap(self, img1='captcha.png', img2='captcha1.png'):
        img = cv.imread(img1, 0)
        img1 = cv.imread(img2, 0)
        gap = None
        for x in range(len(img)):
            for y in range(80, len(img[0])):
                if img[x][y] != img1[x][y] and abs(int(img[x][y]) - int(img1[x][y])) > 20:
                    if not gap:
                        gap = y
                    else:
                        gap = min(gap, y)
        return gap

    def run(self):
        self.browser = webdriver.Chrome()
        self.browser.get('https://passport.bilibili.com/login')
        locator = (By.ID, 'login-username')
        WebDriverWait(self.browser, 20, 0.5).until(ec.presence_of_element_located(locator))
        self.send_key()
        time.sleep(2)
        # self.shot_screen()
        self.get_position()
        # self.mouse_action()
        self.get_geetest_image()
        self.shot_origin_screen()
        self.get_geetest_image('captcha1.png')
        print(self.get_gap())
        self.mouse_action()


if __name__ == "__main__":
    biliili = Bilibili('username', 'password')
    biliili.run()
