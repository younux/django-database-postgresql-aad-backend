import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='django_database_postgresql_aad_backend',
    packages=['django_database_postgresql_aad_backend'],
    version='v0.0.1',
    license='MIT',
    description='Django database backend for Azure Postgresql that adds AAD authentication',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Younes',
    author_email='b.younes.h@gmail.com',
    url='https://github.com/younux/django-database-postgresql-aad-backend',
    download_url='https://github.com/younux/django-database-postgresql-aad-backend/releases/download/v0.0.1/django_database_postgresql_aad_backend-v0.0.1.tar.gz',
    keywords=['Django', 'Database', 'Backend', 'Postgresql', 'Azure', 'AAD'],
    install_requires=[
        'asgiref==3.3.1',
        'azure-core==1.10.0',
        'azure-identity==1.5.0',
        'certifi==2020.12.5',
        'cffi==1.14.4',
        'chardet==4.0.0',
        'cryptography==3.3.1',
        'Django==3.1.5',
        'idna==2.10',
        'msal==1.8.0',
        'msal-extensions==0.3.0',
        'portalocker==1.7.1',
        'psycopg2-binary==2.8.6',
        'pycparser==2.20',
        'PyJWT==1.7.1',
        'pytz==2020.5',
        'requests==2.25.1',
        'six==1.15.0',
        'sqlparse==0.4.1',
        'urllib3==1.26.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
