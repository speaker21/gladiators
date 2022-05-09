import sqlite3
import random

class Database:
    def __init__(self, database_filename) -> None:
        self._database_filename = database_filename

    def execute(self, execution, *args):
        connection = sqlite3.connect(self._database_filename)
        cursor = connection.cursor()
        if args:
            cursor.execute(execution, *args)
        else:
            cursor.execute(execution)
        result = cursor.fetchall()
        cursor.close()
        connection.commit()
        connection.close()
        return result

    def reset_data(self):
        self.execute('update gladiators SET OWNER=?', (None,))
        self.execute('update gladiators SET is_dead=?', (False,))
        self.execute('update gladiators SET winstreak=?', (0,))
        self.execute('update gladiators SET level=?', (1,))
        self.execute('update gladiators SET hp=max_hp')

        self.execute('update lanista_data SET gold=?', (1000, ))

    def add_random_data(self):
        a = ('Граф', 'Дар','Меркурий','Март', 'Христамрирадос', 'Князь', 'Принц', 'Космос')
        for i in a:
            self.execute('insert into gladiators (name, attack_power, hp, owner) VALUES (?,?,?,?)', (i, random.randint(10,80), random.randint(10,80), None))




if __name__ == '__main__':
    d = Database('database.db')
    d.reset_data()

