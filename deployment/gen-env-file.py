import os
from django.core.management.utils import get_random_secret_key
from getpass import getpass
from urllib.parse import quote

ENV_TEMPLATE = '''
DEBUG=False
PRIMARY_HOSTNAME=127.0.0.1
DATABASE_URL=mysql://las_db_user:{url_passwd}@localhost:3306/las_db
DATABASE_RAW_PASSWORD={raw_passwd}
SECRET_KEY={secret_key}
'''


def _main():
    manage_py = './manage.py'
    print('checking location of script...')

    if not os.path.exists(manage_py):
        print('cannot find manage.py, please make sure you are running this script in the Django project root folder')
        exit()

    print('Please enter the password of database user:')
    db_passwd = getpass()

    print('Please enter the password of database user again:')
    db_passwd_again = getpass()

    if db_passwd != db_passwd_again:
        print('two passwords do not match each other.')
        exit()

    url_db_passwd = quote(db_passwd)

    secret_key = get_random_secret_key()

    with open('.env', 'w') as f:
        f.write(ENV_TEMPLATE.format(url_passwd=url_db_passwd,
                raw_passwd=db_passwd, secret_key=secret_key))
        print(".env file generated")


if __name__ == "__main__":
    _main()
