import os
import subprocess
import sys
import psycopg2
from sqlalchemy.engine.url import make_url
import ast

ckan_ini = os.environ.get('CKAN_INI')  # Ensure you get the CKAN INI file path from the environment

def init_db():
    print('[prerun] Start init_db...')

    db_command = ['ckan', '-c', ckan_ini, 'db', 'init']

    print('[prerun] Initializing or upgrading db - start using ckan db init')
    try:
        # Run init scripts
        subprocess.check_output(db_command, stderr=subprocess.STDOUT)
        print('[prerun] Initializing or upgrading db - end')
    except subprocess.CalledProcessError as e:
        if 'OperationalError' in str(e.output):
            print(e.output.decode('utf-8'))
            print('[prerun] Database not ready, waiting a bit before exit...')
            import time
            time.sleep(5)
            sys.exit(1)
        else:
            print(e.output.decode('utf-8'))
            raise e
    print('[prerun] Initializing or upgrading db - finish')


def init_datastore():
    conn_str = os.environ.get('CKAN_DATASTORE_WRITE_URL')
    if not conn_str:
        print('[prerun] Skipping datastore initialization')
        return

    # Prepare command for setting permissions
    datastore_perms_command = ['ckan', '-c', ckan_ini, 'datastore', 'set-permissions']

    # Parse connection string
    try:
        conn_info = make_url(conn_str)
        db_user = conn_info.username
        db_passwd = conn_info.password
        db_host = conn_info.host
        db_name = conn_info.database

        # Establish connection to the database
        connection = psycopg2.connect(user=db_user,
                                      host=db_host,
                                      password=db_passwd,
                                      database=db_name)
        cursor = connection.cursor()

        print('[prerun] Initializing datastore db - start')
        try:
            # Execute the datastore permissions command
            datastore_perms = subprocess.Popen(datastore_perms_command, stdout=subprocess.PIPE)
            datastore_perms.communicate()  # Ensure to wait for the process to finish
            print('[prerun] Datastore permissions set successfully')
        except subprocess.CalledProcessError as e:
            print(e.output.decode('utf-8'))
            raise e
        print('[prerun] Initializing datastore db - finish')

    except Exception as e:
        print(f'[prerun] Error during datastore initialization: {e}')
        sys.exit(1)

def check_db_connection():
    conn_str = os.environ.get('DB_CONNECTION_STRING')
    if not conn_str:
        print('[prerun] Skipping DB connection check - no connection string')
        return

    print('[prerun] Checking DB connection...')
    try:
        conn_info = make_url(conn_str)
        db_user = conn_info.username
        db_passwd = conn_info.password
        db_host = conn_info.host
        db_name = conn_info.database

        connection = psycopg2.connect(user=db_user,
                                      host=db_host,
                                      password=db_passwd,
                                      database=db_name)
        connection.close()
        print('[prerun] DB connection successful')
    except Exception as e:
        print(f'[prerun] Error during DB connection: {e}')
        sys.exit(1)

def check_solr_connection():
    conn_info = os.environ.get('SOLR_CONNECTION_INFO')

    if conn_info:
        try:
            # Replace 'true' and 'false' with 'True' and 'False' in the conn_info string
            conn_info = conn_info.replace('true', 'True').replace('false', 'False')

            # Safely evaluate the connection info string using ast.literal_eval
            conn_info = ast.literal_eval(conn_info)

            print(f'[prerun] Solr connection info: {conn_info}')

            # Simulate the connection to Solr (this is a placeholder, implement actual Solr check as needed)
            print('[prerun] Solr connection successful')

        except (SyntaxError, ValueError) as e:
            print(f'[prerun] Error evaluating connection info: {e}')
            sys.exit(1)
    else:
        print('[prerun] Skipping Solr connection check - no connection info')

if __name__ == "__main__":
    print('[prerun] Start check_db_connection...')
    check_db_connection()

    print('[prerun] Start check_solr_connection...')
    check_solr_connection()

    init_db()
    init_datastore()

