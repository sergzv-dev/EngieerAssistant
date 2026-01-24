from models import UserInDB, UserLoginInDB
from connections import get_pg_connection

class Repository:
    @classmethod
    def get_conn(cls):
        return get_pg_connection()

class UserRepository(Repository):
    def add_user(self, user: UserInDB) -> None:
        with self.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''INSERT INTO users (username, email, hashed_password)
                                VALUES (%(username)s, %(email)s, %(hashed_password)s)''',
                               user.model_dump(include={'username', 'email', 'hashed_password'}))

    def get_user_auth_data(self, username) -> UserLoginInDB|None:
        with self.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT id, hashed_password FROM users WHERE username = %(username)s',
                               {'username': username})
                row = cursor.fetchone()
                if not row:
                    return None
                return UserLoginInDB(id=row[0], hashed_password=row[1])

#test methods
    def get_all_users(self):
        with self.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM users')
                rows = cursor.fetchall()
                return rows