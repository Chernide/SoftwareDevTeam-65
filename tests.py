import os
import app as ap
import unittest
import tempfile
import json

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        ap.app.testing = True
        self.app = ap.app.test_client()
        self.authKey = ''

    def tearDown(self):
        pass
    
    def test_root(self):
        rv = self.app.get('/')
        print("Testing root")
        assert b"This probably isn't what you want.\n Try /getPoliticians/YOUR_ZIP for a list of your local politicians" in rv.data

    def test_unauth_access(self):
        print("Testing unauthorized access to getPoliticians")
        resp = self.app.get('/getPoliticians', query_string={'city': 'Boulder', 'state': 'CO'})
        assert b"Missing Authorization Header" in resp.data
    
    def test_invalid_signup(self):
        print("Testing invalid signup")
        resp = self.app.post('/signup', data=json.dumps({'email': "test@test.com"}), content_type='application/json')
        assert b"Email/password not provided" in resp.data
    
    def test_valid_signup(self):
        print("Testing valid signup")
        resp = self.app.post('/signup', data=json.dumps({'email': "test@test.com", "password": "password"}), content_type='application/json')
        assert b"Account already taken" in resp.data or b"token" in resp.data
    
    def test_partial_login(self):
        print("Testing invalid login - invalid pswd")
        resp = self.app.post('/login', data=json.dumps({'email': "austinattempt@gmail.com", 'password': 'password'}), content_type='application/json')
        assert b"Invalid credentials" in resp.data
    
    def test_no_user_login(self):
        print("Testing invalid login - no username")
        resp = self.app.post('/login', data=json.dumps({'email': "thisdoesntexist", 'password': 'password'}), content_type='application/json')
        assert b"User not found" in resp.data
    
    def test_valid_login(self):
        print("Testing valid login")
        resp = self.app.post('/login', data=json.dumps({'email': "austinattempt@gmail.com", 'password': 'surehopethisworks'}), content_type='application/json')
        assert b"token" in resp.data
    
    def test_auth_access(self):
        resp = self.app.post('/login', data=json.dumps({'email': "austinattempt@gmail.com", 'password': 'surehopethisworks'}), content_type='application/json')
        assert b"token" in resp.data

        stringResp = resp.data.decode('utf-8')
        authKey = json.loads(stringResp)['token']

        print("Testing authorized access to getPoliticians with token " + authKey)
        
        # Valid request
        resp = self.app.get('/getPoliticians', query_string={'city': 'Boulder', 'state': 'CO'}, headers={'Authorization': ('Bearer ' + authKey)})
        assert b"President of the United States" in resp.data and b"Boulder" in resp.data

        # Invalid request
        print("Testing authorized invalid request to getPoliticians with token " + authKey)
        resp = self.app.get('/getPoliticians', query_string={'city': 'Boulder', 'state': 'NZ'}, headers={'Authorization': ('Bearer ' + authKey)})
        assert b"Failed to parse address" in resp.data

        resp = self.app.get('/getPoliticians', query_string={'city': 'Boulder'}, headers={'Authorization': ('Bearer ' + authKey)})
        assert b"Invalid parameters" in resp.data

    def test_db_query(self):
        resp = self.app.post('/getFedReps', query_string={'state': 'CO'})
        assert b"President of the United States" in resp.data and b"House" in resp.data
    
    def test_invalid_db_query(self):
        resp = self.app.post('/getFedReps', query_string={'state': 'NZ'})
        assert b"Invalid state code" in resp.data

if __name__ == '__main__':
    unittest.main()