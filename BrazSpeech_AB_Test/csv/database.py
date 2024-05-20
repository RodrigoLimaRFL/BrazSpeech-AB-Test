import paramiko
from sshtunnel import SSHTunnelForwarder
import pymysql
import pandas as pd

class Database:
    # SSH and database configuration
    ssh_host = '143.107.183.175'
    ssh_port = 14822
    ssh_user = 'guico21'
    ssh_password = "&ejaN%eQ('yz" # or use ssh_pkey for private key

    remote_bind_address = '127.0.0.1'
    remote_bind_port = 3306

    db_host = '127.0.0.1'
    db_user = 'guico21'
    db_password = 'att%eY4y'
    db_name = 'braz'
    db_port = 3306

    connection = None
    server = None
                
    def __init__(self):
        # Set up the SSH tunnel
        self.server = SSHTunnelForwarder(
            (self.ssh_host, self.ssh_port),
            ssh_username=self.ssh_user,
            ssh_password=self.ssh_password,
            remote_bind_address=(self.remote_bind_address, self.remote_bind_port),
            local_bind_address=('0.0.0.0', 10022)  # Local port to forward
        )

        # Start the server
        self.server.start()

        # Connect to the MySQL database
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=self.server.local_bind_port,
            user=self.db_user,
            password=self.db_password,
            db=self.db_name
        )

    
    def _run_query(self, sql_query, params=None):
        """Runs a given SQL query via the global database connection.

        :param sql: MySQL query
        :return: Pandas DataFrame containing results for SELECT queries,
                last inserted ID for INSERT queries, None for other queries
        """
        if sql_query.strip().lower().startswith("select"):
            return pd.read_sql_query(sql_query, self.connection, params=params)  # type: ignore
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(sql_query, params)
                self.connection.commit()
                if sql_query.strip().lower().startswith("insert"):
                    return cursor.lastrowid


    def fiveSecAudiosSP(self):
        sql_query = f"""
        SELECT name, file_path, duration
        FROM (
            SELECT a.name,
                d.file_path,
                d.end_time - d.start_time AS duration,
                ROW_NUMBER() OVER (PARTITION BY a.name ORDER BY d.file_path) AS row_num
            FROM Audio a
            JOIN Dataset d ON a.id = d.audio_id
            WHERE a.corpus_id = 2
            AND d.end_time - d.start_time > 9
            AND d.end_time - d.start_time < 11
        ) AS ranked
        WHERE row_num <= 5;
        """
        return self._run_query(sql_query)
