import tkinter as tk
from tkinter import ttk
import database
import random


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

class Label(tk.Label):
    def __init__(self, width=15, height=15, *args, **kwargs):
        tk.Label.__init__(self, width=width, height=height, justify='left', anchor='nw', *args, **kwargs)
    def update_current_state(self, ):
        self.configure(text='')
#=======================================================================
class Listbox(tk.Listbox):
    def __init__(self, list_to_display, **kwargs):
        self.list_to_display = list_to_display
        self.elements_dict = {}
        tk.Listbox.__init__(self, **kwargs)
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
        return gladiators_list.get_gladiators_from_db_for_market()

    def get_valid_data(self):
        self.list_to_display = self.get_gladiators_to_show_from_gladiatorslist(
            self.gladiators_list)

    def buy_gladiator(self, player):
        selected_gladiator_name = self.get_selected_element()
        gladiator = self.elements_dict[selected_gladiator_name]
        if player.gold<gladiator.price:
            print('У вас недостаточно денег')
            return

        gladiator.set_owner(player.name)
        gladiator.save_gladiator_in_db()

        player.gold-=gladiator.price
        player.save_data()

        self.update_current_state()

class LanistaListbox(Listbox):
    def __init__(self, gladiators_list, **kwargs):
        self.gladiators_list = gladiators_list
        self.list_to_display = self.get_gladiators_to_show_from_gladiatorslist(
            self.gladiators_list)
        Listbox.__init__(self, self.list_to_display, **kwargs)

    def get_gladiators_to_show_from_gladiatorslist(self, gladiators_list):
        return gladiators_list.get_gladiators_from_db_for_player()

    def sell_gladiator(self, player, gladiators_list):
        selected_gladiator_name = self.get_selected_element()
        gladiator = self.elements_dict[selected_gladiator_name]
        gladiator.set_owner(None)
        gladiator.save_gladiator_in_db()
        self.update_current_state()

    def get_gladiators_to_show_from_gladiatorslist(self, playername):
        return GLADIATORS_LIST.get_gladiators_from_db_for_player(playername)

    def get_valid_data(self):
        self.list_to_display = self.get_gladiators_to_show_from_gladiatorslist(
            self.gladiators_list)

class EnemyChoiseListbox(Listbox):
    pass
#==============================================================================================================
class Text(tk.Text):
    pass

class FigthText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, width=60, height=20, **kwargs)


#==============================================================================================================

class Button(tk.Button):
    def __init__(self, width = 30, height = 2, *args, **kwargs):
        tk.Button.__init__(self, height = height, width = width, *args, **kwargs)

class Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, height=window.height, width=window.width, **kwargs)
        self.create_elements()
        self.grid_propagate(0)

    def create_elements(self):
        pass

    def show_listbox_information(self, listbox, label):
        selected_gladiator_name = listbox.get_selected_element()
        selected_gladiator_data = listbox.elements_dict[selected_gladiator_name]
        name = selected_gladiator_data.name
        hp = selected_gladiator_data.hp
        full_hp = selected_gladiator_data.hp
        level = selected_gladiator_data.level
        price = selected_gladiator_data.price
        data = f'''
        Имя: {name}
        HP:{full_hp}/{hp}
        Уровень:{level}
        Цена: {price}
        '''

        label.configure(text = data)

class CurrentFrame:
    def __init__(self, current_frame) -> None:
        self.current_frame = current_frame

class MainMenuFrame(Frame):
    def create_elements(self):
        self.to_market_button = Button(
            master=self, text='В магазин', command=lambda: frame_switcher.switch_to_frame(market))
        self.to_market_button.grid(column=0, row=1)

        self.to_market_button = Button(
            master=self, text='Осмотреть гладиаторов противника', command=lambda: frame_switcher.switch_to_frame(enemy_gladiators))
        self.to_market_button.grid(column=2, row=1)

        self.to_gladiators = Button(
            master=self, text='Ваши Гладиаторы', command=lambda: frame_switcher.switch_to_frame(gladiators))
        self.to_gladiators.grid(column=0, row=0)

        self.to_gladiators = Button(
            master=self, text='Подготовка к следующему бою', command=lambda: frame_switcher.switch_to_frame(prepare_to_fight))
        self.to_gladiators.grid(column=2, row=0)
        
        #self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)

class GladiatorsFrame(Frame):
    def create_elements(self):
        self.main_information_label = Label(master=self)
        self.main_information_label.grid(column=1, row=0)

        self.main_listbox = LanistaListbox('player', master=self, exportselection=False)
        self.main_listbox.bind('<<ListboxSelect>>', lambda event: self.show_listbox_information(self.main_listbox, self.main_information_label))
        self.main_listbox.grid(column=0, row=0)

        self.to_market_button = Button(
            master=self, text='В магазин', command=lambda: frame_switcher.switch_to_frame(market))
        self.to_market_button.grid(column=2, row=0)

        self.to_market_button = Button(
            master=self, text='Вернуться', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.to_market_button.grid(column=0, row=2)

        self.sell_gladiator_button = Button(master=self, text='Продать', command=lambda: UPDATER.operation(
            self.main_listbox.sell_gladiator(PLAYER, GLADIATORS_LIST)))
        self.sell_gladiator_button.grid(column=0, row=1)

        
        #self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)

class MarketFrame(Frame):
    def create_elements(self):
        self.back_to_gladiators_button = Button(
            master=self, text='Вернуться', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.back_to_gladiators_button.grid(column=2, row=0)

        self.back_to_gladiators_button = Button(
            master=self, text='Ваши Гладиаторы', command=lambda: frame_switcher.switch_to_frame(gladiators))
        self.back_to_gladiators_button.grid(column=1, row=1)

        self.main_information_label = Label(master=self)
        self.main_information_label.grid(column=1, row=0)

        self.main_listbox = MarketListbox(GLADIATORS_LIST, master=self, exportselection=False)
        self.main_listbox.bind('<<ListboxSelect>>', lambda event: self.show_listbox_information(self.main_listbox, self.main_information_label))
        self.main_listbox.grid(column=0, row=0)

        self.buy_gladiator_button = Button(master=self, text='Купить', command=lambda: UPDATER.operation(
            self.main_listbox.buy_gladiator(PLAYER)))
        self.buy_gladiator_button.grid(column=0, row=1)

        
        #self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)

class EnemyGladiatorsFrame(Frame):
    def create_elements(self):
        self.back_to_gladiators_button = Button(
            master=self, text='Вернуться', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.back_to_gladiators_button.grid(column=2, row=0)

        self.main_information_label = Label(master=self)
        self.main_information_label.grid(column=1, row=0)

        self.main_listbox = LanistaListbox(enemy.name, master=self, exportselection=False)
        self.main_listbox.bind('<<ListboxSelect>>', lambda event: self.show_listbox_information(self.main_listbox, self.main_information_label))
        self.main_listbox.grid(column=0, row=0)
        
        #self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)


class PrepeareToFight(Frame):
    def create_elements(self):
        self.main_information_label = Label(master=self)
        self.main_information_label.grid(column=1, row=0)

        self.main_listbox = LanistaListbox('player', master=self, exportselection=False)
        self.main_listbox.bind('<<ListboxSelect>>', lambda event: self.show_listbox_information(self.main_listbox, self.main_information_label))
        self.main_listbox.grid(column=0, row=0)

        self.to_menu_button = Button(
            master=self, text='Вернуться', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.to_menu_button.grid(column=1, row=2)

        self.enemy_choise_listbox = EnemyChoiseListbox((enemy, 'Случайный противник'), master=self, exportselection=False)
        self.enemy_choise_listbox.grid(column=2, row=0)

        self.to_menu_button = Button(
            master=self, text='Сразиться', command=lambda: FIGHT.start(self.main_listbox, self.enemy_choise_listbox))
        self.to_menu_button.grid(column=1, row=1)
        
        #self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)

class FightScreen(Frame):
    def create_elements(self):
        self.fight_text_space = FigthText(master=self)
        self.fight_text_space.grid(row=0, column=0)

        self.to_menu_button = Button(
        master=self, text='Вернуться', command=lambda: frame_switcher.switch_to_frame(main_menu))
        self.to_menu_button.grid(row=1, column=0)
        self.grid_columnconfigure(0, weight=1)

# Data:==============================================================================================================

class Gladiator:
    def __init__(self, id, name, attack_power, hp, owner, is_dead, level, price, winstreak) -> None:
        self.id = id
        self.name = name
        self.attack_power = attack_power
        self.hp = hp
        self.owner = owner
        self.is_dead = is_dead
        self.level = level
        self.winstreak = winstreak
        if price == None:
            price = int(self.hp*2.5+self.attack_power*4)
        self.price = price

    def __repr__(self) -> str:
        return self.name

    def set_owner(self, owner: str):
        self.owner = owner

    def save_gladiator_in_db(self):
        DATABASE.execute(f'''update gladiators
                                SET name=?, attack_power=?, hp=?, owner=?, is_dead=?, level=?, price=?
                                WHERE name = ?
                                ''', (self.name, self.attack_power, self.hp, self.owner, self.is_dead, self.level, self.price, self.name))

class GladiatorsList:
    def __init__(self) -> None:
        self.database = DATABASE
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
            gladiator_list.append(Gladiator(*raw_gladiator))
        return gladiator_list

    def get_gladiators_from_db_for_player(self, playername):
        gladiators_from_db_for_player = []
        for gladiator in self.gladiator_list:
            if gladiator.owner == playername:
                if gladiator.is_dead == False:
                    gladiators_from_db_for_player.append(gladiator)
        return gladiators_from_db_for_player

    def get_gladiators_from_db_for_market(self):
        gladiators_from_db_for_market = self.get_gladiators_from_db_for_player(
            None)
        return gladiators_from_db_for_market

    

class Updater:
    def __init__(self, elements) -> None:
        self.elements = elements

    def operation(self, operation):
        operation
        self.update_elements()
        

    def update_elements(self):
        for element in self.elements:
            element.main_listbox.update_current_state(),
            element.main_information_label.update_current_state()


class FrameSwitcher:
    def switch_to_frame(self, frame_two: tk.Frame):
        CURRENT_FRAME.current_frame.pack_forget()
        frame_two.pack()
        CURRENT_FRAME.current_frame = frame_two

#==============================================================================================================

class Lanista:
    def __init__(self, name) -> None:
        self.name = name
        self.gladiators_list = GLADIATORS_LIST.get_gladiators_from_db_for_player(self.name)
        self.load_data() #lanista_data
        self.gold = self.lanista_data[1]

    def load_data(self):
        select_from_db = DATABASE.execute('select * from lanista_data where name=?', (self.name,))
        self.lanista_data = select_from_db[0]
        

    def get_random_gladiators(self):
        free_gladiators = GLADIATORS_LIST.get_gladiators_from_db_for_market()
        random_gladiator = random.randint(0, len(free_gladiators)-1)
        free_gladiators[random_gladiator].set_owner(self.name)
        free_gladiators[random_gladiator].save_gladiator_in_db()

    def choise_random_gladiator(self):
        self.gladiators_list = GLADIATORS_LIST.get_gladiators_from_db_for_player(self.name)
        random_index = random.randint(0, len(self.gladiators_list)-1)
        random_gladiator = self.gladiators_list[random_index]
        return random_gladiator

    def save_data(self):
        DATABASE.execute('update lanista_data SET gold=? where name=?', (self.gold,self.name))


    def __repr__(self):
        return self.name

class EnemyLanista(Lanista):
    def __init__(self, name):
        Lanista.__init__(self, name)
        if self.gladiators_list == []: 
            for i in range(5):
                self.get_random_gladiators()

class Player(Lanista):
    pass

#==============================================================================================================

class Fight:
    def start(self, listbox_of_gladiators, listbox_of_enemies):
        selected_gladiator_name = listbox_of_gladiators.get_selected_element()
        selected_gladiator = listbox_of_gladiators.elements_dict[selected_gladiator_name]

        selected_enemy_name = listbox_of_enemies.get_selected_element()
        selected_enemy = listbox_of_enemies.elements_dict[selected_enemy_name]

        if not selected_gladiator:return
        if not selected_enemy:return

        if selected_enemy.name=='Квинт':
            enemy_gladiator = enemy.choise_random_gladiator()
            frame_switcher.switch_to_frame(fitght_screen)
            battle_result = self.fight(selected_gladiator, enemy_gladiator)
            if battle_result[0] == False:
                battle_result = ('Все погибли.', battle_result[1])
            fitght_screen.fight_text_space.insert('end', f'{battle_result[1]}\nПобедитель:{battle_result[0]}')


    def fight(self, member_one, member_two):
        battle_log = ''

        member_one_hp = member_one.hp
        member_two_hp = member_two.hp

        while True:
            member_two_hp = member_two_hp - member_one.attack_power
            battle_log+=f'{member_one.name} наносит {member_two.name} удар {member_one.attack_power}. {member_two.name}: {member_two_hp}HP\n'

            member_one_hp = member_one_hp - member_two.attack_power
            battle_log+=f'{member_two.name} наносит {member_one.name} удар {member_two.attack_power}. {member_one.name}: {member_one_hp}HP\n'


            if member_two_hp<=0 and member_one_hp<=0:
                self.winner_update(False, (member_two, member_one))
                return False, battle_log

            elif member_two_hp<=0:
                self.winner_update(member_one, member_two)
                return member_one, battle_log

            elif member_one_hp<=0:
                self.winner_update(member_two, member_one)
                return member_two, battle_log
        
    def winner_update(self, winner, loser):
        if winner:
            loser.is_dead = True
            winner.level+=1
            winner.save_gladiator_in_db()
            loser.save_gladiator_in_db()
            UPDATER.update_elements()
        else:
            loser[0].is_dead = True
            loser[1].is_dead = True
            loser[0].save_gladiator_in_db()
            loser[1].save_gladiator_in_db()
            UPDATER.update_elements()



DATABASE = database.Database('database.db')
GLADIATORS_LIST = GladiatorsList()
FIGHT = Fight()


PLAYER = Player('player')
enemy = EnemyLanista('Квинт')

window = Window()
main_menu = MainMenuFrame()
market = MarketFrame()
gladiators = GladiatorsFrame()
enemy_gladiators = EnemyGladiatorsFrame()
prepare_to_fight = PrepeareToFight()
fitght_screen = FightScreen()

CURRENT_FRAME = CurrentFrame(main_menu)

frame_switcher = FrameSwitcher()

UPDATER = Updater(
    (gladiators, market, enemy_gladiators, prepare_to_fight))




main_menu.pack()
window.mainloop()