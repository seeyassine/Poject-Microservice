# config.py
import os

MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),  # Default to localhost if not set
    'user': os.getenv('MYSQL_USER', 'root'),  # Default user as root if not set
    'password': os.getenv('MYSQL_PASSWORD', 'nano@password'),  # Default empty password if not set
    'database': os.getenv('MYSQL_DATABASE', 'my_db'),  # Default DB name
    'port': int(os.getenv('MYSQL_PORT', 3306))  # Default to port 3306 if not set
}

