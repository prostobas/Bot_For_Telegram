from telebot import types
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