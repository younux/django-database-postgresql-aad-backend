from django_database_postgresql_aad_backend.base import DatabaseWrapper


class AccessToken:
    def __init__(self, token, expires_on):
        self.token = token
        self.expires_on = expires_on


def mock_azure_identity_mixin_class(access_token, raise_error):
    class AzureIdentityMixinMock:
        @staticmethod
        def get_access_token(tenant_id, client_id, client_secret, scope):
            if raise_error:
                raise Exception
            else:
                return access_token

    return AzureIdentityMixinMock


def mock_logger_mixin_class():
    class Logger:
        def __init__(self):
            self.logger_called = False
            self.info_messages = []

        def info(self, msg):
            self.logger_called = True
            self.info_messages.append(msg)

    class LoggerMixinMock:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.logger = Logger()

    return LoggerMixinMock


def mock_database_wrapper_class(azure_identity_mixin_cls, logger_mixin_cls, in_token, in_expires_on, settings_dict):
    class ConnectionParamsMixin:
        def get_connection_params(self):
            self.settings_dict = settings_dict

    class DatabaseWrapperMock(azure_identity_mixin_cls, logger_mixin_cls, DatabaseWrapper, ConnectionParamsMixin):
        token = in_token
        expires_on = in_expires_on

        def __init__(self, *args, **kwargs):
            super().__init__(args, kwargs)
            self.settings_dict = settings_dict

    return DatabaseWrapperMock

def create_database_wrapper_instance(old_token, old_expires_on,
                                     new_token, new_expires_on,
                                     raise_error_when_get_access_token,
                                     settings_dict):
    access_token = AccessToken(new_token, new_expires_on)
    azure_identity_mixin_cls = mock_azure_identity_mixin_class(access_token,
                                                               raise_error_when_get_access_token)
    logger_mixin_cls = mock_logger_mixin_class()
    database_wrapper_cls = mock_database_wrapper_class(azure_identity_mixin_cls,
                                                       logger_mixin_cls,
                                                       old_token,
                                                       old_expires_on,
                                                       settings_dict)
    return database_wrapper_cls()