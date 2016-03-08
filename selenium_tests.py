import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class MakeAlongBrowserTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        

    def test_correct_login(self):
        
        browser= self.browser
        browser.get('http://localhost:5000')
        assert browser.title == 'MakeAlong - Bringing the World Together, One Project at a Time'

        email = browser.find_element_by_name('email')
        email.send_keys("leilani@hbmail.com")
        password = browser.find_element_by_name('password')
        password.send_keys("test")

        btn = browser.find_element_by_tag_name('button')

        btn.click()

        assert browser.find_element_by_id('group_add')


    def test_existing_user_incorrect_pass(self):
        
        browser= self.browser
        browser.get('http://localhost:5000')
        assert browser.title == 'MakeAlong - Bringing the World Together, One Project at a Time'

        email = browser.find_element_by_name('email')
        email.send_keys("leilani@hbmail.com")
        password = browser.find_element_by_name('password')
        password.send_keys("wrong")

        btn = browser.find_element_by_tag_name('button')

        btn.click()

        assert browser.find_element_by_id('homepage')

    def test_nonexisting_user(self):
        
        browser= self.browser
        browser.get('http://localhost:5000')
        assert browser.title == 'MakeAlong - Bringing the World Together, One Project at a Time'

        email = browser.find_element_by_name('email')
        email.send_keys("susie@hbmail.com")
        password = browser.find_element_by_name('password')
        password.send_keys("test")

        btn = browser.find_element_by_tag_name('button')

        btn.click()

        assert browser.find_element_by_id('new_user_email')

    def test_log_out(self):

        browser= self.browser
        browser.get('http://localhost:5000')

        email = browser.find_element_by_name('email')
        email.send_keys("leilani@hbmail.com")
        password = browser.find_element_by_name('password')
        password.send_keys("test")
        
        btn = browser.find_element_by_tag_name('button')
        btn.click()

        log_out =  btn = browser.find_element_by_id('logout')
        log_out.click()

        assert browser.find_element_by_name('password')


    def test_signup_form(self):

        browser= self.browser
        browser.get('http://localhost:5000/sign_up_form')

        assert browser.find_element_by_id('new_user_email')



    def tearDown(self):
        self.browser.close()

if __name__ == "__main__":
    unittest.main()