from urlparse import urlparse, parse_qs
from httpretty import httpretty, httprettified
from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model

class AppsfuelTestCase(TestCase):
    @httprettified
    def test_functional(self):
        response = self.client.get('/auth/login/appsfuel/')
        self.assertEqual(response.status_code, 302)
        location = urlparse(response['Location'])
        self.assertEqual(location.hostname, 'app.appsfuel.com')
        self.assertEqual(location.path, '/content/permission')
        qs = parse_qs(location.query)
        self.assertEqual(qs.keys(), ['state', 'redirect_uri', 'response_type', 'client_id'])
        self.assertTrue(qs['redirect_uri'][0].startswith('http://testserver/auth/complete/appsfuel/?redirect_state='))
        self.assertEqual(qs['response_type'][0], 'code')
        self.assertEqual(qs['client_id'][0], settings.APPSFUEL_CLIENT_ID)
        httpretty.register_uri(
            method=httpretty.POST,
            uri='https://api.appsfuel.com/v1/live/oauth/token',
            body='{"status" : "ok", "access_token" : "<access-token>",  "expire_in" : 28800}',
            content_type="application/json",
        )
        httpretty.register_uri(
            method=httpretty.GET,
            uri='https://api.appsfuel.com/v1/live/user?access_token=%3Caccess-token%3E',
            body='{"user_id": "<user-id>", "is_paid": false, "status":"ok", "display_name": "Im A Test", "email": "test@testserver.com"}',
            content_type="application/json",
        )
        response = self.client.get(qs['redirect_uri'][0] + '&code=imareqtoken')
        self.assertEqual(len(httpretty.latest_requests), 2)
        self.assertEqual(parse_qs(httpretty.latest_requests[0].body).keys(), ['client_secret', 'code', 'redirect_uri', 'client_id', 'grant_type'])
        self.assertEqual(httpretty.latest_requests[1].body, '')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/accounts/profile/')
        user = get_user_model().objects.get()
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.first_name, 'Im A Test')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.email, 'test@testserver.com')
