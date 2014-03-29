"""
Created on Aug 14, 2013

@author: pussbb
"""
import unittest
import api
from flask import json
import simplexml


class Test(unittest.TestCase):

    def setUp(self):
        api.app.config.from_object('api.config.TestingConfig')
        self.app = api.app.test_client()

    def tearDown(self):
        pass

    def to_json(self, data):
        return json.loads(data)

    def test_api_route(self):
        rv = self.app.get('/api/')
        assert rv.status_code == 403

    def test_v01_blueprint(self):
        rv = self.app.get('/api/v.0.1/')
        assert rv.status_code == 200
        data = self.to_json(rv.data)
        self.assertIsInstance(data, dict)
        self.assertIn('commands', data)

    def test_v01_response_format(self):
        rv = self.app.get('/api/v.0.1/users/',
                          headers={"accept": "application/xml"})
        self.assertIsNotNone(simplexml.loads(rv.data))

        rv = self.app.get('/api/v.0.1/users/',
                          headers={"accept": "application/json"})
        self.assertIsNotNone(json.loads(rv.data))

    def test_v01_simple_calls(self):
        rv = self.app.get('/api/v.0.1/users/')
        self.assertIn('records', self.to_json(rv.data))
        self.assertIsNotNone(self.to_json(rv.data)['records'])

        rv = self.app.get('/api/v.0.1/users/1')
        self.assertIn('email', self.to_json(rv.data))
        self.assertEqual('pussbb', self.to_json(rv.data)['login'])

        rv = self.app.get('/api/v.0.1/users/qwqw')
        self.assertEqual(rv.status_code, 501)

        rv = self.app.post('/api/v.0.1/users/1')
        self.assertEqual(rv.status_code, 501)

        rv = self.app.post('/api/v.0.1/users/')

        self.assertIn('errors', self.to_json(rv.data))
        self.assertEqual(rv.status_code, 400)

        post_data = {"login": "test",
                     "email": "test@email.net",
                     "password": "123456",
                     "role_id": 1}

        rv = self.app.post('/api/v.0.1/users/', data=post_data)
        self.assertEqual(rv.status_code, 201)
        data = self.to_json(rv.data)
        self.assertIn('id', data)

        rv = self.app.put('/api/v.0.1/users/{0}'.format(data['id']),
                          data={'login': 'test2'})
        self.assertEqual(rv.status_code, 202)

        rv = self.app.delete('/api/v.0.1/users/{0}'.format(data['id']))
        self.assertEqual(rv.status_code, 204)

        rv = self.app.get('/api/v.0.1/users/me')
        self.assertEqual(rv.status_code, 200)

        rv = self.app.delete('/api/v.0.1/users/me')
        self.assertEqual(rv.status_code, 405)

        rv = self.app.delete('/api/v.0.1/languages/3')
        self.assertEqual(rv.status_code, 405)

    def test_v01_conditions(self):
        rv = self.app.get('/api/v.0.1/news/?with=["author"]')
        self.assertIn('records', self.to_json(rv.data))
        self.assertIn('author', self.to_json(rv.data)['records'][0])

        rv = self.app.get('/api/v.0.1/news/?per_page=2')
        self.assertIn('per_page', self.to_json(rv.data))
        self.assertEqual(self.to_json(rv.data)['per_page'], 2)

        rv = self.app.get('/api/v.0.1/news/'
                          '?filter={"author_id": [43223,2323,232]}')
        self.assertIn('total', self.to_json(rv.data))
        self.assertEqual(self.to_json(rv.data)['total'], 0)

        rv = self.app.get('/api/v.0.1/news/?filter={"author_id": 1}')
        self.assertIn('records', self.to_json(rv.data))
        self.assertIn('author_id', self.to_json(rv.data)['records'][0])

        rv = self.app.get('/api/v.0.1/news/?filter='
                          '{"created_at":{"comparison_key":">", '
                          '"value":"2013-04-02"}}')
        self.assertIn(rv.status_code, (200, 301))

if __name__ == "__main__":
    unittest.main(verbosity=2)

