import sqlite3
import time
from main import bot
class ANKETA:
    def ank(self, mes):
        conn = sqlite3.connect('baza.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        info = ''

        for el in users:
            if el[0] == mes.from_user.id:
                info = f'1️⃣ Ник: {el[1]}\n' \
                        f'2️⃣ Пол: {el[2]}\n' \
                        f'3️⃣ Возраст: {el[3]}\n' \
                        f'4️⃣ Письмо: {el[4]}\n'
        cur.close()
        conn.close()
        time.sleep(0.5)
        bot.send_message(mes.chat.id, '💡 Добро пожаловать в раздел "Моя анкета"❗ '
                                      'Это ваши данные которые вы указали при регистрации. 👇\n\n'
                                      '' + info )