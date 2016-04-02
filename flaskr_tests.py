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
        """Test to see if the sign up page comes up."""

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

        #sign in field on homepage
        self.assertIn('<h2>Please Sign In</h2>', result.data)

        #make sure a new user wasn't created
        self.assertNotIn('<h3> Your craft groups:</h3>', result.data)

        #flash message, on homepage
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
        #header on user homepage
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

        # make sure js validation did not allow form submit and still on sign up page
        self.assertIn('<h2>Sign Up!</h2>', result.data)

        # make sure a user wasn't created and redirected to user homepage
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

        # make sure js validation did not allow form submit and still on sign up page
        self.assertIn('<h2>Sign Up!</h2>', result.data)

        # make sure a user wasn't created and redirected to user homepage
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

        # make sure js validation did not allow form submit and still on sign up page
        self.assertIn('<h2>Sign Up!</h2>', result.data)

        # make sure a user wasn't created and redirected to user homepage
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

        # make sure js validation did not allow form submit and still on sign up page
        self.assertIn('<h2>Sign Up!</h2>', result.data)

        # make sure a user wasn't created and redirected to user homepage
        self.assertNotIn('<h3> Your craft groups:</h3>', result.data) 


    def test_login_correct(self):
        """Tests to see current user can login with correct info"""

        return self.client.post('/sign_in', 
                                  data={'email':'leilani@hbmail.com',
                                        'password':'test'},
                                  follow_redirects=True)

       # make sure a user is redirected to user homepage 
        self.assertIn('<h3> Your craft groups:</h3>', result.data)


    def test_login_incorrect(self):
        """Tests to see current user can not login with incorrect info"""

        return self.client.post('/sign_in', 
                                  data={'email':'leilani@hbmail.com',
                                        'password':'wrong'},
                                  follow_redirects=True)

        # make sure a user is redirected to homepage to try to sign in again
        self.assertIn('<h4>Sign in</h4>', result.data)

        # make sure a user wasn't redirected to user homepage
        self.assertNotIn('<h3> Your craft groups:</h3>', result.data


    def test_login_new_user(self):
        """Tests to see if new user gets sent to sign up page"""

        return self.client.post('/sign_in', 
                                  data={'email':'userfgmail.com',
                                        'password':'test'},
                                  follow_redirects=True)

        # make sure a user is redirected to sign up page if they don't have an account
        self.assertIn('<h2>Sign Up!</h2>', result.data)


class FlaskTestsSessions(unittest.TestCase):
    """Tests for MakeAlong app for functions that require session data."""

    def setUp(self):
        """Do before every test"""
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
        """Test that unconfirmed invite msgs are appearing on homepage"""

        result = self.client.get('/user', follow_redirects=True)
    
        self.assertEqual(result.status_code, 200)
        self.assertIn('Terri has invited you to join:', result.data)


    def test_confirm_invite(self):
        """Test that group info json is being returned to html after confirming invite"""

        return self.client.post('/invite_confirm.json', 
                                  data={'invite_id':1,},
                                  follow_redirects=True)
        
        # Make sure a group div for the group the user just accepted the invite
        # for is now showing up on the user page 
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


    def test_group_correct_user(self):
        """Test if user can go to group page based on session user data"""

        result = self.client.get('/group_home/1', follow_redirects=True)
        
        #The logged in user is part of this group
        self.assertEqual(result.status_code, 200)
        self.assertIn('Welcome to Knitters to the rescue!', result.data)


    def test_group_incorrect_user(self):
        """Test that user can't go to group page based on session user data"""

        result = self.client.get('/group_home/4', follow_redirects=True)
        
        #The logged in user is not part of this group, test that they are 
        #redirected back to their user homepage
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h3> Your craft groups:</h3>', result.data)


    def test_show_group_profile_form_non_group_member(self):
        """Test if group profile form shows non group member"""

        result = self.client.get('/group_profile_form/4', follow_redirects=True)
        
        #The logged in user is not part of this group, test that they are 
        #redirected back to their user homepage
        self.assertEqual(result.status_code, 200)
        self.assertIn('Your craft groups:', result.data)
    

    def test_send_invite(self):
        """Test if email invite is added to the database"""

        result = self.client.post('/send_invite/1',

                                  data={'name' : "Leilani",
                                        'email':"test@hbmail.com",
                                        'text': "Come join my group!"},
                                        follow_redirects=True)

        # Flash message that appears after the invite has been added to the 
        # database
        self.assertEqual(result.status_code, 200)
        self.assertIn('Invitation sent!', result.data)


    def test_logout(self):
        """Test if user can logout"""

        result = self.client.get('/log_out', follow_redirects=True)
        
        # Logged out and returned to the homepage
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h4>Sign in</h4>', result.data)
      

class FlaskTestMakeGroupsUpdateGroups(unittest.TestCase):
    """Tests for MakeAlong app for making groups or updating groups without polls."""

    def setUp(self):
        """Do at the beginning of every test"""
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

        with self.client as c:
                with c.session_transaction() as sess:
                    sess['user_id'] = 1
                c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
   

    def test_create_group_no_pattern(self):
        """Test that a group can be created with no pattern"""

        return self.client.post('/create_group', 
                                  data={'group_name':"New Group",
                                        'group_descrip':"Fun Group",
                                        'hashtag':"",
                                        'group_image':'static/images/craft_group_default.jpg'},
                                        follow_redirects=True)

        #Group was created without a pattern and redirected to new group page
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

        #Group was created with a set pattern and redirected to new group page
        self.assertEqual(result.status_code, 200)
        self.assertIn('Chosen Pattern', result.data)


    def test_show_group_profile_form_group_admin(self):
        """Test if group profile form shows for admin"""

        result = self.client.get('/group_profile_form/2', follow_redirects=True)
        
        # Admin is logged in and should be able to get to this form page
        self.assertEqual(result.status_code, 200)
        self.assertIn('<p>Currently:<i> Super Sewers</i></p>', result.data)


    def test_show_group_profile_form_group_member_no_admin(self):
        """Test if group profile form shows for group member, not the admin"""

        result = self.client.get('/group_profile_form/5', follow_redirects=True)
        
        # Admin is not logged in and should not be able to get to the form page
        # instead they should be redirected to the group page
        
        # Form page
        self.assertNotIn('<p>Currently:<i> Modern Quilters</i></p>', result.data)

        #Group page for correct redirect
        self.assertEqual(result.status_code, 200)
        self.assertIn('Welcome to Modern Quilters', result.data)



    def test_update_group_name(self):
        """Test that a group name can be updated"""

        return self.client.post('/group_profile_update/1', 
                                  data={'group_name':"New Group Name",
                                        'group_descrip':"",
                                        'hashtag':"",
                                        'group_image':"",},
                                        follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('Welcome to New Group Name', result.data)


    def test_update_group_description(self):
        """Test that a group description can be updated"""

        return self.client.post('/group_profile_update/1', 
                                  data={'group_name':"",
                                        'group_descrip':"New description!",
                                        'hashtag':"",
                                        'group_image':"",},
                                        follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('New description!', result.data)


    def test_update_group_hashtag(self):
        """Test that a group hashtag can be updated"""

        return self.client.post('/group_profile_update/1', 
                                  data={'group_name':"",
                                        'group_descrip':"",
                                        'hashtag':"newhashtag",
                                        'group_image':"",},
                                        follow_redirects=True)

        #Server should add the #makealong prefix prior to storing in the database
        self.assertEqual(result.status_code, 200)
        self.assertIn('#makealongnewhashtag', result.data)


    def test_update_pattern_name(self):
        """Test that a group pattern name can be updated"""

        return self.client.post('/group_profile_update/1', 
                                  data={'group_name':"",
                                        'group_descrip':"",
                                        'hashtag':"",
                                        'group_image':"",
                                        'update_pattern_name':"New Pattern Name"},
                                        follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('New Pattern Name', result.data)


    def test_update_pattern_link(self):
        """Test that a group pattern link can be updated"""

        return self.client.post('/group_profile_update/2', 
                                  data={'group_name':"",
                                        'group_descrip':"",
                                        'hashtag':"",
                                        'group_image':"",
                                        'update_pattern_link':"https://www.ravelry.com/"},
                                        follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('<a href="https://www.ravelry.com/" target="blank">', result.data)


    def test_update_add_pattern_with_name(self):
        """Test that a group pattern without a link can be added to a group that didn't have one"""

        return self.client.post('/group_profile_update/2', 
                                  data={'group_name':"",
                                        'group_descrip':"",
                                        'hashtag':"",
                                        'group_image':"",
                                        'new_pattern_name':"New Pattern"},
                                        follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('This month we are working on New Pattern', result.data)


    def test_update_add_pattern_with_link(self):
        """Test that a group pattern with a link can be added to a group that didn't have one"""

        return self.client.post('/group_profile_update/2', 
                                  data={'group_name':"",
                                        'group_descrip':"",
                                        'hashtag':"",
                                        'group_image':"",
                                        'new_pattern_name':"New Pattern",
                                        'new_pattern_link':"https://www.ravelry.com/"},
                                        follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('<a href="https://www.ravelry.com/" target="blank">', result.data)


class FlaskTestGroupPoll(unittest.TestCase):
    """Tests for MakeAlong group poll created at group creation."""

    @classmethod
    def setUp(cls):
        """Do once before all tests in this class"""
        # Get the Flask test client
        cls.client = app.test_client()

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

        with cls.client as c:
                with c.session_transaction() as sess:
                    sess['user_id'] = 1
                c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')

    @classmethod
    def tearDown(cls):
        """Do after all tests have run."""

        db.session.close()
        db.drop_all()



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

        # Test that poll clock is showing up
        self.assertEqual(result.status_code, 200)
        self.assertIn('Days Left to Vote on a Pattern', result.data)


    def test_poll_votes(self):
        """Test if correct poll count is being sent to the client""" 
        
        return self.client.get('/poll.json/4', follow_redirects=True)

        # Test that correct vote count is being returned and rendered by the client
        self.assertIn('Pattern A:0', result.data)
        self.assertIn('Pattern B:0', result.data)


    def test_add_vote(self):
        """Test if admin final confirmation buttons are showing after all votes are in""" 
        
        return self.client.get('/update_poll.json',
                                data={'group_id':4,
                                      'pattern_id':4},
                                      follow_redirects=True)

        # Vote data
        self.assertIn('Pattern A:1', result.data)
        self.assertIn('Pattern B:0', result.data)

        # Admin final confirmation buttons
        self.assertIn('<label><b>Pattern A</label></b>', result.data)
        self.assertIn('<label><b>Pattern B</label></b>', result.data)


    def test_final_vote(self):
        """Test final vote from admin and finalization of poll"""

        return self.client.get('/final_vote/4',
                                data={'final_vote_submit':"4"},
                                      follow_redirects=True)

        # Test that poll in no longer showing after admin confirmation
        self.assertIn('This month we are working on Pattern A', result.data)


class FlaskTestComments(unittest.TestCase):
    """Tests for MakeAlong group comments."""

    @classmethod
    def setUp(cls):
        """Do once before all tests in this class"""
        # Get the Flask test client
        cls.client = app.test_client()

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

        with cls.client as c:
                with c.session_transaction() as sess:
                    sess['user_id'] = 1
                c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')

    @classmethod
    def tearDown(cls):
        """Do after all tests have run."""

        db.session.close()
        db.drop_all()


    def test_comment_ajax_text(self):
        """Test ajax handling of comment containing text"""

        return self.client.get('/comment_add.json',
                                data={'group_id':"1",
                                      'comment_text':"This is a new commment"},
                                      follow_redirects=True)

        # Test that text comment is being rendered in browser after ajax call
        self.assertIn("<div class='comment_text'> This is a new comment</div>", result.data)


    def test_comment_ajax_link(self):
        """Test ajax handling of comment containing text"""

        return self.client.get('/comment_add.json',
                                data={'group_id':"1",
                                      'comment_text':"This comment has a link https://www.ravelry.com/"},
                                      follow_redirects=True)

        # Test that link in text comment was correctly turned into a link by the
        # server and is being rendered correctly in the browser after ajax call
        self.assertIn("<a href ='https://www.ravelry.com/'>", result.data)


    def test_comment_ajax_youtube(self):
        """Test ajax handling of comment containing text"""

        return self.client.get('/comment_add.json',
                                data={'group_id':"1",
                                      'comment_text':"This is a youtube link https://www.youtube.com/watch?v=IGITrkYdjJs"},
                                      follow_redirects=True)

        # Test that youtube link in text comment was correctly turned into an 
        # iframe preview window with the correct youtube id after ajax call
        self.assertIn("<iframe width='300' height='300' src='http://www.youtube.com/embed/IGITrkYdjJs?autoplay=0'>", result.data)


    def test_comment_text_server(self):
        """Test text comment is rendering correctly from server"""

        return self.client.get('/group_home/1',
                                data={'group_id':"1"},
                                      follow_redirects=True)

        # Test that previously rendered, in browser comment, shows correctly 
        # after refresh
        self.assertIn("<div class='comment_text'> This is a new comment</div>", result.data)


    def test_comment_link_server(self):
        """Test ajax handling of comment containing text"""

        return self.client.get('/group_home/1',
                                data={'group_id':"1"},
                                      follow_redirects=True)

        # Test that previously rendered, in browser comment, shows correctly 
        # after refresh
        self.assertIn("<a href ='https://www.ravelry.com/'>", result.data)


    def test_comment_ajax_youtube(self):
        """Test ajax handling of comment containing text"""

        return self.client.get('/group_home/1',
                                data={'group_id':"1"},
                                      follow_redirects=True)
        
        # Test that previously rendered, in browser comment, shows correctly 
        # after refresh
        self.assertIn("<iframe width='300' height='300' src='http://www.youtube.com/embed/IGITrkYdjJs?autoplay=0'>", result.data)


if __name__ == '__main__':
    import unittest

    unittest.main()
