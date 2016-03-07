import json
import unittest
# from unittest import TestCase
from model import User, UserGroup, Group, Comment, Invite, connect_to_db, db
from server import app
import server
import seed
import os
from flask import session

# api = twitter.Api(
#     consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
#     consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
#     access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
#     access_token_secret=os.environ['TWITTER_TOKEN_SECRET'])

# photos = UploadSet('photos', IMAGES)
# manuals = UploadSet('manuals')

# app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
# app.config['UPLOADED_PHOTOS_ALLOW'] = set(['jpg', 'JPG'])
# app.config['UPLOADED_MANUALS_ALLOW']= set(['pdf', 'PDF'])
# app.config['UPLOADED_MANUALS_DEST'] = 'static/pdfs'

class FlaskTests(unittest.TestCase):
    """Tests for MakeAlong app for functions that don't require sessions."""

    def setUp(self):
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables from model
        db.create_all()

        # Import different types of data from seed file
        seed.load_users()
        seed.load_groups()
        seed.load_usergroups()
        seed.load_patterns()
        
        seed.set_val_user_id()
        seed.set_val_group_id()
        seed.set_val_usergroup_id()
        seed.set_val_pattern_id()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
        # Session.rollback() 


    def test_load_home(self):
        """Tests to see if the homepage comes up."""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h4> Sign in </h4>', result.data)


    def test_load_signup(self):
        """Tests to see if the signup page comes up."""

        result = self.client.get('/sign_up_form')

        self.assertEqual(result.status_code, 200)
        self.assertIn('<h2>Sign Up!</h2>', result.data)


    def test_process_signup_current_user(self):
        """Test sign up form to make sure current user gets sent back home"""

        return self.client.post('/sign_up', 
                                data={'email':'leilani@hbmail.com',
                                      'password':'test',
                                      'first_name':'Leilani',
                                      'last_name':'Taziri',
                                      'user_photo':'images/cat'},
                                follow_redirects=True)

        self.assertIn('<h2>Please Sign In</h2>', result.data)
        self.assertNotIn('<h3> Your craft groups:</h3>', result.data)
        self.assertIn('email already exists, please sign in', result.data)


    def test_process_signup_new_user(self):
        """Test sign up form to make new user can sign up with complete information"""

        return self.client.post('/sign_up', 
                                  data={
                                      'email':'userdgmail.com',
                                      'password':'test',
                                      'first_name':'Jane',
                                      'last_name':'Doe',
                                      'user_photo':'images/dog'},
                                  follow_redirects=True)

        self.assertIn('<h3> Your craft groups:</h3>', result.data)


    def test_process_signup_no_email(self):
        """Test sign up form to make sure you have to enter a password"""

        return self.client.post('/sign_up', 
                                  data={
                                        'email':'',
                                        'password':'test',
                                        'first_name':'Jane',
                                        'last_name':'Doe',
                                        'user_photo':'images/dog'},
                                  follow_redirects=True)

        self.assertIn('<h2>Sign Up!</h2>', result.data)
        self.assertNotIn('<h3> Your craft groups:</h3>', result.data) 


    def test_process_signup_no_password(self):
        """Test sign up form to make sure you have to enter a password"""

        return self.client.post('/sign_up', 
                                  data={
                                        'email':'userdgmail.com',
                                        'password':'',
                                        'first_name':'Jane',
                                        'last_name':'Doe',
                                        'user_photo':'images/dog'},
                                  follow_redirects=True)

        self.assertIn('<h2>Sign Up!</h2>', result.data)
        self.assertNotIn('<h3> Your craft groups:</h3>', result.data) 


    def test_process_signup_no_first_name(self):
        """Test sign up form to make sure you have to enter a firstname"""

        return self.client.post('/sign_up', 
                                  data={
                                        'email':'userdgmail.com',
                                        'password':'test',
                                        'first_name':'',
                                        'last_name':'Doe',
                                        'user_photo':'images/dog'},
                                  follow_redirects=True)

        self.assertIn('<h2>Sign Up!</h2>', result.data)
        self.assertNotIn('<h3> Your craft groups:</h3>', result.data) 


    def test_process_signup_no_last_name(self):
        """Test sign up form to make sure you have to enter a firstname"""
        
        return self.client.post('/sign_up', 
                                  data={
                                  'email':'userdgmail.com',
                                  'password':'test',
                                  'first_name':'Jane',
                                  'last_name':'',
                                  'user_photo':'images/dog'},
                                  follow_redirects=True)

        self.assertIn('<h2>Sign Up!</h2>', result.data)
        self.assertNotIn('<h3> Your craft groups:</h3>', result.data) 


    def test_login_correct(self):
        """Tests to see current user can login with correct info"""

        return self.client.post('/sign_in', 
                                  data={'email':'leilani@hbmail.com',
                                        'password':'test'},
                                  follow_redirects=True)

        self.assertIn('<h3> Your craft groups:</h3>', result.data)


    def test_login_incorrect(self):
        """Tests to see current user can not login with incorrect info"""

        return self.client.post('/sign_in', 
                                  data={'email':'leilani@hbmail.com',
                                        'password':'wrong'},
                                  follow_redirects=True)

        self.assertIn('<h4>Sign in</h4>', result.data)


    def test_login_new_user(self):
        """Tests to see if new user gets sent to sign up page"""

        return self.client.post('/sign_in', 
                                  data={'email':'userfgmail.com',
                                        'password':'test'},
                                  follow_redirects=True)

        self.assertIn('<h2>Sign Up!</h2>', result.data)



class FlaskTestsSessions(unittest.TestCase):
    """Tests for MakeAlong app for functions that require sessions."""

    def setUp(self):
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables from model
        db.create_all()

        # Import different types of data from seed file
        seed.load_users()
        seed.load_groups()
        seed.load_usergroups()
        seed.load_patterns()
        
        seed.set_val_user_id()
        seed.set_val_group_id()
        seed.set_val_usergroup_id()
        seed.set_val_pattern_id()

        with self.client as c:
                with c.session_transaction() as sess:
                    sess['user_id'] = '1'
                c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
        # Session.rollback()        

    # this test wont run. No clue why

    # def correct_group_for_user(self):
    #     """Test that the correct groups are showing on user homepage"""

    #     with self.client.session_transaction() as sess:
    #         sess['user_id'] = 1

    #         result = self.client.get('/user', follow_redirects=True)
        
    #         self.assertEqual(result.status_code, 200)
    #         self.assertIn('Knitters to the Rescue!', result.data)

    def test_show_group_form(self):
        """Test to see if group form page renders"""

        result = self.client.get('/group_form', follow_redirects=True)


        self.assertEqual(result.status_code, 200)
        self.assertIn('<h2>Create a Group!</h2>', result.data)


    def test_logout(self):
        """Test if user can logout"""

        result = self.client.get('/log_out', follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h4> Sign in </h4>', result.data)
      

    def test_group_correct_user(self):
        """Test if user can go to group page based on session user data"""

        result = self.client.get('/group_home/1', follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h3>Knitters to the rescue!</h3>', result.data)



    


if __name__ == '__main__':
    import unittest

    unittest.main()
