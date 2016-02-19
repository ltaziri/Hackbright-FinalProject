import json
from unittest import TestCase
from model import User, UserGroup, Group, Comment, Invite, connect_to_db, db
# example_data
from server import app
import server
import seed

class FlaskTests(TestCase):

    def setUp(self):

        app.config['SECRET_KEY'] = 'sekrit!'
        # Get the Flask test client
        self.client = app.test_client()

        # self.app = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql://localhost/testdb")

        # Create tables and add sample data
        db.create_all()
        
        seed.load_users()
        seed.load_groups()
        seed.load_usergroups()

        # example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop(usergroups)
        db.drop(groups)
        db.drop(users)
        




    def login(self, username, password, inviteid):
        """Simulate login with inputs"""

        return self.app.post('/sign_in', data=dict(
        username=username,
        password=password,
        inviteid=inviteid),
        follow_redirects=True)


    # def logout(self):
    #     return self.app.get('/log_out', follow_redirects=True)


    def test_login_session(self):
        """Test login session with inputs"""

        rv = self.login('useragmail.com', 'test', None)
        assert flask.session['user_id'] == 1 
        rv = self.login('userbgmail.com', 'wrong', None)
        assert flask.session['user_id'] == False
        rv = self.login('userfgmail.com', 'test', None)
        assert flask.session['user_id'] == False
    

    # def test_login_redirect(self):
    #     """Test login redirects with inputs"""

    #     rv = self.login('useragmail.com', 'test', None)
    #     self.assert_redirects(rv, '/user')
    #     rv = self.login('userbgmail.com', 'wrong', None)
    #     self.assert_redirects(rv, '/') 
    #     # 'Invalid password.' in response.data
    #     rv = self.login('userfgmail.com', 'test', None)
    #     self.assert_redirects(rv, '/sign_up_form') 
        # "You are not signed up yet, please sign up." in response.data

#when testing session have to insert mock secret_key otherwise session will fail. 

# test database insertion and flask routing.

if __name__ == '__main__':
    import unittest

    unittest.main()
