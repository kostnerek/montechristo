import unittest
import requests
import json
from sqlalchemy import text, create_engine
#from ..models.User.UserModel import UserModel


class TestUserRes(unittest.TestCase):
    def setUp(self):  # Prepare test environment
        self.engine = create_engine('sqlite:///app/db.sqlite')
        self.conn = self.engine.connect()
        
        self.valid_user1 = {
            "username": "test_user1",
            "mail": "test1@test.com",
            "password": "zaq1@WSX"
        }
        self.valid_user1 = json.dumps(self.valid_user1, indent = 4) 
        
        """ non valid username """
        self.non_valid_username = json.dumps({
            "username": "te",
            "mail": "test3@test.com",
            "password": "zaq1@WSX"
        })
        
        """ non valid mail """
        self.non_valid_mail = json.dumps({
            "username": "test_user3",
            "mail": "test3@test",
            "password": "zaq1@WSX"
        })
        """ non valid password """
        self.non_valid_password = json.dumps({
            "username": "test_user4",
            "mail": "test4@test.com",
            "password": "zaq"
        })
        """ existing username """
        self.existing_username = json.dumps({
            "username": "test_user1",
            "mail": "test5@test.com",
            "password": "zaq1@WSX"
        })
        """ existing mail """
        self.existing_mail = json.dumps({
            "username": "test_user5",
            "mail": "test1@test.com",
            "password": "zaq1@WSX"
        })

    
    def test1_user_creation(self):
        response = requests.post('http://localhost:5000/api/register', data=self.valid_user1, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        
    def test2_user_get(self):
        response = requests.get('http://localhost:5000/api/user/1')
        self.assertEqual(response.status_code, 200)
    
    def test3_if_user_created_in_db(self):
        user = self.engine.execute(text("SELECT * FROM users WHERE username = 'test_user1'")).fetchone()
        check = True if user else False
        self.assertEqual(check, True)
    
    def test4_if_non_valid_username(self):
        response = requests.post('http://localhost:5000/api/register', data=self.non_valid_username, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test5_if_non_valid_mail(self):
        response = requests.post('http://localhost:5000/api/register', data=self.non_valid_mail, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)
    
    def test6_if_non_valid_password(self):
        response = requests.post('http://localhost:5000/api/register', data=self.non_valid_password, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)
    
    def test7_if_exising_username(self):
        response = requests.post('http://localhost:5000/api/register', data=self.non_valid_username, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)
        
    def test8_if_exising_mail(self):
        response = requests.post('http://localhost:5000/api/register', data=self.non_valid_mail, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)
    
    def test9_logging_in(self):
        logging_creds=json.dumps({
            "username":"test_user1",
            "password":"zaq1@WSX"
        })
        response = requests.post('http://localhost:5000/api/login', data=logging_creds, headers={'Content-Type': 'application/json'})
        access_token=response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(access_token), 0)    
        self.assertGreater(len(refresh_token), 0) 
    
    def test10_logging_out(self):
        logging_creds=json.dumps({
            "username":"test_user1",
            "password":"zaq1@WSX"
        })
        response = requests.post('http://localhost:5000/api/login', data=logging_creds, headers={'Content-Type': 'application/json'})
        access_token=response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        
        response_logout = requests.delete('http://localhost:5000/api/logout', 
                                        headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}, 
                                        data=json.dumps({"refresh_token": refresh_token})
                                        )
        self.assertEqual(response_logout.status_code, 200)

    def test11_user_delete(self):
        response = requests.delete('http://localhost:5000/api/user/1')
        self.assertEqual(response.status_code, 200)
    
        
    def tearDown(self):  # Cleanup after test
        response = requests.delete('http://localhost:5000/api/user/1')

#unittest.main()
if __name__ == '__main__':
    unittest.main()