import sqlite3
import os


class Database:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, username):
        with self.connection:
            res = self.cursor.execute("""INSERT into users (user_id, username) VALUES (?, ?)""", (user_id, username,))
            self.connection.commit()
            return res

    def user_exists(self, user_id):
        with self.connection:
            res = self.cursor.execute("""SELECT * from users WHERE user_id = ?""", (user_id,)).fetchall()
            return bool(len(res))

    def add_balance(self, user_id, amount):
        with self.connection:
            res = self.cursor.execute("""UPDATE users SET balance = balance + ? WHERE user_id = ?""", (amount, user_id,))
            self.connection.commit()
            return res

    def minus_balance(self, user_id, amount):
        with self.connection:
            res = self.cursor.execute("""UPDATE users SET balance = balance - ? WHERE user_id = ?""", (amount, user_id,))
            self.connection.commit()
            return res

    def stats(self, user_id):
        with self.connection:
            return self.cursor.execute("""SELECT * from users WHERE user_id = ?""", (user_id,)).fetchone()

    def add_order(self, user_id, username, link):
        with self.connection:
            res = self.cursor.execute("""INSERT into orders (user_id, username, link) VALUES (?, ?, ?)""", (user_id, username, link,))
            self.connection.commit()
            return res

    def orders(self):
        with self.connection:
            return self.cursor.execute("""SELECT * from orders""").fetchall()

    def add_worker(self, user_id):
        with self.connection:
            res = self.cursor.execute("""INSERT into workers (user_id) VALUES (?)""", (user_id,))
            self.connection.commit()
            return res

    def up_balance_worker(self, user_id, amount):
        with self.connection:
            res = self.cursor.execute("""UPDATE workers SET balance = balance + ? WHERE user_id = ?""", (amount, user_id,))
            self.connection.commit()
            return res

    def minus_balance_worker(self, user_id, amount):
        with self.connection:
            res = self.cursor.execute("""UPDATE workers SET balance = balance - ? WHERE user_id = ?""", (amount, user_id,))
            self.connection.commit()
            return res

    def worker_exists(self, user_id):
        with self.connection:
            res = self.cursor.execute("""SELECT * from workers WHERE user_id = ?""", (user_id,)).fetchall()
            return bool(len(res))

    def worker_stats(self, user_id):
        with self.connection:
            return self.cursor.execute("""SELECT * from workers WHERE user_id = ?""", (user_id,)).fetchone()

    def get_order_info(self, id_):
        with self.connection:
            return self.cursor.execute("""SELECT * from orders WHERE order_id = ?""", (id_,)).fetchone()

    def get_accepted_order(self, id_):
        with self.connection:
            return self.cursor.execute("""SELECT * from accepted_orders WHERE order_id = ?""", (id_,)).fetchone()

    def set_order_to_worker(self, worker_id, user_id, id_, link):
        with self.connection:
            res = self.cursor.execute("""INSERT into accepted_orders (worker_id, user_id, order_id, link) VALUES (?, ?, ?, ?)""", (worker_id, user_id, id_, link,))
            self.connection.commit()
            return res

    def delete_order(self, id_):
        with self.connection:
            res = self.cursor.execute("""DELETE from orders WHERE order_id = ?""", (id_,))
            self.connection.commit()
            return res

    def delete_accepted_order(self, id_):
        with self.connection:
            res = self.cursor.execute("""DELETE from accepted_orders WHERE order_id = ?""", (id_,))
            self.connection.commit()
            return res

    def worker_orders(self, worker_id):
        with self.connection:
            return self.cursor.execute("""SELECT * from accepted_orders WHERE worker_id = ?""", (worker_id,)).fetchall()

    def add_worker_balance(self, user_id, amount):
        with self.connection:
            res = self.cursor.execute("""UPDATE workers SET balance = balance + ? WHERE user_id = ?""", (amount, user_id,))
            self.connection.commit()
            return res

    def workers(self):
        with self.connection:
            return self.cursor.execute("""SELECT * FROM workers""").fetchall()

    def all_users(self):
        with self.connection:
            return self.cursor.execute("""SELECT count (*) from users""").fetchall()

    def search_user(self, username):
        with self.connection:
            return self.cursor.execute("""SELECT * from users WHERE username = ?""", (username,)).fetchone()

    def block_user(self, user_id):
        with self.connection:
            res = self.cursor.execute("""UPDATE users SET is_banned = 1 WHERE user_id = ?""", (user_id,))
            self.connection.commit()
            return res

    def set_all_money(self, user_id, amount):
        with self.connection:
            res = self.cursor.execute("""UPDATE users SET all_money = all_money + ? WHERE user_id = ? """, (amount, user_id,))
            self.connection.commit()
            return res

    def set_all_orders(self, user_id):
        with self.connection:
            res = self.cursor.execute("""UPDATE users SET orders = orders + 1 WHERE user_id = ?""", (user_id,))
            self.connection.commit()
            return res

    def del_worker(self, user_id):
        with self.connection:
            res = self.cursor.execute("""DELETE from workers WHERE user_id = ?""", (user_id,))
            self.connection.commit()
            return res

    def get_users(self):
        with self.connection:
            return self.cursor.execute("""SELECT user_id, active from users""").fetchall()

    def set_active(self, user_id, active):
        with self.connection:
            res = self.cursor.execute("""UPDATE users SET active = ? WHERE user_id = ?""", (active, user_id,))
            self.connection.commit()
            return res

    def add_promo(self, promo, amount, activations):
        with self.connection:
            res = self.cursor.execute("""INSERT into promocodes (promo, amount, activations) VALUES (?, ?, ?)""", (promo, amount, activations))
            self.connection.commit()
            return res

    def minus_activ(self, promo):
        with self.connection:
            res = self.cursor.execute("""UPDATE promocodes SET activations = activations - 1 WHERE promo = ?""", (promo,))
            self.connection.commit()
            return res

    def delete_promo(self, promo):
        with self.connection:
            res = self.cursor.execute("""DELETE from promocodes WHERE promo = ?""", (promo,))
            self.connection.commit()
            return res

    def get_promo(self, name):
        with self.connection:
            return self.cursor.execute("""SELECT * from promocodes WHERE promo = ?""", (name,)).fetchone()

