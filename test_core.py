from Flask_API_JWT import app, LOCAL_HOST, DROPBOX_TOKEN, SECRET_KEY, USERS

from flask import json
import unittest, requests, datetime, jwt


def generate_jwt(email, invalid=''):
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    login = {'email' : email, 'dropbox_token': DROPBOX_TOKEN, 'exp' : exp}
    token = jwt.encode(login, SECRET_KEY + invalid).decode('utf-8')
    return  str(token)


def curl(route, file, header, email='wherever'):
    url = LOCAL_HOST + route
    files = {'file': open(file, 'rb')}
    return requests.post(url, files=files, headers=header)


def curlWithToken(route, file):
    url = LOCAL_HOST + route
    files = {'file': open(file, 'rb')}
    header = {'X-Authentication-Token': generate_jwt(USERS[0])}
    return requests.post(url, files=files, headers=header)

def curlWithTokenURL(route, data):
    url = LOCAL_HOST + route
    header = {'X-Authentication-Token': generate_jwt(USERS[0])}
    return requests.post(url, data={'url' : data}, headers=header)


class TestTokenRequiredDecorator(unittest.TestCase):

    routes = ['/excel/info', '/image/convert', '/image/convert/fromdropbox']

    def test_excelInfoWithoutToken(self):
        req = curl(self.routes[0], 'tests/mil.xlsx', {} , USERS[0])
        self.assertEqual({'404' : 'token'}, json.loads(req.content))

    def test_imageConvertWithoutToken(self):
        req = curl(self.routes[1], 'tests/mil.xlsx', {} , USERS[0])
        self.assertEqual({'404' : 'token'}, json.loads(req.content))

    def test_imageConverFromDropBoxtWithoutToken(self):
        req = curl(self.routes[2], 'tests/mil.xlsx', {} , USERS[0])
        self.assertEqual({'404' : 'token'}, json.loads(req.content))

    def test_withoutEmail(self):
        header = {'X-Authentication-Token': generate_jwt('')}
        file = 'tests/mil.xlsx'
        req = curl(self.routes[0], file, header)
        self.assertEqual({'404' : 'email'}, json.loads(req.content))

    def test_invalidToken(self):
        header = {'X-Authentication-Token': generate_jwt(USERS[0], 'adn')}
        file = 'tests/mil.xlsx'
        req = curl(self.routes[0], file, header)
        self.assertEqual({'401' : 'token'}, json.loads(req.content))



class TestExcelInfo(unittest.TestCase):

    route = '/excel/info'

    def setUp(self):
        test = app.test_client()
        self.response = test.get(self.route)

    def test_get(self):
        self.assertEqual(404, self.response.status_code)

    def test_noFile(self):
        url = LOCAL_HOST + self.route
        header = {'X-Authentication-Token': generate_jwt(USERS[0])}
        req = requests.post(url, files="", headers=header)
        self.assertEqual({'404' : 'file'}, json.loads(req.content))

    def test_noExtension(self):
        req = curlWithToken(self.route, 'tests/blank')
        self.assertEqual({'400': 'filename has no extension'}, json.loads(req.content))

    def test_wrongExtension(self):
        req = curlWithToken(self.route, 'README.md')
        self.assertEqual({'400': 'extension not allowed'}, json.loads(req.content))

    def test_usage(self):
        url = 'tests/mil.xlsx'
        req = curlWithToken(self.route, url)
        self.assertEqual('["a","bac","bca","z"]\n', req.text)


class TestImageConvert(unittest.TestCase):

    route = '/image/convert'

    def setUp(self):
        test = app.test_client()
        self.response = test.get(self.route)

    def test_get(self):
        self.assertEqual(404, self.response.status_code)

    def test_noFile(self):
        url = LOCAL_HOST + self.route
        header = {'X-Authentication-Token': generate_jwt(USERS[0])}
        req = requests.post(url, files="", headers=header)
        self.assertEqual({'404' : 'file'}, json.loads(req.content))

    def test_noExtension(self):
        req = curlWithToken(self.route, 'tests/blank')
        self.assertEqual({'400': 'extension not allowed'}, json.loads(req.content))

    def test_wrongExtension(self):
        req = curlWithToken(self.route, 'README.md')
        self.assertEqual({'400': 'extension not allowed'}, json.loads(req.content))

    def test_openImageExcept(self):
        req = curlWithToken(self.route, 'tests/notImage.jpg')
        self.assertEqual({'400': 'is it a image?'}, json.loads(req.content) )

    def test_JPGtoPNG(self):
        req = curlWithToken(self.route, 'tests/rocket.jpg') ##just
        self.assertEqual('image/png', req.headers['Content-Type'] )

    def test_PNGtoJPG(self):
        req = curlWithToken(self.route, 'tests/rocket.png') ##just
        self.assertEqual('image/jpeg', req.headers['Content-Type'] )


class TestImageConvertFromDropBox(unittest.TestCase):

    route = '/image/convert/fromdropbox'

    def setUp(self):
        test = app.test_client()
        self.response = test.get(self.route)

    def test_get(self):
        self.assertEqual(404, self.response.status_code)

    def test_noUrl(self):
        url = LOCAL_HOST + self.route
        header = {'X-Authentication-Token': generate_jwt(USERS[0])}
        req = requests.post(url, files="", headers=header)
        self.assertEqual({'404' : 'url'}, json.loads(req.content))

    def test_urlNotFoundInDropBox(self):
        req = curlWithTokenURL(self.route, 'she/p.png')
        self.assertEqual({'404': 'URL server side'}, json.loads(req.content))


    def test_urlHasNoExtension(self):
        req = curlWithTokenURL(self.route, 'she/p')
        self.assertEqual({"400":"extension not allowed"}, json.loads(req.content))
