import random
import re
import telebot as tb
from telebot import types
import sqlite3
import time

from datetime import datetime
#6230965819:AAEItt6Nd6GvV5Wo9gGI2c1A_UZsQOWrxm8 тест
#6222870229:AAFPDHeKkEEvyrm6JZiItlhIOU4pvIEeHzc бот
bot = tb.TeleBot('6230965819:AAEItt6Nd6GvV5Wo9gGI2c1A_UZsQOWrxm8')

nik = ''
uspol= ''
age = 0
note = ''
class BUTTON():
    def __init__(self):
        self.KEYBB = types.KeyboardButton
        self.KEYBM = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.KEYBR = types.ReplyKeyboardRemove()

    def but(self, btn1, btn2, btn3, btn4):
        markup = self.KEYBM
        btn_1 = self.KEYBB(btn1)
        btn_2 = self.KEYBB(btn2)
        btn_3 = self.KEYBB(btn3)
        btn_4 = self.KEYBB(btn4)
        markup.row(btn_1, btn_2)
        markup.row(btn_3)
        markup.row(btn_4)
        return markup

    def pol_but(self, btn1, btn2):
        markup = self.KEYBM
        btn_1 = self.KEYBB(btn1)
        btn_2 = self.KEYBB(btn2)
        markup.row(btn_1, btn_2)
        return markup

    def delete_but(self):
        return self.KEYBR

BUT = BUTTON().but('Моя анкета', 'Помощь', 'Смотреть записи', 'Изменить запись')
EDITBUT = BUTTON().but('Ник', 'Пол', 'Возраст', 'Пожелание')
POLBUT = BUTTON().pol_but('Мужской', 'Женский')
DELETEBUT = BUTTON().delete_but()



class HELP:
    def __init__(self, text):
        self.text = text

    def help(self, mes):
        bot.send_message(mes.chat.id, self.text)

class RECORDING():
    def __init__(self):
        self.ARRAY = []
        self.smail_m = [ "😊", "👦", "😉", "😎", "💪", "😩", "👱", "😛", "🙉"]
        self.smail_d = ["❤", "🌹", "👩", "💋", "🙌", "😩", "‍️👱‍♀️", "💜", "🧡", "💕", "🥰", "😘", "😙"]

    def array(self, len_us, us, id):
        l = len_us
        u = us
        i = id
        y = random.randrange(0, l)
        if y not in self.ARRAY: #and us[y][0] != id:
            self.ARRAY.append(y)
            return y
        elif len(self.ARRAY) == l:
            self.ARRAY.clear()
            return self.array(l, u, i)
        else:
            return self.array(l, u, i)

    def record(self, mes):
        conn = sqlite3.connect('baza.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        y = self.array(len(users), users, mes.from_user.id)
        if users[y][2].lower() == 'мужской':
            text = 'мужчина'
            x = random.choice(self.smail_m)
        else:
            text = 'девушка'
            x = random.choice(self.smail_d)
        info = f'{x} Автор {text}:  {users[y][1]} \n' \
               f'📌 Возраст: {users[y][3]}\n\n' \
               f'✍ <b>Письмо из прошлого: </b><i>{users[y][4]}</i>'

        cur.close()
        conn.close()
        bot.send_message(mes.chat.id, info, parse_mode='html')

class EDIT():
    def wish(self, mes):
        mes_txt = mes.text.lower()
        if mes_txt == "ник":
            bot.send_message(mes.chat.id, 'Введите новый никнейм: 👇', reply_markup=DELETEBUT)
            bot.register_next_step_handler(mes, self.wish_nik)
        elif mes_txt == "пол":
            bot.send_message(mes.chat.id, 'Введите или укажите свой пол: 👇', reply_markup=POLBUT)
            bot.register_next_step_handler(mes, self.wish_pol)
        elif mes_txt == "возраст":
            bot.send_message(mes.chat.id, 'Введите новый возраст: 👇', reply_markup=DELETEBUT)
            bot.register_next_step_handler(mes, self.wish_age)
        else:
            bot.send_message(mes.chat.id, 'Введите новое пожелание: 👇', reply_markup=DELETEBUT)
            bot.register_next_step_handler(mes, self.wish_notes)

    def wish_nik(self, mes):
        conn = sqlite3.connect('baza.sql')
        cur = conn.cursor()
        nik = mes.text.strip()
        regex = "^[a-zA-Zа-яА-ЯеЁ,.?/!0123456789]+$"
        pattern = re.compile(regex)
        pat = pattern.search(nik) is not None
        if pat == True and len(nik) <= 15:
            data = (nik, mes.from_user.id)
            cur.execute("UPDATE users set nik = ? where id = ?", data)
            conn.commit()
            cur.close()
            conn.close()
            time.sleep(0.5)
            bot.send_message(mes.chat.id, 'Ваша запись изменина!', reply_markup=BUT)
        elif pat == False or ' ' in nik:
            bot.send_message(mes.chat.id,
                             'Ваш ник содержит недопустимые символы! 🤨 Введите другой! ')
            bot.register_next_step_handler(mes, self.wish_nik)
        elif len(nik) > 15:
            bot.send_message(mes.chat.id, 'Длина ника не может быть больше 15 символов! 🙄 Придумай другой! ')
            bot.register_next_step_handler(mes, self.wish_nik)
        else:
            bot.send_message(mes.chat.id, 'Эээххх жаль, но такой ник уже есть! 🙂  Напиши другой!')
            bot.register_next_step_handler(mes, self.wish_nik)


    def wish_pol(self, mes):
        uspol = mes.text.strip()
        if uspol.lower() == 'мужской' or uspol.lower() == 'женский':
            conn = sqlite3.connect('baza.sql')
            cur = conn.cursor()
            data = (uspol, mes.from_user.id)
            cur.execute("UPDATE users set pol = ? where id = ?", data)
            conn.commit()
            cur.close()
            conn.close()
            time.sleep(0.5)
            bot.send_message(mes.chat.id, 'Ваша запись изменина!', reply_markup=BUT)
        else:
            bot.send_message(mes.chat.id, 'Неее, ну так дело не пойдет, пиши правду! 😄')
            bot.register_next_step_handler(mes, self.wish_pol)


    def wish_age(self, mes):
        age = mes.text.strip()
        try:
            age = int(age)
            if age > 0 and age <= 100:
                conn = sqlite3.connect('baza.sql')
                cur = conn.cursor()
                age = mes.text.strip()
                data = (age, mes.from_user.id)
                cur.execute("UPDATE users set age = ? where id = ?", data)
                conn.commit()
                cur.close()
                conn.close()
                time.sleep(0.5)
                bot.send_message(mes.chat.id, 'Ваша запись изменина!', reply_markup=BUT)
            else:
                bot.send_message(mes.chat.id, f'Друг, люди больше {age} лет не живут! 😂')
                bot.send_message(mes.chat.id, f'Напиши точный возраст:')
                bot.register_next_step_handler(mes, self.wish_age)
        except ValueError:
            bot.send_message(mes.chat.id, 'Зачем ты меня пытаешься обмануть, введи число ❗❗❗')
            bot.register_next_step_handler(mes, self.wish_age)

    def wish_notes(self, mes):
        note = mes.text.strip()
        if len(note) > 80:
            bot.send_message(mes.chat.id, 'Друг, твоё пожелание слишком длинное, напиши пожалуйста попроще )')
            bot.register_next_step_handler(mes, self.wish_notes)
        else:
            conn = sqlite3.connect('baza.sql')
            cur = conn.cursor()
            data = (note, mes.from_user.id)
            cur.execute("UPDATE users set notes = ? where id = ?", data)
            conn.commit()
            cur.close()
            conn.close()
            time.sleep(0.5)
            bot.send_message(mes.chat.id, 'Ваша запись изменина!', reply_markup=BUT)


class TELEGRAMBOT: # объявляем родительский класс
    def __init__(self, id, BUT, EDITBUT, POLBUT, DELETEBUT):
        print("Создан объект бота!")
        self._USER_ID = id
        self._COMMANDS = ['Привет!', 'Здравствуй!','Хай!']
        self._BUT = BUT
        self._EDITBUT = EDITBUT
        self._POLBUT = POLBUT
        self._DELETEBUT = DELETEBUT

    def examination(self, id):
        conn = sqlite3.connect('baza.sql')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users '
                    '(id int auto_increment primary key,'
                    'nik varchar(25), '
                    'pol varchar(10), '
                    'age int,'
                    'city varchar(80)'
                    'notes varchar(80))')

        conn.commit()
        cur.close()
        conn.close()

        conn = sqlite3.connect('baza.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        ans = None
        for el in users:
            if id == el[0]:
                ans = 'yes'
                break
            else:
                ans = 'no'
        cur.close()
        conn.close()
        return ans

    def communicat(self, message):
        answer = self.examination(self._USER_ID)
        mes_txt = message.text.lower()
        if mes_txt == "начать":
            if answer == 'no' or answer == None:
                self.lounding(message)
            else:
                bot.send_message(message.chat.id, f' {random.choice(self._COMMANDS)} {message.from_user.first_name}', reply_markup=self._BUT)
        elif mes_txt == 'моя анкета':
            anketa = ANKETA().ank(message)
        elif mes_txt == 'помощь':
            help = HELP(f'Добро пожаловать в раздел "Помощь"❗ Это бот "Писем" от создателя PROSTOBAS - @prost0bas.' \
               f'\n\n ⚙ Данное приложение было создано для того, чтобы вы могли писать разные письма другим людям, редактировать свое и просматривать другие. 🥰' \
               f'' \
               f'\n\n🤖 Версия бота V1.0').help(message)
        elif mes_txt == 'смотреть записи':
            recording = RECORDING().record(message)
        elif mes_txt == 'изменить запись':
            time.sleep(0.5)
            bot.send_message(message.chat.id, 'Выберите снизу раздел который хотите изменить',
                             reply_markup=self._EDITBUT)
            edit = EDIT()
            bot.register_next_step_handler(message,  edit.wish)
        else:
            bot.send_message(message.chat.id, 'Я тебя что-то не понимаю 🤨')

    # Функция при старте, когда пользователь нажал кнопку или написал что-то
    def lounding(self, message):
        # Вызываем класс пользователь с функцией проверки пользователя
        answer = self.examination(self._USER_ID)
        if answer == 'no' or answer == None:
            bot.send_message(message.chat.id, 'Добро пожаловать в приложение "Письмо из прошлого". Меня зовут Максим и я являюсь его основателем! '
                                              'В чем суть этого приложения Вы поймете после того, как пройдете регистрацию. Желаю успехов и хорошего настроения!'
                                              ''
                                              'Введите свое анонимное имя  ')
            bot.register_next_step_handler(message, self.user_name)
        else:
            bot.send_message(message.chat.id, 'Здравствуйте❗', reply_markup=self._BUT)

    def user_name(self, message):
        global nik
        nik = message.text.strip()
        conn = sqlite3.connect('baza.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        ans = None
        for el in users:
            if nik == el[1]:
                ans = 'yes'
            else:
                ans = 'no'
        cur.close()
        conn.close()
        regex = "^[a-zA-Zа-яА-ЯеЁ,.\|?/!0123456789]+$"
        pattern = re.compile(regex)
        pat = pattern.search(nik) is not None
        if ans == 'no' or ans == None and pat == True and len(nik) <= 15:
            bot.send_message(message.chat.id, f'Отлично❗'
                                              f'\n✅Теперь вас зовут: {nik}. '
                                              f'\nИдем дальше 🚶‍♂️ '
                                              f'\n\nВведите или укажите свой пол: 👇', reply_markup=self._POLBUT)
            bot.register_next_step_handler(message, self.user_pol)
        elif pat == False or ' ' in nik:
            bot.send_message(message.chat.id,
                             'Ваш ник содержит недопустимые символы! 🤨 Введите другой! ')
            bot.register_next_step_handler(message, self.user_name)
        elif len(nik) > 15:
            bot.send_message(message.chat.id, 'Длина ника не может быть больше 15 символов! 🙄 Придумай другой! ')
            bot.register_next_step_handler(message, self.user_name)
        else:
            bot.send_message(message.chat.id, 'Эээххх жаль, но такой ник уже есть! 🙂  Напиши другой!')
            bot.register_next_step_handler(message, self.user_name)

    def user_pol(self, message):
        global uspol
        uspol = message.text.strip()
        if uspol.lower() == 'мужской' or uspol.lower() == 'женский':
            bot.send_message(message.chat.id, f'Супер ☺. Осталось еще чуть-чуть. '
                                              f'\n✅ Вас зовут: {nik}. '
                                              f'\n✅ Ваш пол: {uspol}.'
                                              f'\n\nТеперь напишите свой возраст:👇', reply_markup=self._DELETEBUT)
            bot.register_next_step_handler(message, self.user_age)
        else:
            bot.send_message(message.chat.id, 'Неее, ну так дело не пойдет, пиши правду! 😄')
            bot.register_next_step_handler(message, self.user_pol)

    def user_age(self, message):
        global age
        age = message.text.strip()
        try:
            age = int(age)
            if age > 0 and age <= 100:
                bot.send_message(message.chat.id, f'Ураааа ☺. Последний этап. '
                                              f'\n✅ Вас зовут: {nik}. '
                                              f'\n✅ Ваш пол: {uspol}.'
                                              f'\n✅ Ваш возраст: {age}.'
                                              f'\n\nНапишите своё письмо другим людям: 🤗')
                bot.register_next_step_handler(message, self.user_note)
            else:
                bot.send_message(message.chat.id, f'Друг, люди больше {age} лет не живут! 😂')
                bot.send_message(message.chat.id, f'Напиши точный возраст:')
                bot.register_next_step_handler(message, self.user_age)
        except ValueError:
            bot.send_message(message.chat.id, 'Зачем ты меня пытаешься обмануть, введи число ❗❗❗')
            bot.register_next_step_handler(message, self.user_age)

    def user_note(self, message):
        note = message.text.strip()
        conn = sqlite3.connect('baza.sql')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (id, nik, pol, age, notes) VALUES (('%d'), ('%s'), ('%s'), ('%d'), ('%s'))" % (
                self._USER_ID, nik, uspol, age, note))
        conn.commit()
        cur.close()
        conn.close()
        time.sleep(0.)
        if len(note) > 80:
            bot.send_message(message.chat.id, 'Друг, твоё письмо слишком длинное, напиши пожалуйста попроще )')
            bot.register_next_step_handler(message, self.user_note)
        else:
            bot.send_message(message.chat.id, f'Поздравляю, вы прошли регистрацию успешна❗ '
                                              f'\n✅ Вас зовут: {nik}. '
                                              f'\n✅ Ваш пол: {uspol}.'
                                              f'\n✅ Ваш возраст: {age}.'
                                              f'\n✅ Ваше пожелание: {note}.'
                                              f'\n\n 💡 Теперь вам доступны все функции. '
                                              f' Снизу представлены кнопки,'
                                              f'нажмите кнопку "Помощь", чтобы я мог ввести вас в курс дела 🙂', reply_markup=self._BUT)



@bot.message_handler(commands=['start'])
def start(message):
    BOT = TELEGRAMBOT(message.from_user.id, BUT, EDITBUT, POLBUT, DELETEBUT)
    BOT.lounding(message)

@bot.message_handler()
def callback(message):
    BOT = TELEGRAMBOT(message.from_user.id, BUT, EDITBUT, POLBUT ,DELETEBUT)
    BOT.communicat(message)


print('Бот запущен!')
while True:
    if __name__ == '__main__':
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception:
            pass
