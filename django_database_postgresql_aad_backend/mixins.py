import logging

from azure.identity import ClientSecretCredential


class AzureIdentityMixin:
    @staticmethod
    def get_access_token(tenant_id, client_id, client_secret, scope):
        credentials = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret)
        return credentials.get_token(scope)


class LoggerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.logger = logging.getLogger(__name__)

