import json
import unittest
from model import User, UserGroup, Group, Comment, Invite, connect_to_db, db
from server import app
import server
import seed
import os
from flask import session


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
        seed.load_invites()
        
        # Reset auto incrementing primary keys to start after seed data
        seed.set_val_user_id()
        seed.set_val_group_id()
        seed.set_val_usergroup_id()
        seed.set_val_pattern_id()
        seed.set_val_invite_id()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


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
        """Test sign up form to make sure you have to enter a lastname"""
        
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
    """Tests for MakeAlong app for functions that require session data."""

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
        seed.load_invites()
        
        seed.set_val_user_id()
        seed.set_val_group_id()
        seed.set_val_usergroup_id()
        seed.set_val_pattern_id()
        seed.set_val_invite_id()

        with self.client as c:
                with c.session_transaction() as sess:
                    sess['user_id'] = 1
                c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_correct_group_for_user(self):
        """Test that the correct groups are showing on user homepage"""

        result = self.client.get('/user', follow_redirects=True)
    
        self.assertEqual(result.status_code, 200)
        self.assertIn('Knitters to the rescue!', result.data)


    def test_open_invite_msg(self):
        """Test that open invite msgs are appearing on homepage"""

        result = self.client.get('/user', follow_redirects=True)
    
        self.assertEqual(result.status_code, 200)
        self.assertIn('Terri has invited you to join:', result.data)


    def test_confirm_invite(self):
        """Test that group info json is being returned to html after confirming invite"""

        return self.client.post('/invite_confirm.json', 
                                  data={'invite_id':1,},
                                  follow_redirects=True)
  
        self.assertIn('group_id:4', result.data)


    def test_show_group_form(self):
        """Test to see if group form page renders"""

        result = self.client.get('/group_form', follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('<h2>Create a Group!</h2>', result.data)


    def test_user_profile_update(self):
        """Test that user profile is updating correctly"""

        return self.client.post('/user_profile_update', 
                                  data={'user_descrip':"new info",},
                                  follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('Your profile has been updated!', result.data)


    def test_create_group_no_pattern(self):
        """Test that a group can be created with no pattern"""

        return self.client.post('/create_group', 
                                  data={'group_name':"New Group",
                                        'group_descrip':"Fun Group",
                                        'hashtag':"",
                                        'group_image':'static/images/craft_group_default.jpg'},
                                        follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('New Group', result.data)
        self.assertIn('Fun Group', result.data)


    def test_create_group_with_pattern_no_poll(self):
        """Test that a group with a pattern, no poll, can be created"""

        return self.client.post('/create_group', 
                                  data={'group_name':"New Group",
                                        'group_descrip':"Fun Group",
                                        'hashtag':"",
                                        'group_image':'static/images/craft_group_default.jpg',
                                        'pattern_name':'Chosen Pattern'},
                                        follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('Chosen Pattern', result.data)


    def test_create_group_with_poll(self):
        """Test that a group with a poll can be created"""

        return self.client.post('/create_group', 
                                  data={'group_name':"New Group",
                                        'group_descrip':"Fun Group",
                                        'hashtag':"",
                                        'group_image':'static/images/craft_group_default.jpg',
                                        'vote_days':5,
                                        'pattern_name_a':'Pattern A',
                                        'pattern_name_b':'Pattern B'},
                                        follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('Days Left to Vote on a Pattern', result.data)


    def test_group_correct_user(self):
        """Test if user can go to group page based on session user data"""

        result = self.client.get('/group_home/1', follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('Welcome to Knitters to the rescue!', result.data)


    def test_group_incorrect_user(self):
        """Test that user can't go to group page based on session user data"""

        result = self.client.get('/group_home/4', follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h3> Your craft groups:</h3>', result.data)


    def test_show_group_profile_form_group_admin(self):
        """Test if group profile form shows for admin"""

        result = self.client.get('/group_profile_form/2', follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('<p>Currently:<i> Super Sewers</i></p>', result.data)


    def test_show_group_profile_form_group_member_no_admin(self):
        """Test if group profile form shows for group member, not the admin"""

        result = self.client.get('/group_profile_form/5', follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('Welcome to Modern Quilters', result.data)


    def test_show_group_profile_form_non_group_member(self):
        """Test if group profile form shows non group member"""

        result = self.client.get('/group_profile_form/4', follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('Your craft groups:', result.data)


    # group update tests will go here

    def test_poll_votes(self):
        """Test if correct poll count is being sent to template""" 
        pass
        

    def test_logout(self):
        """Test if user can logout"""

        result = self.client.get('/log_out', follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h4> Sign in </h4>', result.data)
      

   

if __name__ == '__main__':
    import unittest

    unittest.main()
