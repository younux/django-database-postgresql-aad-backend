# django_database_postgresql_aad_backend


django-database-postgresql-aad-backend is a django database backend that adds Azure active directory authentication for 
your Azure postgresql server. It uses the authentication as described in Azure documentation : 
[https://docs.microsoft.com/en-us/azure/postgresql/howto-configure-sign-in-aad-authentication](https://docs.microsoft.com/en-us/azure/postgresql/howto-configure-sign-in-aad-authentication).

This backend is based on Django postgresql backend (which it inherits from all its features) and adds AAD options in 
database settings as described bellow :


    DATABASES = {
        "default": {
            "ENGINE": "django_database_postgresql_aad_backend",
            "NAME": os.getenv("DB_NAME"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
            "USER": os.getenv("DB_USERNAME"),
            "PASSWORD": "",
            "OPTIONS": {
                "sslmode": "require"
            },
            "AAD_OPTIONS": {
                "SP_CLIENT_ID": os.getenv("DB_SP_CLIENT_ID"),
                "`SP_CLIENT_SECRET`": os.getenv("DB_SP_CLIENT_SECRET"),
                "`SP_TENANT_ID`": os.getenv("DB_SP_TENANT_ID"),
            }
        }
    }
    
To enable Azure Active directory authentication you need to :
 
   - Install `django_database_postgresql_aad_backend` using pip : 

    pip install django_database_postgresql_aad_backend
    
   - Add the backend to installed apps in `setting.py` 
        
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'django_database_postgresql_aad_backend',
    ]
        
   - Provide `AAD_OPTIONS` dictionary inside database settings with the following keys : 
    
      - `SP_CLIENT_ID` (Required) The client ID of the service principal used to authenticate to Azure Active directory.
      - `SP_CLIENT_SECRET`: (Required) The client secret of the service principal used to authenticate to Azure active directory.
      - `SP_TENANT_ID`: (Required) The tenant ID of the service principal.
      - `REFRESH_BEFORE_MINUTES`: (Optional) This is used to specify how much time (in minutes) the token should be valid.
            Default value is 5.

If you don't provide `AAD_OPTIONS` dictionary, Azure active directory authentication will be disabled and the backend
will use the default user/password authentication method.


## Tests 

To run tests : 

    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    coverage run --source django_database_postgresql_aad_backend -m unittest discover 
    coverage report

## Building package

To build package : 

    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    python3 setup.py sdist bdist_wheel

## Publish package 
    
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    
 
## Improvements

 - The token is fetched and stored in memory. An improvement would be to support a caching system to store token 
 and share it between multiple instances of the backend.
 - Add more test cases !
