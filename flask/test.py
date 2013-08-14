'''
Created on Aug 14, 2013

@author: pussbb
'''
import unittest
import api
from flask import json, jsonify


class Test(unittest.TestCase):


    def setUp(self):
        api.app.config.from_object('api.config.TestingConfig')
        self.app = api.app.test_client()
        pass

    def tearDown(self):
        pass


    def test_api_route(self):
        rv = self.app.get('/api/')
        assert rv.status_code == 404

    def test_v01_blueprint(self):
        rv = self.app.get('/api/v.0.1/')
        assert '"commands":' in rv.data

    def test_v01_simple_calls(self):
        rv = self.app.get('/api/v.0.1/users/')
        assert '"api_key"' in rv.data

        rv = self.app.get('/api/v.0.1/users/1')
        assert '"pussbb"' in rv.data

        rv = self.app.get('/api/v.0.1/users/qwqw')
        assert '501: Not Implemented' in rv.data

        rv = self.app.post('/api/v.0.1/users/1')
        assert '501: Not Implemented' in rv.data

        rv = self.app.post('/api/v.0.1/users/')
        assert '"erorrs":' in rv.data and rv.status_code == 200

        rv = self.app.post('/api/v.0.1/users/', data={"login": "test",
                                                      "email": "test@email.net",
                                                      "password": "123456",
                                                      "role_id" : 1,
                                                      })

        assert '"id"' in rv.data and rv.status_code == 200
        data = json.loads(rv.data)

        rv = self.app.put('/api/v.0.1/users/{0}'.format(data['id']))
        assert rv.status_code == 200

        rv = self.app.delete('/api/v.0.1/users/{0}'.format(data['id']))
        assert '"total"'in rv.data and rv.status_code == 200

        rv = self.app.get('/api/v.0.1/users/me')
        assert rv.status_code == 200 and 'hello me' in rv.data

        rv = self.app.delete('/api/v.0.1/users/me')
        assert rv.status_code == 405 and '405: Method Not Allowed' in rv.data

        rv = self.app.delete('/api/v.0.1/languages/3')
        assert rv.status_code == 405 and '405: Method Not Allowed' in rv.data

    def test_v01_conditions(self):
        rv = self.app.get('/api/v.0.1/news/?with=["author"]')
        assert 'api_key' in rv.data

        rv = self.app.get('/api/v.0.1/news/?per_page=2')
        assert '"per_page": 2' in rv.data

        rv = self.app.get('/api/v.0.1/news/?filter={"author_id": [43223,2323,232]}')
        assert '"total": 0' in rv.data

        rv = self.app.get('/api/v.0.1/news/?filter={"author_id": 1}')
        assert '"author_id"' in rv.data

        rv = self.app.get('/api/v.0.1/news/?filter={"created_at":{"comparison_key":">", "value":"2013-04-02"}}')
        assert rv.status_code in (200, 301)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(verbosity=2)

