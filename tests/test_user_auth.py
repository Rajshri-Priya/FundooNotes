from tests.test_setup import TestSetUp


class UserRegistrationTestCase(TestSetUp):
    # Create your tests here.
    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 400)

    def test_user_registration(self):
        user_data = {
            "first_name": "Tanvi",
            "last_name": "Raj",
            "email": "tanvi@gmail.com",
            "address": "vit",
            "phone": "1234567",
            "username": "tanvi1",
            "password": "tanvi1"
        }
        response = self.client.post(self.register_url, data=user_data)
        self.assertEqual(response.status_code, 201)

    def test_user_registration_empty_username_password(self):
        data = {
            "first_name": "Tanvi",
            "last_name": "Raj",
            "email": "tanvi@gmail.com",
            "address": "vit",
            "phone": "1234567",
            "username": "",
            "password": "tanvi"

        }
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 400)

        # *************************************LOGIN*******************************


class LoginTestCase(TestSetUp):

    def test_user_login_success(self):
        # response = self.client.post(self.register_url, data=self.data)
        login_data = {
            'username': 'tanvi',
            'password': 'tanvi'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 201)  # Expect a successful login response

    def test_user_login_invalid_credentials(self):
        # Test a login with invalid credentials
        login_data = {
            'username': 'tanvi',
            'password': 'tanvi12'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 401)  # Expect an unauthorized response

    def test_user_login_missing_fields(self):
        # Test a login with missing fields
        login_data = {
            'username': 'tanvi'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 401)  # Expect a bad request response
