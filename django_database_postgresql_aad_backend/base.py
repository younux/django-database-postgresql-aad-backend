import time

from django.db.backends.postgresql import base
from django.core.exceptions import ImproperlyConfigured

from .mixins import AzureIdentityMixin, LoggerMixin

# Default scope to use when requesting AAD token
SCOPE = "https://ossrdbms-aad.database.windows.net/.default"
# The difference between the token expiration time and current
# time in minutes bellow which the token should be refreshed
DEFAULT_REFRESH_BEFORE_MINUTES = 5


class DatabaseWrapper(AzureIdentityMixin, LoggerMixin, base.DatabaseWrapper):
    token = None
    expires_on = None

    def get_token_if_expired(self, tenant_id, client_id, client_secret, scope,
                             refresh_before_minutes=DEFAULT_REFRESH_BEFORE_MINUTES):
        if not (self.__class__.expires_on
                and ((self.__class__.expires_on - time.time()) > 60 * refresh_before_minutes)
                ):
            self.logger.info("No valid token, token will be requested.")
            access_token = self.__class__.get_access_token(tenant_id, client_id, client_secret, scope)
            self.__class__.token = access_token.token
            self.__class__.expires_on = access_token.expires_on
            self.logger.info("Token was set.")
        else:
            self.logger.info("A valid token is present, no need to request it.")

    def get_connection_params(self):
        conn_params = super().get_connection_params()
        # Check if AAD authentication is used
        if self.settings_dict.get("AAD_OPTIONS"):
            # Check that AAD authentication parameters are provided
            if not (self.settings_dict.get("AAD_OPTIONS").get("SP_CLIENT_ID")
                    and self.settings_dict.get("AAD_OPTIONS").get("SP_CLIENT_SECRET")
                    and self.settings_dict.get("AAD_OPTIONS").get("SP_TENANT_ID")
                    ):
                raise ImproperlyConfigured(
                    "settings.DATABASES is improperly configured."
                    "Please supply all AAD_OPTIONS values.")
            try:
                refresh_before_minutes = self.settings_dict.get("AAD_OPTIONS").get("REFRESH_BEFORE_MINUTES",
                                                                                   DEFAULT_REFRESH_BEFORE_MINUTES)
                # Getting or refreshing AAD token
                self.get_token_if_expired(
                    self.settings_dict["AAD_OPTIONS"]['SP_TENANT_ID'],
                    self.settings_dict["AAD_OPTIONS"]['SP_CLIENT_ID'],
                    self.settings_dict['AAD_OPTIONS']['SP_CLIENT_SECRET'],
                    SCOPE,
                    refresh_before_minutes)
            except Exception as e:
                raise ImproperlyConfigured(
                    "settings.DATABASES AAD is improperly configured."
                    "The application could not retrieve an access token."
                    + str(e))
            # Setting password with token value
            conn_params['password'] = self.__class__.token
            return conn_params
