import tkinter as tk
from typing import Callable


"""
Модуль для GUI.

! НЕ ДОДЕЛАНО
"""


class GuiFirebirdFromTkinter():

    def __init__(self, width_windows_px: int, height_windows_px: int):
        """
        Реализация GUI Firebird на библиотеки Tkinter

        width_windows_px: Ширина окна в px
        height_windows_px: Высота окна в px
        """
        # Основой класс
        self.tk_windows = tk.Tk()
        # Заголовок окна
        self.tk_windows.title("Tkinter From Selenium")
        self.width_windows_px = width_windows_px
        self.height_windows_px = height_windows_px
        # Размер окна
        self.tk_windows.geometry('{}x{}'.format(
            width_windows_px, height_windows_px))
        ###
        # Стили
        ###
        self.style_font = ('Times 14')
        ###
        # Создать базовые виджеты
        ##
        self.create_base_widget()
        ###
        # Запустить цикл событий
        ##
        self.tk_windows.mainloop()

    def create_base_widget(self):
        """
        Создание базовых виджетов для приложения
        """
        #
        self.text_info = tk.Label(
            self.tk_windows, text="Поле для Информации", font=self.style_font,
            # Убираем 10% у ширины окна
            wraplength=self.width_windows_px-((self.width_windows_px/100)*10), justify="center")
        self.text_info.pack(side=tk.TOP, expand=True, fill=tk.X)
        # Кнопка назад
        button_last = tk.Button(self.tk_windows, text="Last",
                                command=self.TK_OnClickLast, font=self.style_font, bg='#aaffff')
        button_last.pack(side=tk.LEFT, expand=True, fill=tk.X)
        # Обработка нажатия стелки влево
        self.tk_windows.bind('<Left>', lambda *args,
                             **kwarg: self.TK_OnClickLast)
        # ##
        # # Добавляем пользовательские кнопки в Tkinter. Добавленные кнопки сохраняться в переменную `user_buttons`
        # ##
        # if tk_button:
        #     _i = 1
        #     for name_bt, func_bt in tk_button.items():
        #         name_bt: str
        #         # Функция обработчик нажатия на кнопку
        #         func_bt: Callable
        #         #
        #         tmp_button1 = tk.Button(
        #             self.tk_windows, text=f"{_i}: {name_bt}", wraplength=100, command=func_bt, font=self.style_font)
        #         tmp_button1.pack(side=tk.LEFT, expand=True, fill=tk.X)
        #         #
        #         self.user_buttons[name_bt] = func_bt
        #         # Обработка нажатия для пользовательских кнопок, цифра клавиши равна порядковому номеру кнопки
        #         self.tk_windows.bind(f'{_i}', lambda *args,
        #                              **kwarg: func_bt())
        #         _i += 1
        # # Кнопка вперед
        # button_next = tk.Button(self.tk_windows, text="Next",
        #                         command=self.TK_OnClickNext, font=self.style_font, bg='#aaffff')
        # button_next.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        # # Обработка нажатия стелки вправо
        # self.tk_windows.bind('<Right>', lambda *args,
        #                      **kwarg: self.TK_OnClickNext())
        # #
