import tkinter as tk
from tkinter import font as tkFont
import database
import random
import sys


# Widgets==============================================================================================================
class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.width = 800
        self.height = 400
        x = '200'
        y = '100'
        self.geometry(f'{str(self.width)}x{str(self.height)}+{x}+{y}')
        self.title('Age Of Gladiators')
        self.configure(bg='blue')
        self.resizable(False, False)
        # self.attributes("-fullscreen", True)


class Label(tk.Label):
    def __init__(self, *args, width=20, height=10, **kwargs):
        tk.Label.__init__(self, *args, width=width, height=height,
                          justify='left', anchor='nw', **kwargs)
        self.configure(font=FONT)
        self.configure(bg='#851f11')
        self.configure(fg='#eaba94')

    def update_current_state(self):
        self.configure(text='')


class PlayerMoneyLabel(Label):
    def __init__(self, **kwargs):
        Label.__init__(self, height=1, width=15, **kwargs)
        self.update_current_state()

    def update_current_state(self, ):
        self.configure(text=f'Септимы: {PLAYER.gold}')


# =======================================================================
class Listbox(tk.Listbox):
    def __init__(self, list_to_display, **kwargs):
        self.list_to_display = list_to_display
        self.elements_dict = {}
        tk.Listbox.__init__(self, **kwargs)

        self.configure(font=FONT)
        self.configure(bg='#851f11')
        self.configure(fg='#eaba94')
        self.configure(selectbackground='#eaba94')
        self.add_elements_to_listbox()

    def add_elements_to_listbox(self):
        for element in self.list_to_display:
            self.elements_dict[element.__repr__()] = element
        for element in self.elements_dict:
            self.insert('end', element)

    def get_valid_data(self):
        pass

    def update_current_state(self):
        self.clear()
        self.get_valid_data()
        self.add_elements_to_listbox()

    def clear(self):
        self.elements_dict = {}
        self.delete(0, 'end')

    def get_selected_element(self):
        selected_index = self.curselection()
        selected_element = self.get(selected_index)
        return selected_element


class MarketListbox(Listbox):
    def __init__(self, gladiators_list, **kwargs):
        self.gladiators_list = gladiators_list
        self.list_to_display = self.get_gladiators_to_show_from_gladiatorslist(
            self.gladiators_list)
        Listbox.__init__(self, self.list_to_display, **kwargs)

    def get_gladiators_to_show_from_gladiatorslist(self, gladiators_list):
        return gladiators_list.get_gladiators_for_market_current_day()

    def get_valid_data(self):
        self.list_to_display = self.get_gladiators_to_show_from_gladiatorslist(
            self.gladiators_list)

    def buy_gladiator(self, player):
        selected_gladiator_name = self.get_selected_element()
        gladiator = self.elements_dict[selected_gladiator_name]
        if player.gold < gladiator.price:
            print('У вас недостаточно денег')
            return

        gladiator.set_owner(player.name)
        gladiator.save_gladiator_in_db()

        player.gold -= gladiator.price
        player.save_data()

        UPDATER.update_elements()


class LanistaListbox(Listbox):
    def __init__(self, gladiators_list, **kwargs):
        self.gladiators_list = gladiators_list
        self.list_to_display = self.get_gladiators_to_show_from_gladiatorslist(
            self.gladiators_list)
        Listbox.__init__(self, self.list_to_display, **kwargs)

    def sell_gladiator(self, player):
        selected_gladiator_name = self.get_selected_element()
        gladiator = self.elements_dict[selected_gladiator_name]
        gladiator.set_owner(None)
        gladiator.save_gladiator_in_db()

        player.gold += gladiator.price
        player.save_data()

        UPDATER.update_elements()

    def get_gladiators_to_show_from_gladiatorslist(self, playername):
        return GLADIATORS_LIST.get_gladiators_from_db_for_player(playername)

    def get_valid_data(self):
        self.list_to_display = self.get_gladiators_to_show_from_gladiatorslist(
            self.gladiators_list)


class EnemyChoiseListbox(Listbox):
    pass
# ==============================================================================================================


class Text(tk.Text):
    pass


class FigthText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, width=60, height=15, **kwargs)
        self.configure(font=FONT)
        self.configure(bg='#851f11')
        self.configure(fg='#eaba94')
        self.configure(selectbackground='#eaba94')

    def update_current_state(self, ):
        self.delete('1.0', 'end')


# ==============================================================================================================

class Button(tk.Button):
    def __init__(self, width=15, height=2, *args, **kwargs):
        tk.Button.__init__(self, *args, height=height, width=width, **kwargs)

        self.configure(font=FONT)
        self.configure(bg='#851f11')
        self.configure(fg='#eaba94')
        self.configure(activebackground="#4e1207")


class Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, height=window.height,
                          width=window.width, **kwargs)

        canvas = tk.Canvas(self, width=window.width, height=window.height)
        canvas.place(x=0, y=0)
        self.photo = tk.PhotoImage(file='static/frames_bg/main_menu.png')
        canvas.create_image(
            window.width//2, window.height//2, image=self.photo)

        self.create_elements()
        self.grid_propagate(0)

    def create_elements(self):
        pass

    def show_listbox_information(self, listbox, label):
        selected_gladiator_name = listbox.get_selected_element()
        selected_gladiator_data = listbox.elements_dict[selected_gladiator_name]
        name = selected_gladiator_data.name
        crit = selected_gladiator_data.crit_chance
        hp = selected_gladiator_data.hp
        full_hp = selected_gladiator_data.max_hp
        level = selected_gladiator_data.level
        price = selected_gladiator_data.price
        evasion = selected_gladiator_data.evasion
        attack_power = selected_gladiator_data.attack_power
        winstreak = selected_gladiator_data.winstreak

        data = f'''
        Имя: {name}
        Атака: {attack_power}
        HP:{hp}/{full_hp}
        Уровень:{level}
        Крит: {crit}%
        Уклонение: {evasion}%

        Цена: {price}
        '''

        label.configure(text=data)


class CurrentFrame:
    def __init__(self, current_frame) -> None:
        self.current_frame = current_frame


class MainMenuFrame(Frame):
    def create_elements(self):
        self.to_market_button = Button(
            master=self, text='Магазин', command=lambda: frame_switcher.switch_to_frame(market))
        self.to_market_button.grid(column=0, row=1, pady=10)

        self.to_market_button = Button(
            master=self, text='Противники', command=lambda: frame_switcher.switch_to_frame(enemy_gladiators))
        self.to_market_button.grid(column=2, row=1)

        self.to_gladiators_button = Button(
            master=self, text='Гладиаторы', command=lambda: frame_switcher.switch_to_frame(gladiators))
        self.to_gladiators_button.grid(column=0, row=0, pady=10)

        self.next_day_button = Button(
            master=self, text='Следующий день', command=NEXT_DAY.next_day)
        self.next_day_button.grid(column=0, row=2, pady=10)

        self.to_battle_button = Button(
            master=self, text='К бою!', command=lambda: frame_switcher.switch_to_frame(prepare_to_fight))
        self.to_battle_button.grid(column=2, row=0)

        self.new_game_button = Button(
            master=self, text='Настройки', command=lambda: frame_switcher.switch_to_frame(settings_frame))
        self.new_game_button.grid(column=2, row=2, sticky='s', pady=10)

        self.exit_button = Button(
            master=self, text='Выход', command=sys.exit)
        self.exit_button.grid(column=2, row=3, sticky='s', pady=10)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)


class GladiatorsFrame(Frame):
    def create_elements(self):
        self.main_information_label = Label(master=self)
        self.main_information_label.grid(column=1, row=0, pady=10)

        self.main_listbox = LanistaListbox(
            'player', master=self, exportselection=False)
        self.main_listbox.bind('<<ListboxSelect>>', lambda event: self.show_listbox_information(
            self.main_listbox, self.main_information_label))
        self.main_listbox.grid(column=0, row=0, pady=10)

        self.to_market_button = Button(
            master=self, text='Магазин', command=lambda: frame_switcher.switch_to_frame(market))
        self.to_market_button.grid(column=1, row=2, pady=10)

        self.to_menu_button = Button(
            master=self, text='Назад', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.to_menu_button.grid(column=2, row=0, pady=10, sticky='n')

        self.player_money_label = PlayerMoneyLabel(master=self)
        self.player_money_label.grid(column=0, row=1, pady=10)

        self.sell_gladiator_button = Button(
            master=self, text='Продать', command=lambda: self.main_listbox.sell_gladiator(PLAYER))
        self.sell_gladiator_button.grid(column=0, row=2, pady=10)

        #self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)


class MarketFrame(Frame):
    def create_elements(self):
        self.back_to_gladiators_button = Button(
            master=self, text='Назад', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.back_to_gladiators_button.grid(
            column=2, row=0, pady=10, sticky='n')

        self.back_to_gladiators_button = Button(
            master=self, text='Гладиаторы', command=lambda: frame_switcher.switch_to_frame(gladiators))
        self.back_to_gladiators_button.grid(column=1, row=2, pady=10)

        self.main_information_label = Label(master=self)
        self.main_information_label.grid(column=1, row=0, pady=10)

        self.main_listbox = MarketListbox(
            GLADIATORS_LIST, master=self, exportselection=False)
        self.main_listbox.bind('<<ListboxSelect>>', lambda event: self.show_listbox_information(
            self.main_listbox, self.main_information_label))
        self.main_listbox.grid(column=0, row=0, pady=10)

        self.buy_gladiator_button = Button(
            master=self, text='Купить', command=lambda: self.main_listbox.buy_gladiator(PLAYER))
        self.buy_gladiator_button.grid(column=0, row=2, pady=10)

        self.player_money_label = PlayerMoneyLabel(master=self)
        self.player_money_label.grid(column=0, row=1, pady=10)

        self.grid_columnconfigure((0, 1, 2), weight=1)


class EnemyGladiatorsFrame(Frame):
    def create_elements(self):
        self.back_to_gladiators_button = Button(
            master=self, text='Назад', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.back_to_gladiators_button.grid(column=2, row=0, pady=10)

        self.main_information_label = Label(master=self)
        self.main_information_label.grid(column=1, row=0, pady=10)

        self.main_listbox = LanistaListbox(
            enemy.name, master=self, exportselection=False)
        self.main_listbox.bind('<<ListboxSelect>>', lambda event: self.show_listbox_information(
            self.main_listbox, self.main_information_label))
        self.main_listbox.grid(column=0, row=0)

        #self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)


class SettingsFrame(Frame):
    def create_elements(self):
        self.back_to_menu_button = Button(
            master=self, text='Новая игра', command=NewGame.new_game)
        self.back_to_menu_button.grid(column=0, row=0, pady=10)

        self.new_game_button = Button(
            master=self, text='Назад', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.new_game_button.grid(column=0, row=1, pady=10, sticky='s')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #self.grid_rowconfigure(1, weight=1)
        #self.grid_columnconfigure((0,1,2), weight=1)


class PrepeareToFight(Frame):
    def create_elements(self):
        self.main_information_label = Label(master=self)
        self.main_information_label.grid(column=1, row=0, pady=10)

        self.main_listbox = LanistaListbox(
            'player', master=self, exportselection=False)
        self.main_listbox.bind('<<ListboxSelect>>', lambda event: self.show_listbox_information(
            self.main_listbox, self.main_information_label))
        self.main_listbox.grid(column=0, row=0, pady=10)

        self.to_menu_button = Button(
            master=self, text='Назад', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.to_menu_button.grid(column=1, row=2, pady=10)

        self.enemy_choise_listbox = EnemyChoiseListbox(
            (enemy, 'Разработка'), master=self, exportselection=False)
        self.enemy_choise_listbox.grid(column=2, row=0, pady=10)

        self.to_menu_button = Button(
            master=self, text='В бой!', command=lambda: FIGHT.start(self.main_listbox, self.enemy_choise_listbox))
        self.to_menu_button.grid(column=1, row=1, pady=10)

        #self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)


class FightScreen(Frame):
    def create_elements(self):
        self.fight_text_space = FigthText(master=self)
        self.fight_text_space.grid(row=0, column=0, pady=10)

        self.to_menu_button = Button(
            master=self, text='Продолжить', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.to_menu_button.grid(row=1, column=0, pady=10)
        self.grid_columnconfigure(0, weight=1)

# Data:==============================================================================================================


class Gladiator:
    def __init__(self, *args) -> None:
        self.set_attributes(*args)
        self.calculate_attrs()

    def __repr__(self) -> str:
        return self.name

    def set_owner(self, owner: str):
        self.owner = owner

    def save_gladiator_in_db(self):
        DATABASE.execute(f'''update gladiators
                                SET name=?,
                                attack_power=?,
                                hp=?, owner=?,
                                is_dead=?,
                                level=?,
                                accuracy=?,
                                crit_chance=?,
                                evasion=?,
                                max_hp=?

                                WHERE name = ?
                                ''', (self.name,
                                      self.attack_power,
                                      self.hp,
                                      self.owner,
                                      self.is_dead,
                                      self.level,
                                      self.accuracy,
                                      self.crit_chance,
                                      self.evasion,
                                      self.max_hp,

                                      self.name))

    def calculate_attrs(self):
        price = int((self.hp*2.5+self.attack_power*4 +
                    self.crit_chance*10+self.evasion*10)*(self.level/2))
        if self.owner == 'player':
            price -= int(price*0.4)
        self.price = price

    def level_up(self):
        self.level += 1

        attrs_to_up = ('attack_power',
                       'accuracy',
                       'crit_chance',
                       'evasion',
                       'max_hp')

        random_attr = random.randint(0, len(attrs_to_up)-1)
        attr_to_up = attrs_to_up[random_attr]

        if attr_to_up == 'attack_power':
            self.attack_power += random.randint(5, 20)
        elif attr_to_up == 'accuracy':
            self.accuracy += random.randint(1, 2)
        elif attr_to_up == 'crit_chance':
            self.crit_chance += random.randint(2, 5)
        elif attr_to_up == 'evasion':
            self.evasion += random.randint(2, 5)
        elif attr_to_up == 'max_hp':
            self.attack_power += random.randint(10, 20)

        if self.accuracy > 95:
            self.accuracy = 95
        if self.evasion > 40:
            self.evasion = 40

        self.save_gladiator_in_db()

    def update_from_db(self):
        data_from_db_by_name = DATABASE.execute('select * from gladiators where name=?', (self.name, ))[0]
        self.set_attributes(*data_from_db_by_name)
    
    def set_attributes(self, id, name, attack_power, hp, owner, is_dead, level, winstreak, accuracy, crit_chance, evasion, max_hp):
        self.id = id
        self.name = name
        self.attack_power = attack_power
        self.hp = hp
        self.owner = owner
        self.is_dead = is_dead
        self.level = level
        self.winstreak = winstreak
        self.accuracy = accuracy
        self.crit_chance = crit_chance
        self.evasion = evasion
        self.max_hp = max_hp

        self.calculate_attrs()

class GladiatorsList:
    def __init__(self) -> None:
        self.gladiator_list = []
        self.database = DATABASE

        self.reset_gladiators_data()
        self.gladiators_for_market_current_day = self.get_gladiators_for_market_new_day()

    def reset_gladiators_data(self):
        self.gladiator_list = self.get_gladiators_from_db()

    def get_gladiators_from_db(self):
        raw_list_of_gladiators = self.database.execute(
            'select * from gladiators')
        gladiator_list = self.raw_gladiators_to_class_gladiator(
            raw_list_of_gladiators)
        return gladiator_list

    def raw_gladiators_to_class_gladiator(self, raw_list_of_gladiators):
        gladiator_list = []
        for raw_gladiator in raw_list_of_gladiators:
            gladiator = Gladiator(*raw_gladiator)
            gladiator.calculate_attrs()
            gladiator_list.append(gladiator)
        return gladiator_list

    def get_gladiators_from_db_for_player(self, playername):
        gladiators_from_db_for_player = []
        self.reset_gladiators_data()
        for gladiator in self.gladiator_list:
            if gladiator.owner == playername:
                if gladiator.is_dead == False:
                    gladiators_from_db_for_player.append(gladiator)
        return gladiators_from_db_for_player

    def get_gladiators_from_db_with_none_player(self):
        gladiators_from_db_for_market = self.get_gladiators_from_db_for_player(
            None)
        return gladiators_from_db_for_market

    def get_gladiators_for_market_current_day(self):
        if self.gladiators_for_market_current_day is None:
            self.get_gladiators_for_market_new_day()
        for gladiator in self.gladiators_for_market_current_day:
            if gladiator.owner is not None:
                self.gladiators_for_market_current_day.remove(gladiator)
        return self.gladiators_for_market_current_day

    def get_gladiators_for_market_new_day(self):
        free_gladiators = self.get_gladiators_from_db_with_none_player()
        gladiators_for_market = []
        for i in range(5):
            gladiator = self._check_unique(gladiators_for_market, free_gladiators)
            gladiators_for_market.append(gladiator)
        self.gladiators_for_market_current_day = gladiators_for_market

    def _check_unique(self, gladiators_for_market, free_gladiators):
        random_gladiator_index = random.randint(0, len(free_gladiators)-1)
        gladiator = free_gladiators[random_gladiator_index]
        if gladiator in gladiators_for_market:
            return self._check_unique(gladiators_for_market, free_gladiators)
        return gladiator

    def get_dead_gladiators_list(self):
        self.reset_gladiators_data()
        dead_gladiators_list = []
        for gladiator in self.gladiator_list:
            if gladiator.is_dead:
                dead_gladiators_list.append(gladiator)
        return dead_gladiators_list

          
    def create_gladiators_for_gladiator_list(self, gladiator_list):
        for gladiator in gladiator_list:
            attack_power = random.randint(10, 30)
            hp = 100
            max_hp = 100
            crit_chance = random.randint(0, 15)
            accuracy = random.randint(50, 75)
            evasion = random.randint(0, 15)
            level = 1
            owner = None
            is_dead=0

            DATABASE.execute('''update gladiators SET 
            attack_power=?,
            hp=?,
            max_hp=?,
            crit_chance=?,
            accuracy=?,
            evasion=?,
            level=?,
            owner=?,
            is_dead=?

            where name=?''', (
                attack_power,
                hp,
                max_hp,
                crit_chance,
                accuracy,
                evasion,
                level,
                owner,
                is_dead,

                gladiator.name
            ))


class FrameSwitcher:
    def switch_to_frame(self, frame_two: tk.Frame):
        CURRENT_FRAME.current_frame.pack_forget()
        frame_two.pack()
        CURRENT_FRAME.current_frame = frame_two
        UPDATER.update_elements()

# ==============================================================================================================


class Lanista:
    def __init__(self, name) -> None:
        self.name = name
        self.gladiators_list = GLADIATORS_LIST.get_gladiators_from_db_for_player(
            self.name)
        self.load_data()  # lanista_data
        self.gold = self.lanista_data[1]

    def load_data(self):
        select_from_db = DATABASE.execute(
            'select * from lanista_data where name=?', (self.name,))
        self.lanista_data = select_from_db[0]

    def get_random_gladiators(self):
        free_gladiators = GLADIATORS_LIST.get_gladiators_from_db_with_none_player()
        random_gladiator = random.randint(0, len(free_gladiators)-1)
        free_gladiators[random_gladiator].set_owner(self.name)
        free_gladiators[random_gladiator].save_gladiator_in_db()

    def choise_random_gladiator(self):
        self.gladiators_list = GLADIATORS_LIST.get_gladiators_from_db_for_player(
            self.name)

        gladiators_to_fight=[]

        for gladiator in self.gladiators_list:
            if gladiator.hp==gladiator.max_hp:
                gladiators_to_fight.append(gladiator)
        if gladiators_to_fight == []: gladiators_to_fight = self.gladiators_list

        random_index = random.randint(0, len(gladiators_to_fight)-1)
        random_gladiator = gladiators_to_fight[random_index]
        return random_gladiator

    def save_data(self):
        DATABASE.execute(
            'update lanista_data SET gold=? where name=?', (self.gold, self.name))

    def reset_data(self):
        self.gladiators_list = GLADIATORS_LIST.get_gladiators_from_db_for_player(
            self.name)
        self.load_data()  # lanista_data
        self.gold = self.lanista_data[1]

    def __repr__(self):
        return self.name


class EnemyLanista(Lanista):
    def __init__(self, name):
        Lanista.__init__(self, name)
        if self.gladiators_list == []:
            for i in range(5):
                self.get_random_gladiators()

    def reset_data(self):
        self.gladiators_list = GLADIATORS_LIST.get_gladiators_from_db_for_player(
            self.name)
        self.load_data()  # lanista_data
        self.gold = self.lanista_data[1]
        for i in range(5):
            self.get_random_gladiators()

    def buy_gladiator(self):
        lanista_gladiators_list = GLADIATORS_LIST.get_gladiators_from_db_for_player(
            self.name)
        if len(lanista_gladiators_list)<7:
            gladiator_list_to_buy = GLADIATORS_LIST.gladiators_for_market_current_day
            gladiator_list_to_buy.sort(key=lambda gladiator: gladiator.price, reverse=True)
            for gladiator in gladiator_list_to_buy:
                if self.gold>=gladiator.price:
                    self.gold-=gladiator.price
                    gladiator.owner = self.name
                    gladiator.save_gladiator_in_db()
            self.save_data()

class Player(Lanista):
    def pay_rent(self):
        lanista_gladiators_list = GLADIATORS_LIST.get_gladiators_from_db_for_player(
            self.name)
        for gladiator in lanista_gladiators_list:
            gladiator_rent = int(gladiator.price*0.1)
            self.gold-=gladiator_rent
        self.save_data()



class LanistaList:
    def __init__(self, *args) -> None:
        self.lanista_list = {}
        self.format_lanistas(*args)

    def format_lanistas(self, *args):
        for i in args:
            self.lanista_list[i.name] = i

    def get_lanista_by_name(self, name):
        return self.lanista_list[name]


# ==============================================================================================================

class Fight:
    def start(self, listbox_of_gladiators, listbox_of_enemies):
        selected_gladiator_name = listbox_of_gladiators.get_selected_element()
        selected_gladiator = listbox_of_gladiators.elements_dict[selected_gladiator_name]
        selected_enemy_name = listbox_of_enemies.get_selected_element()

        selected_enemy = listbox_of_enemies.elements_dict[selected_enemy_name]

        if not selected_gladiator:
            return
        if not selected_enemy:
            return

        if selected_enemy.name == 'Квинт':
            enemy_gladiator = enemy.choise_random_gladiator()
            frame_switcher.switch_to_frame(fight_screen)
            battle_result = self.fight(selected_gladiator, enemy_gladiator)
            if battle_result[0] == False:
                battle_result = ('Все погибли.', battle_result[1])
            fight_screen.fight_text_space.insert(
                'end', f'{battle_result[1]}\nПобедитель:{battle_result[0]}\nНаграда:{battle_result[2]}')

    def fight(self, member_one, member_two):
        battle_log = ''

        while True:
            crit_result = ''
            hit_result = self.hit(member_two, member_one)
            if hit_result['crit']:
                crit_result = 'критический '
            if hit_result['hit']:
                battle_log += f'{member_two.name} наносит {member_one.name} {crit_result}удар {hit_result["dmg"]}. {member_one.name}: {member_one.hp}HP\n'
            else:
                battle_log += f'{member_two.name} промахнулся.\n'

            crit_result = ''
            hit_result = self.hit(member_one, member_two)
            if hit_result['crit']:
                crit_result = 'критический '
            if hit_result['hit']:
                battle_log += f'{member_one.name} наносит {member_two.name} {crit_result}удар {hit_result["dmg"]}. {member_two.name}: {member_two.hp}HP\n\n'
            else:
                battle_log += f'{member_one.name} промахнулся.\n\n'

            if member_two.hp <= 0 and member_one.hp <= 0:
                reward_phrase = self.winner_update(False, (member_two, member_one))
                return False, battle_log, reward_phrase

            elif member_two.hp <= 0:
                reward_phrase = self.winner_update(member_one, member_two)
                return member_one, battle_log, reward_phrase

            elif member_one.hp <= 0:
                reward_phrase = self.winner_update(member_two, member_one)
                return member_two, battle_log, reward_phrase


    def winner_update(self, winner, loser):
        if winner:
            loser.is_dead = True
            bonus = 0
            winner.level_up()
            winner.save_gladiator_in_db()
            loser.save_gladiator_in_db()
            winner_lanista = LANISTA_LIST.get_lanista_by_name(winner.owner)

            if winner.price<loser.price:
                bonus = loser.price-winner.price
            reward = 300 + bonus*2
            winner_lanista.gold += reward
            winner_lanista.save_data()

            UPDATER.update_elements()
            return f'Победитель получает: {reward} септимов.'
        else:
            loser[0].is_dead = True
            loser[1].is_dead = True
            loser[0].save_gladiator_in_db()
            loser[1].save_gladiator_in_db()
            UPDATER.update_elements()
            return 'В этой битве нет победителя.'

    def hit(self, attacking_gladiator, defencing_gladiator):
        success_hit = False
        success_crit = False

        attacking_gladiator_attackpower = attacking_gladiator.attack_power

        chance_to_hit = attacking_gladiator.accuracy - defencing_gladiator.evasion
        chance_to_crit = attacking_gladiator.crit_chance

        random_number_for_hit = random.randint(0, 100)
        if chance_to_hit - random_number_for_hit > 0:
            success_hit = True

        random_number_for_crit = random.randint(0, 100)
        if chance_to_crit - random_number_for_crit > 0:
            success_crit = True

        random_generate_attack = random.randint(0, 100)
        random_bonus = random.randint(1, 10)
        if random_generate_attack - 50 > 0:
            attacking_gladiator_attackpower += int(
                attacking_gladiator_attackpower/100*random_bonus)
        else:
            attacking_gladiator_attackpower -= int(
                attacking_gladiator_attackpower/100*random_bonus)

        if success_hit:
            if success_crit:
                attacking_gladiator_attackpower *= 2
            defencing_gladiator.hp -= attacking_gladiator_attackpower

        return {'hit': success_hit, 'crit': success_crit, 'dmg': attacking_gladiator_attackpower}


class Updater:
    def update_elements(self):
        market.main_information_label.update_current_state()
        market.main_listbox.update_current_state()
        market.player_money_label.update_current_state()

        gladiators.main_information_label.update_current_state()
        gladiators.main_listbox.update_current_state()
        gladiators.player_money_label.update_current_state()

        prepare_to_fight.main_information_label.update_current_state()
        prepare_to_fight.main_listbox.update_current_state()

        fight_screen.fight_text_space.update_current_state()

        enemy_gladiators.main_listbox.update_current_state()


class NextDay:
    def next_day(self):
        self.gladiators_healing()
        enemy.buy_gladiator()
        GLADIATORS_LIST.get_gladiators_for_market_new_day()
        self._make_gladiators_alive()
        PLAYER.pay_rent()
        
        UPDATER.update_elements()

    def gladiators_healing(self):
        gladiators_list = GLADIATORS_LIST.get_gladiators_from_db()
        for gladiator in gladiators_list:
            if not gladiator.is_dead:
                if gladiator.hp < gladiator.max_hp:
                    gladiator.hp += 20
                    if gladiator.hp > gladiator.max_hp:
                        gladiator.hp = gladiator.max_hp
                    gladiator.save_gladiator_in_db()

    def _make_gladiators_alive(self):
        dead_gladiators_list = GLADIATORS_LIST.get_dead_gladiators_list()
        GLADIATORS_LIST.create_gladiators_for_gladiator_list(dead_gladiators_list)
        self._random_level_up_next_day(dead_gladiators_list)

    def _random_level_up_next_day(self, gladiators_list):
        NewGame.random_lvl_up(gladiators_list, count_gladiators_to_lvl_up=len(gladiators_list))

class NewGame:
    @classmethod
    def new_game(cls):
        DATABASE.reset_data()
        GLADIATORS_LIST.reset_gladiators_data()
        GLADIATORS_LIST.create_gladiators_for_gladiator_list(
            GLADIATORS_LIST.gladiator_list)
        GLADIATORS_LIST.get_gladiators_for_market_new_day()
        PLAYER.reset_data()
        cls.random_lvl_up(gladiators_list= GLADIATORS_LIST.get_gladiators_from_db_with_none_player())
        
        enemy.reset_data()
        
        UPDATER.update_elements() # Должен быть последним

    @classmethod
    def random_lvl_up(cls, gladiators_list, count_gladiators_to_lvl_up = 50):
        gladiators_count = len(gladiators_list)

        gladiators_to_lvlup_indexes = []
        for i in range(count_gladiators_to_lvl_up):
            random_gladiator_index = cls._get_lvlup_index(gladiators_to_lvlup_indexes, gladiators_count)
            gladiators_to_lvlup_indexes.append(random_gladiator_index)

        for index in gladiators_to_lvlup_indexes:
            random_level = random.randint(1, 5)
            for i in range(random_level):
                gladiators_list[index].update_from_db()
                gladiators_list[index].level_up()

    @classmethod
    def _get_lvlup_index(cls, gladiators_to_lvlup_indexes, gladiators_count):
        random_gladiator_index = random.randint(0, gladiators_count-1)

        if random_gladiator_index in gladiators_to_lvlup_indexes:
            return cls._get_lvlup_index(gladiators_to_lvlup_indexes, gladiators_count)
        return random_gladiator_index

    





DATABASE = database.Database('database.db')
GLADIATORS_LIST = GladiatorsList()
FIGHT = Fight()
UPDATER = Updater()
NEXT_DAY = NextDay()


PLAYER = Player('player')
enemy = EnemyLanista('Квинт')
LANISTA_LIST = LanistaList(PLAYER, enemy)

window = Window()
FONT = tkFont.Font(family='Helvetica', weight="bold")

main_menu = MainMenuFrame()
market = MarketFrame()
gladiators = GladiatorsFrame()
enemy_gladiators = EnemyGladiatorsFrame()
prepare_to_fight = PrepeareToFight()
fight_screen = FightScreen()
settings_frame = SettingsFrame()

CURRENT_FRAME = CurrentFrame(main_menu)


frame_switcher = FrameSwitcher()


main_menu.pack()
window.mainloop()
