import unittest
import time

from django.core.exceptions import ImproperlyConfigured

from .helpers import create_database_wrapper_instance
from django_database_postgresql_aad_backend.base import DatabaseWrapper, DEFAULT_REFRESH_BEFORE_MINUTES


class TestDatabaseWrapper(unittest.TestCase):

    def test_get_token_if_expired_with_invalid_token(self):
        """
        Test function responsible for getting access token from Azure when current token is invalid
        """
        test_cases = [
            {
                "name": "No token is present, we should fetch a new token",
                "old_token": None,
                "old_expires_on": None,
                "new_token": "token1",
                "new_expires_on": time.time() + 60 * DEFAULT_REFRESH_BEFORE_MINUTES,
                "raise_error_when_get_access_token": False,
                "settings_dict": None
            },
            {
                "name": "An expired token is present, we should fetch a new token",
                "old_token": "mytoken",
                "old_expires_on": time.time() - 60 * (DEFAULT_REFRESH_BEFORE_MINUTES + 4),
                "new_token": "token2",
                "new_expires_on": time.time() + 60 * DEFAULT_REFRESH_BEFORE_MINUTES,
                "raise_error_when_get_access_token": False,
                "settings_dict": None
            }
        ]
        for case in test_cases:
            with self.subTest(name=case["name"]):
                database_wrapper = create_database_wrapper_instance(
                    case["old_token"], case["old_expires_on"], case["new_token"], case["new_expires_on"],
                    case["raise_error_when_get_access_token"], case["settings_dict"]
                    )
                database_wrapper.get_token_if_expired("tenant id", "client id", "client secret", "scope")
                self.assertEqual(database_wrapper.token, case["new_token"])
                self.assertEqual(database_wrapper.expires_on, case["new_expires_on"])
                self.assertTrue(database_wrapper.logger.logger_called)
                self.assertTrue("No valid token, token will be requested." in database_wrapper.logger.info_messages)
                self.assertTrue("Token was set." in database_wrapper.logger.info_messages)

    def test_get_token_if_expired_with_valid_token(self):
        """
        Test function responsible for getting access token from Azure when current token is still valid
        """
        test_cases = [
            {
                "name": "Token is present and is valid",
                "old_token": "token",
                "old_expires_on": time.time() + 60 * (DEFAULT_REFRESH_BEFORE_MINUTES + 10),
                "new_token": None,
                "new_expires_on": None,
                "raise_error_when_get_access_token": False,
                "settings_dict": None
            }
        ]
        for case in test_cases:
            with self.subTest(name=case["name"]):
                database_wrapper = create_database_wrapper_instance(
                    case["old_token"], case["old_expires_on"], case["new_token"], case["new_expires_on"],
                    case["raise_error_when_get_access_token"], case["settings_dict"]
                    )
                database_wrapper.get_token_if_expired("tenant id", "client id", "client secret", "scope")
                self.assertEqual(database_wrapper.token, case["old_token"])
                self.assertEqual(database_wrapper.expires_on, case["old_expires_on"])
                self.assertTrue(database_wrapper.logger.logger_called)
                self.assertTrue("A valid token is present, no need to request it."
                                in database_wrapper.logger.info_messages)

    def test_get_connection_params_with_invalid_aad_options(self):
        """
        Test function responsible for getting params with invalid aad options
        """
        test_cases = [
            {
                "name": "Invalid AAD options",
                "old_token": None,
                "old_expires_on": None,
                "new_token": "token",
                "new_expires_on": time.time() + 60 * (DEFAULT_REFRESH_BEFORE_MINUTES + 10),
                "raise_error_when_get_access_token": False,
                "settings_dict": {
                    "ENGINE": "engine",
                    "NAME": "name",
                    "HOST": "host",
                    "PORT": "port",
                    "USER": "user",
                    "PASSWORD": "password",
                    "OPTIONS": {
                        "sslmode": "require"
                    },
                    "AAD_OPTIONS": {
                        "SP_CLIENT_ID": "client id",
                        "SP_CLIENT_SECRET": "client secret",
                        "SP_TENANT_ID": None,
                    }
                }
            }
        ]
        for case in test_cases:
            with self.subTest(name=case["name"]):
                database_wrapper = create_database_wrapper_instance(
                    case["old_token"], case["old_expires_on"], case["new_token"], case["new_expires_on"],
                    case["raise_error_when_get_access_token"], case["settings_dict"]
                    )
                self.assertRaises(ImproperlyConfigured, database_wrapper.get_connection_params)

    def test_get_connection_params_with_error(self):
        """
        Test function responsible for getting params with error raised when fetching token from Azure
        """
        test_cases = [
            {
                "name": "Error raised when calling Azure",
                "old_token": None,
                "old_expires_on": None,
                "new_token": "token",
                "new_expires_on": time.time() + 60 * (DEFAULT_REFRESH_BEFORE_MINUTES + 10),
                "raise_error_when_get_access_token": True,
                "settings_dict": {
                    "ENGINE": "engine",
                    "NAME": "name",
                    "HOST": "host",
                    "PORT": "port",
                    "USER": "user",
                    "PASSWORD": "password",
                    "OPTIONS": {
                        "sslmode": "require"
                    },
                    "AAD_OPTIONS": {
                        "SP_CLIENT_ID": "client id",
                        "SP_CLIENT_SECRET": "client secret",
                        "SP_TENANT_ID": "tenant id",
                    }
                }
            }
        ]
        for case in test_cases:
            with self.subTest(name=case["name"]):
                database_wrapper = create_database_wrapper_instance(
                    case["old_token"], case["old_expires_on"], case["new_token"], case["new_expires_on"],
                    case["raise_error_when_get_access_token"], case["settings_dict"]
                    )
                self.assertRaises(Exception, database_wrapper.get_connection_params)

    def test_get_connection_params_all_good(self):
        """
        Test function responsible for getting params when token is fetched correctly
        """
        test_cases = [
            {
                "name": "Token is fetched correctly and set as password",
                "old_token": None,
                "old_expires_on": None,
                "new_token": "token",
                "new_expires_on": time.time() + 60 * (DEFAULT_REFRESH_BEFORE_MINUTES + 10),
                "raise_error_when_get_access_token": False,
                "settings_dict": {
                    "ENGINE": "engine",
                    "NAME": "name",
                    "HOST": "host",
                    "PORT": "port",
                    "USER": "user",
                    "PASSWORD": "password",
                    "OPTIONS": {
                        "sslmode": "require"
                    },
                    "AAD_OPTIONS": {
                        "SP_CLIENT_ID": "client id",
                        "SP_CLIENT_SECRET": "client secret",
                        "SP_TENANT_ID": "tenant id",
                    }
                }
            }
        ]
        for case in test_cases:
            with self.subTest(name=case["name"]):
                database_wrapper = create_database_wrapper_instance(
                    case["old_token"], case["old_expires_on"], case["new_token"], case["new_expires_on"],
                    case["raise_error_when_get_access_token"], case["settings_dict"]
                    )
                conn_params = database_wrapper.get_connection_params()
                self.assertEqual(conn_params["password"], case["new_token"])


if __name__ == '__main__':
    unittest.main()

