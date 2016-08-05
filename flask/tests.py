import main
import unittest

from mongoengine import *

from subprocess import check_call, CalledProcessError

class AthenaTestCase(unittest.TestCase):
    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

        # Start MongoDB
        try:
            check_call('brew services start mongodb', shell=True)
            self.db = connect(main.app.config['MONGODB_NAME'])
        except CalledProcessError as cpe:
            print 'Unable to start MongoDB.'

    def tearDown(self):
        self.db.drop_database(main.app.config['MONGODB_NAME'])

        # Stop MongoDB
        try:
            check_call('brew services stop mongodb', shell=True)
        except CalledProcessError as cpe:
            print 'Unable to stop MongoDB.'

    def register(self, name, username, password):
        return self.app.post('/register', data=dict(
            fullname=name,
            username=username,
            password=password
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_register_login_logout(self):
        rv = self.register('User Pass', 'user', 'pass')
        assert 'Thank you for creating an account! Please log in with your credentials.' in rv.data
        rv = self.register('User Pass', 'user', 'pass')
        assert 'Username taken' in rv.data
        rv = self.login('user', 'pass')
        assert 'Logged in' in rv.data
        rv = self.logout()
        assert 'Not logged in' in rv.data

if __name__ == '__main__':
    unittest.main()