import unittest
import requests
import json


class TestStringMethods(unittest.TestCase):
    
    def test_del_not_real(self):
        s = requests.session()
        data = {"key": "sfs"}
        data = json.dumps(data)
        req = s.delete('http://127.0.0.1:65430/delete', data = data)
        self.assertEqual(json.loads(req.text)["status"], 'Not Found')
    
    def test_bad_put(self):
        s = requests.session()
        data = {
            "key": "test"
            }
        data = json.dumps(data)
        req = s.put('http://127.0.0.1:65430/put', data = data)
        self.assertEqual(req.status_code, 403)
    
    def test_good_put(self):
        s = requests.session()
        data = {
            "key": "test",
            "message": "1"
        }
        data = json.dumps(data)
        req = s.put('http://127.0.0.1:65430/put', data = data)
        self.assertEqual(json.loads(req.text)["status"], 'Create')
            
    def test_del_real(self):
        s = requests.session()
        data = {"key": "test"}
        data = json.dumps(data)
        req = s.delete('http://127.0.0.1:65430/delete', data = data)
        self.assertEqual(json.loads(req.text)["status"], 'OK')

    # Выше добавил тесты более простых случаев...Не вижу смысла избавляться от старых тестов, которые ниже, плюс два из трех тестов выше тестируют "плохие" случаи
    
    def test_put_and_get(self):
        s = requests.session()
        data = {
            "key": "sfs",
            "message": "1"
                }
        data = json.dumps(data)
        req = s.put('http://127.0.0.1:65430/put', data = data)
        data = {"key": "sfs"}
        data = json.dumps(data)
        req1 = s.get('http://127.0.0.1:65430/get', data = data)
        self.assertEqual(json.loads(req1.text)["message"], '1')

    def test_put_del(self):
        s = requests.session()
        data = {
            "key": "sfs",
            "message": "1"
            }
        data = json.dumps(data)
        req = s.put('http://127.0.0.1:65430/put', data = data)
        data = {"key": "sfs"}
        data = json.dumps(data)
        req1 = s.delete('http://127.0.0.1:65430/delete', data = data)
        self.assertEqual(json.loads(req1.text)['status'], 'OK')


if __name__ == '__main__':
    unittest.main()
