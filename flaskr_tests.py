import json
import unittest
# from unittest import TestCase
from model import User, UserGroup, Group, Comment, Invite, connect_to_db, db, example_data
from server import app
import server
import seed
import os

class FlaskTests(unittest.TestCase):

    def setUp(self):

        app.config['SECRET_KEY'] = 'sekrit!'
        # Get the Flask test client
        self.client = app.test_client(use_cookies=True)

        # self.app = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql://localhost/testdb")

        # Create tables and add sample data
        # db.create_all()

        # db.session.commit()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
        # Session.rollback() 


    def test_home(self):
        result = self.client.get('/')
        self.assertIn('<h2>Please Sign In</h2>', result.data)

   
    def test_login(self):
        return self.client.post('/sign_in', 
                                  data=dict(
                                  email='userbgmail.com',
                                  password='wrong'),
                                  follow_redirects=True)

        self.assertIn('<h2>Please Sign In</h2>', result.data)

        return self.client.post('/sign_in', 
                                  data=dict(
                                  email='userfgmail.com',
                                  password='test'),
                                  follow_redirects=True)

        self.assertIn('<h2>Sign Up!</h2>', result.data)


        return self.client.post('/sign_in', 
                                  data=dict(
                                  email='useragmail.com',
                                  password='test'),
                                  follow_redirects=True)

        self.assertIn('<h3> Your craft groups:</h3>', result.data)

    def test_sign_up_form(self):
        result = self.client.get('/sign_up_form')
        self.assertIn('<h2>Sign Up!</h2>', result.data)

    
    def test_logout(self):
        result = self.client.get('/log_out')
        self.assertIn('<h2>Please Sign In</h2>', result.data)


    def test_sign_up(self):
        return self.client.post('/sign_up', 
                                  data=dict(
                                  email='userdamail.com',
                                  password='test',
                                  first_name='Betty',
                                  last_name='Sue',
                                  user_photo='images/cat'),
                                  follow_redirects=True)

        self.assertIn('<h2>Please Sign In</h2>', result.data)

        return self.client.post('/sign_up', 
                                  data=dict(
                                  email='userdgmail.com',
                                  password='test',
                                  first_name='Jane',
                                  last_name='Doe',
                                  user_photo='images/dog'),
                                  follow_redirects=True)

        self.assertIn(' <h2>Welcome Jane</h2>', result.data)


    


    


   
    

    

        


if __name__ == '__main__':
    import unittest

    unittest.main()
