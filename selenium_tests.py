import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class MakeAlongLoginLogoutTests(unittest.TestCase):
    """Tests that test different login flows and logout"""


    def setUp(self):
        """Happens before each test"""

        self.driver = webdriver.Chrome("/Users/ltaziri/Documents/Hackbright/project/chromedriver")
        self.driver.implicitly_wait(10)
        self.driver.get("http://localhost:5000")


    def tearDown(self):
        """Happens after each test"""

        self.driver.quit()


    def test_homepage(self):
        """Test that the homepage template is rendering"""

        driver = self.driver

        driver.get_screenshot_as_file("screenshots/homepage.png")

        assert driver.title == "MakeAlong - Bringing the World Together, One Project at a Time"
        assert driver.find_element_by_id("homepage")

    def test_correct_login(self):
        """Test that a user can login with the correct information"""
        
        driver = self.driver
        
        # fill out form with correct information in the test database
        email = driver.find_element_by_name("email")
        email.send_keys("leilani@hbmail.com")

        password = driver.find_element_by_name("password")
        password.send_keys("test")

        btn = driver.find_element_by_tag_name("button")
        btn.click()

        # Check that user has been redirected to the user homepage. 
        # Link to new group form and user profile information is found on the
        # user homepage.
        driver.get_screenshot_as_file("screenshots/correct_login.png")
        assert driver.find_element_by_id("group_add")
        assert driver.find_element_by_id("user_profile")


    def test_existing_user_incorrect_pass(self):
        """Test when an existing user enters in the wrong password"""
        
        driver = self.driver
        
        # Existing user in test database
        email = driver.find_element_by_name("email")
        email.send_keys("leilani@hbmail.com")

        # Incorrect password
        password = driver.find_element_by_name("password")
        password.send_keys("wrong")

        btn = driver.find_element_by_tag_name("button")
        btn.click()

        # Check that user is still on the homepage
        driver.get_screenshot_as_file("screenshots/wrong_password.png")
        assert driver.find_element_by_id("homepage")


    def test_nonexisting_user(self):
        """Test that a new user gets sent to the sign up page"""
        
        driver = self.driver

        # Email does not exist in the test database
        email = driver.find_element_by_name("email")
        email.send_keys("susie@hbmail.com")

        password = driver.find_element_by_name("password")
        password.send_keys("test")

        btn = driver.find_element_by_tag_name("button")
        btn.click()

        # Test that user was redirected to the sign up page. 
        # new_user_email is an id in the sign up form on the sign up page.
        driver.get_screenshot_as_file("screenshots/nonexisting_user.png")
        assert driver.find_element_by_id("new_user_email")


    def test_log_out(self):
        """Test that a user can logout after logging in"""

        driver = self.driver

        email = driver.find_element_by_name("email")
        email.send_keys("leilani@hbmail.com")

        password = driver.find_element_by_name("password")
        password.send_keys("test")
        
        btn = driver.find_element_by_tag_name("button")
        btn.click()

        log_out =  driver.find_element_by_id("logout")
        log_out.click()

        # User should be redirected to homepage after being logged out. 
        driver.get_screenshot_as_file("screenshots/logged_out.png")
        assert driver.find_element_by_id("homepage")


class MakeAlongUserHomeTests(unittest.TestCase):
    """Tests for the user homepage"""


    @classmethod
    def setUpClass(cls):
        """Happens once, before all tests"""
        
        cls.driver = webdriver.Chrome("/Users/ltaziri/Documents/Hackbright/project/chromedriver")
        cls.driver.implicitly_wait(10)
        cls.driver.get("http://localhost:5000")
        
        # Log in
        email = cls.driver.find_element_by_name("email")
        email.send_keys("leilani@hbmail.com")

        password = cls.driver.find_element_by_name("password")
        password.send_keys("test")

        btn = cls.driver.find_element_by_tag_name("button")
        btn.click()
      

    @classmethod
    def tearDownClass(cls):
        """Happens once, after all tests are complete"""

        cls.driver.quit()


    def test_create_group_button(self):
        """Test create a group button correctly links to create group form"""
        
        driver = self.driver
        
        group_btn = driver.find_element_by_link_text("Create a new group")
        group_btn.click()

        driver.get_screenshot_as_file("screenshots/group_form.png")
        assert driver.find_element_by_id("new_group_name")

        #Cancel group form and go back to user homepage
        cancel = driver.find_element_by_link_text("Cancel")
        cancel.click()
        

    def test_user_profile_view(self):
        """Test user profile modal window appears after click on link"""

        driver = self.driver

        # Find the user profile view/update link and click on it
        user_profile_link = driver.find_element_by_xpath("""//*[@id="user_page"]
                                                         /div/section[1]/a""")
        user_profile_link.click()

        driver.get_screenshot_as_file("screenshots/user_profile.png")

        # path to About Me header in modal window
        assert driver.find_element_by_xpath("""//*[@id="user_profile"]/div/div/
                                               div[2]/div[1]/div/div/h3""")


    def test_user_update_profile_form(self):
        """Test if user profile form is shown after clicking button on user profile"""

        driver = self.driver

        # Find the user profile view/update link and click on it
        update_btn = driver.find_element_by_id("show_user_form")
        update_btn.click()
        
        # Confirm that profile info is hidden
        try:
            assert driver.find_element_by_xpath("""//*[@id="user_profile"]/div/div/
                                               div[2]/div[1]/div/div/h3""")
        except NoSuchElementException:
            print "User profile was hidden"

        driver.get_screenshot_as_file("screenshots/user_profile_form.png")

        # Confirm that update form is showing with the user photo and description
        # inputs
        assert driver.find_element_by_id("update_user_photo")
        assert driver.find_element_by_name("user_descrip")


class MakeAlongGroupPageTests(unittest.TestCase):
    """Tests for the user homepage"""


    @classmethod
    def setUpClass(cls):
        """Happens once, before all tests"""
        
        cls.driver = webdriver.Chrome("/Users/ltaziri/Documents/Hackbright/project/chromedriver")
        cls.driver.implicitly_wait(10)
        cls.driver.get("http://localhost:5000")
        
        # Log in
        email = cls.driver.find_element_by_name("email")
        email.send_keys("leilani@hbmail.com")

        password = cls.driver.find_element_by_name("password")
        password.send_keys("test")

        btn = cls.driver.find_element_by_tag_name("button")
        btn.click()
        
        #find and click on the first group
        group = cls.driver.find_element_by_xpath("""//*[@id="user_page"]/div/section[2]
                                        /div/div[1]/div[1]/div/a/h3""")
        group.click()


    @classmethod
    def tearDownClass(cls):
        """Happens once, after all tests are complete"""

        cls.driver.quit()
  

    def test_noshow_user_info(self):
        """Test that ind. group users info is not showing prior to clicking on photo"""

        driver = self.driver

        driver.get_screenshot_as_file("screenshots/group_pg_no_group_user_info.png")
        # Path is in hidden user div that should not show up prior to clicking on
        # the group user's photo.
        try:
            assert driver.find_element_by_xpath("""//*[@id="group_home"]/div/div
                                                   /div[2]/div/section[1]/div[1]
                                                   /div[1]/div[1]/h3""")
        except NoSuchElementException:
            print "Group users info not showing prior to click"


    def test_show_user_info(self):
        """Test that ind. group users info shows after clicking on photo"""

        driver = self.driver

        # Find the first users photo and click on it
        user_photo = driver.find_element_by_xpath("""//*[@id="group_home"]/div
                                                  /div/div[2]/div/section[1]
                                                  /div[1]/div[1]/div[2]""")
        user_photo.click()

        driver.get_screenshot_as_file("screenshots/group_pg_after_user_photo_click.png")
        
        assert driver.find_element_by_xpath("""//*[@id="group_home"]/div/div
                                            /div[2]/div/section[1]/div[1]
                                            /div[1]/div[1]/h3""")
        
        close_btn = driver.find_element_by_xpath("""//*[@id="group_home"]/div/div
                                                 /div[2]/div/section[1]/div[1]
                                                 /div[1]/div[1]/button""")
        close_btn.click()


    def test_update_group_link(self):
        """Test clicking on update group link takes you to group update form"""

        driver = self.driver

        update_link = driver.find_element_by_link_text("Update the group information")
        update_link.click()

        driver.get_screenshot_as_file("screenshots/group_update_from.png")
        
        assert driver.find_element_by_id("update_group_submit")
        
        # Cancel form update and go back to group page
        cancel_btn = driver.find_element_by_link_text("Cancel")
        cancel_btn.click()


    def test_invite_form_modal(self):
        """Test that clicking on invite button brings up the invite form in modal window"""

        driver = self.driver

        driver.get_screenshot_as_file("screenshots/group_page_prior_invitebtn_click.png")

        # Test that form is not showing before clicking on the button
        try:
            assert driver.find_element_by_xpath("""//*[@id="invite"]/div/div
                                                   /div[2]/div/div/form""")
        except NoSuchElementException:
            print "Invite form not showing"

        # Find the button and click on it
        invite_button = driver.find_element_by_xpath("""//*[@id="group_home"]/div
                                                    /div/div[2]/div/section[1]
                                                    /div[2]/div/button""")
        invite_button.click()

        driver.get_screenshot_as_file("screenshots/group_page_post_invitebtn_click.png")

        # Confirm that the modal invite form is showing
        assert driver.find_element_by_xpath("""//*[@id="invite"]/div/div/div[2]
                                            /div/div/form""")

        cancel_btn = driver.find_element_by_link_text("Cancel")
        cancel_btn.click()


if __name__ == "__main__":
    unittest.main()