import json
import unittest
# from unittest import TestCase
from model import User, UserGroup, Group, Comment, Invite, connect_to_db, db
from server import app
import server
import seed
import os

class FlaskTests(unittest.TestCase):

    def setUp(self):

        print "!!!!!!!!!!!!!!!!!!!!!!! setting up"
        app.config['SECRET_KEY'] = 'sekrit!'
        # Get the Flask test client
        self.client = app.test_client(use_cookies=True)

        # self.app = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()

        # Import different types of data
        seed.load_users()
        seed.load_groups()
        seed.load_usergroups()
        seed.load_patterns()
        
        seed.set_val_user_id()
        seed.set_val_group_id()
        seed.set_val_usergroup_id()
        seed.set_val_pattern_id()

        # db.session.commit()

    def tearDown(self):
        """Do at end of every test."""

        print "!!!!!!!!!!!!!!!!!!!!!!! Tearing down"
        db.session.close()
        db.drop_all()
        # Session.rollback() 


    def test_home(self):
        result = self.client.get('/')
        self.assertIn('<h4> Sign in </h4>', result.data)

   
    def test_login(self):
        return self.client.post('/sign_in', 
                                  data=dict(
                                  email='leilani@hbmail.com',
                                  password='wrong'),
                                  follow_redirects=True)

        self.assertIn('<h4>Sign in</h4>', result.data)

        return self.client.post('/sign_in', 
                                  data=dict(
                                  email='userfgmail.com',
                                  password='test'),
                                  follow_redirects=True)

        self.assertIn('<h2>Sign Up!</h2>', result.data)


        return self.client.post('/sign_in', 
                                  data=dict(
                                  email='leilani@hbmail.com',
                                  password='test'),
                                  follow_redirects=True)

        self.assertIn('<h3> Your craft groups:</h3>', result.data)


    def test_sign_up_form(self):
        result = self.client.get('/sign_up_form')
        self.assertIn('<h2>Sign Up!</h2>', result.data)

    
    # def test_logout(self):
    #     result = self.client.get('/log_out')
    #     self.assertIn('<h4> Sign in </h4>', result.data)


    def test_sign_up(self):
        return self.client.post('/sign_up', 
                                  data=dict(
                                  email='leilani@hbmail.com',
                                  password='test',
                                  first_name='Leilani',
                                  last_name='Taziri',
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

        self.assertIn('<h3> Your craft groups:</h3>', result.data)


    


    


   
    

    

        


if __name__ == '__main__':
    import unittest

    unittest.main()
