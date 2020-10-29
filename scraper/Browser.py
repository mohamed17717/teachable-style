from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

from time import sleep

from .URL import URL

import time


class Browser:
    '''
            scrape using selenium firefox
            this is functions uses alot
    '''

    def __init__(self, hide=False):
        self.__config_browser__(hide)
        print('browser has configured')

    def __config_browser__(self, hide):
        options = Options()

        options.headless = hide

        userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        print(userAgent)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", userAgent)
        profile.set_preference("intl.accept_languages", 'en-US')

        options.add_argument("--width=1280")
        options.add_argument("--height=800")

        profile.update_preferences()

        self.driver = webdriver.Firefox(profile, options=options)
        self.driver.implicitly_wait(3)
        self.driver.set_script_timeout(1000)
        print('browser has opened')

    def fill_input(self, selector, value):
        element = self.driver.find_element_by_css_selector(selector)

        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(.7)

        element.clear()
        element.send_keys(value)

    def click_btn(self, selector="", btn=None):
        btn = btn or self.driver.find_element_by_css_selector(selector)

        self.driver.execute_script("arguments[0].scrollIntoView();", btn)
        sleep(.7)

        print('before click...')
        btn.click()
        print('click triggered...')

    def set_cookies(self, cookies):
        for cookie in cookies:
            print(cookie)
            self.driver.add_cookie(cookie)

        time.sleep(2)
        self.refresh()

    def exec_js(self, jsCode, returnVar=''):
        """ 
                put "done();" whenever you want stop if your code need to wait 
                returnVar is variable you want its value
        """
        index = jsCode.find('done();')
        if index >= 0:
            jsCode = jsCode.replace('done();', f'done({returnVar});')
            jsCode = 'var done = arguments[0]; ' + jsCode

            func = self.driver.execute_async_script
        else:
            jsCode = f'{jsCode.rstrip(";")}; return {returnVar};'
            func = self.driver.execute_script
        return func(jsCode)

    def get(self, url, with_cookies=False, tries=1):
        if tries <= 0:
            return

        try:
            self.driver.get(url)
        except TimeoutException:
            print('\n\n\n### CHECK THE INTERNET CONNECTION... ###\n\n\n')
            self.get(url, with_cookies, tries-1)

    def refresh(self):
        return self.driver.refresh()

    def set_cookies_from_file(self, filename):
        with open(filename) as f:
            cookies = f.read()

        self.set_cookies(cookies)

    def get_url(self):
        return self.driver.current_url
