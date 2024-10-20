from fastapi import HTTPException, status
import os
import pymysql.cursors
from pymysql import converters
from queue import Queue, Empty
import threading


class DatabaseConnector:
    def __init__(self):
        self.host = os.getenv("DATABASE_HOST")
        self.user = os.getenv("DATABASE_USERNAME")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.database = os.getenv("DATABASE")
        self.port = int(os.getenv("DATABASE_PORT"))
        self.conversions = converters.conversions
        self.conversions[pymysql.FIELD_TYPE.BIT] = (
            lambda x: False if x == b"\x00" else True
        )
        if not self.host:
            raise EnvironmentError("DATABASE_HOST environment variable not found")
        if not self.user:
            raise EnvironmentError("DATABASE_USERNAME environment variable not found")
        if not self.password:
            raise EnvironmentError("DATABASE_PASSWORD environment variable not found")
        if not self.database:
            raise EnvironmentError("DATABASE environment variable not found")

        # Initialize the queue
        self.queue = Queue()
        
        # Start a worker thread to process queue tasks
        self.worker = threading.Thread(target=self.process_queue, daemon=True)
        self.worker.start()

    def get_connection(self):
        connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor,
            conv=self.conversions,
        )
        return connection

    def process_queue(self):
        """Worker thread to process tasks from the queue."""
        while True:
            try:
                # Get the next task from the queue (block until available)
                task = self.queue.get(timeout=1)
                method, sql, param, callback = task
                result = method(sql, param)
                if callback:
                    callback(result)
            except Empty:
                continue
            except Exception as e:
                print(f"Error processing task: {e}")
            finally:
                # Mark task as done
                self.queue.task_done()

    def _execute(self, sql, param):
        """Internal method to execute SQL commands."""
        try:
            connection = self.get_connection()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, param)
                    connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error: " + str(e),
            )

    def _fetch(self, sql, param):
        """Internal method to fetch SQL query results."""
        try:
            connection = self.get_connection()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, param)
                    return cursor.fetchall()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error: " + str(e),
            )

    # CRUD Operations
    def create(self, sql, param, callback=None):
        """Add a CREATE task to the queue."""
        self.queue.put((self._execute, sql, param, callback))

    def read(self, sql, param, callback=None):
        """Add a READ task to the queue."""
        self.queue.put((self._fetch, sql, param, callback))

    def update(self, sql, param, callback=None):
        """Add an UPDATE task to the queue."""
        self.queue.put((self._execute, sql, param, callback))

    def delete(self, sql, param, callback=None):
        """Add a DELETE task to the queue."""
        self.queue.put((self._execute, sql, param, callback))

