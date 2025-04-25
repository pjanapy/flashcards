import pickle, os, csv
import page_text
from global_variables import color
from Set import Set

class Flashcards:

    # List of available commands, with descriptions
    __commands = [
        ('home', 'Open home page.'),
        ('help', 'Display a list of available program instructions.'),
        ('back', 'Go to previous page.'),
        ('sv', 'Save current program state.'),
        ('ex', 'Exit without saving.'),
        ('xx', 'Save and exit.'),
    ]
    
    ''' 
    Dictionary of available program pages.
    '''
    __game_pages = {
        'root': {
            'accepts': 'option',
            'options': {
                1: 'set_selection',
                2: 'set_instatiation',
                3: 'set_deletion'
            }
        },
        'back_home': {
            'accepts': 'text',
            'action': 'home'
        },
        'set_instatiation': {
            'accepts': 'text',
            'action': 'create_set'
        },
        'choose_set_action': {
            'accepts': 'option',
            'options': {
                1: 'set_selection',
                2: 'set_instatiation',
                3: 'set_deletion'
            }    
        },
        'set_deletion': {
            'accepts': 'text',
            'pre_action': 'print_sets',
            'action': 'delete_set'
        },
        'set_selection': {
            'accepts': 'text',
            'pre_action': 'print_sets',
            'action': 'select_set'
        },
        'set_options': {
            'accepts': 'option',
            'options': {
                1: 'play',
                2: 'add_flashcard',
                3: 'edit_flashcards',
                4: 'import_flashcards',
                5: 'view_statistics'
            }
        },
        'edit_flashcards': {
            'accepts': 'text',
            'pre_action': 'print_flashcards',
            'action': 'delete_flashcard'
        },
        'play': {
            'accepts': 'text',
            'pre_action': 'draw_card',
            'action': 'evaluate_answer'
        },
        'add_flashcard': {
            'accepts': 'text',
            'action': 'add_flashcard'
        },
        'view_statistics': {
            'accepts': 'text',
            'pre_action': 'show_statistics'
        },
        'import_flashcards': {
            'accepts': 'text',
            'pre_action': 'print_import',
            'action': 'import_flashcards'
        },
    }

    # Location of data file.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(base_dir, "data.pkl")
    imports_dir_path = os.path.join(base_dir, "imports/")

    def __init__(self):
        self.prompt = '>> '
        self.game_page = 'root'
        self.data = self.load()
        self.new_set = {}
        self.new_flashcard = None
        self.sets = []
        self.selected_set = None
        self.selected_set_name = None
        self.current_card = None
        self.last_question = None
        self.page_history = ['root']
        self.current_cards = None
        self.attempts = 0
        if 'sets' in self.data:
            for set in self.data['sets']:
                self.sets.append(Set(set.name,
                                     set.description,
                                     set.cards,
                                     set.played_cards,
                                     set.statistics)
                                )
    
    def get_user_input(self, message:str = ''):
        '''
        Returns user input.
        '''
        raw_input = input(f'{self.prompt} {message}' if message else self.prompt).strip()
        return raw_input

    def process_input(self, input):
        '''
        Processes user input based on current value of __game_page.
        '''
        page_data = self.__game_pages[self.game_page]

        if page_data['accepts'] == 'option':
            last_page = self.game_page
            if self.is_int(input):
                try:
                    page = page_data['options'][int(input)]
                    self.set_page(page)
                except KeyError:
                    print(f'{color['WARNING']}There is no option with value: {input}{color['RESET']}')
                    self.set_page(self.game_page)
            else:
                print(f'{color['WARNING']}Invalid input.{color['RESET']}')
                self.set_page(last_page)
        elif page_data['accepts'] == 'text':
            try:
                action = page_data['action']
                getattr(self, action)(input=input)
            except KeyError:
                return 1

    def set_page(self, page = ''):
        '''
        Loads page and prints it's contents.
        '''
        if page == '':
            page =  self.game_page
        if page in list(self.__game_pages.keys()):
            self.game_page = page
            self.page_history.append(page)
            print(getattr(page_text, page + '_page')[0])
            if 'pre_action' in self.__game_pages[page]:
                pre_action = self.__game_pages[page]['pre_action']
                getattr(self, pre_action)()
        else:
            print(f'{color['WARNING']}Page {page} doesn\'t exist.{color['RESET']}')
            self.set_page(self.game_page)

    def help(self):
        '''
        Prints help page.
        '''
        self.set_page('back_home')
        print(getattr(page_text, 'help_page')[0])
        print(color['ACCENT'] + '{:<10}{}'.format('Command', 'Description') + color['RESET'])
        for item in self.__commands:
            it = f'{color['COMMAND']}{item[0]}{color['RESET']}'
            print('{:<19}{}'.format(it, item[1]))
    
    def load(self):
        data = {}
        if os.path.getsize(self.data_file_path) > 0:
            with open(self.data_file_path, 'rb') as f:
                data = pickle.load(f)
        return data
        
    def sv(self, message = ''):
        self.data['sets'] = self.sets
        with open(self.data_file_path, "wb") as f:
            print(f'{color['ACCENT']}Saving data. {message}{color['RESET']}')
            pickle.dump(self.data, f)
        return
    
    def xx(self):
        message = f'{color['ACCENT']}Program closed.{color['RESET']}'
        self.sv(message)
        exit(0)
    
    def ex(self):
        print(f'{color['ACCENT']}Program closed without saving.{color['RESET']}')
        exit(0)

    def home(self, input=''):
        '''
        Sets page to system's root page.
        '''
        self.selected_set = None
        self.selected_set_name = None
        self.set_page('root')
            
    def back(self):
        if len(self.page_history) > 1:
            page = self.page_history[-2]
            self.page_history = ['root']
            self.set_page(page)

    def create_set(self, input):
        if 'name' not in self.new_set:
            if len(input) != 0:
                self.new_set['name'] = input # Gives new temp set a name
                print(page_text.set_instatiation_page[1])
            else:
                print(f'{color['WARNING']}Set name cannot be empty.{color['RESET']}')
                self.set_page('set_instatiation')
        else:
            self.sets.append(Set(self.new_set['name'], input)) # Creates a Set
            print(f'{color['ACCENT']}New set \'{self.new_set['name']}\' has been added.{color['RESET']}')
            self.new_set = {}
            self.set_page('choose_set_action')

    def print_sets(self):
        if len(self.sets) != 0:
            print(color['ACCENT'] + '{:<5}{:<15}{}'.format('No.', 'Name', 'Description') + color['RESET'])
            for i, set in enumerate(self.sets):
                num = '['  + color['NUMBER'] + str(i + 1) + color['RESET'] + ']'
                print('{:<14}{:<15}{}'.format(num ,set.name, set.description))
        else:
            print(f'{color['ACCENT']}No available sets. First create one.{color['RESET']}')
            self.set_page('choose_set_action')

    def print_flashcards(self):
        self.current_cards = self.selected_set.get_cards()
        print(color['ACCENT'] +'{:<5}{:<30}{}'.format('No.', 'Question', 'Answer') + color['RESET'])
        for i, card in enumerate(self.current_cards, 1):
            num = '['  + color['NUMBER'] + str(i) + color['RESET'] + ']'
            print('{:<14}{:<30}{}'.format(num, card[0][:29], card[1][:19]))

    def delete_flashcard(self, input):
        try:
            number = input.split()[1]
            if self.is_int(number) and input.split()[0] == 'del':
                self.selected_set.delete_card(self.current_cards[int(number) - 1])
                self.current_cards.remove(self.current_cards[int(number) - 1])
                print(f'{color['ACCENT']}Card removed.{color['RESET']}')
        except KeyError:
            print(f'{color['WARNING']}Wrong card number.{color['RESET']}')
        except IndexError:
            print(f'{color['WARNING']}Incorrect syntax.{color['RESET']}')

        self.set_page('edit_flashcards')
    
    def print_import(self):
        file_list = os.listdir(self.imports_dir_path)
        file_list = [f for f in file_list if os.path.isfile(os.path.join(self.imports_dir_path, f))]
        
        if len(file_list) > 0:
            print('Available files:')
            for file in file_list:
                print(f'{color['ACCENT']}{file}{color['RESET']}')

    def import_flashcards(self, input):
        if len(input) > 0:
            data = []
            try:
                with open(self.imports_dir_path + input, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        data.append(tuple(row))
            except FileNotFoundError:
                print(f"Error: The file '{input}' was not found.")
            except UnicodeDecodeError:
                print(f"Error: Encoding issue while reading '{input}'.")
            except csv.Error as e:
                print(f"CSV format error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            else:
                print(f"File '{input}' loaded successfully with {len(data)} rows.")
            finally:
                print("Import process finished.")
                self.selected_set.import_cards(data)
        else:
            print('Wrong input.')        
            self.print_import()

    def select_set(self, input):
        if self.is_int(input) and int(input) > 0:
            for i, set in enumerate(self.sets):
                if i == int(input) - 1:
                    print(f'Selected set: "{color['ACCENT']}{set.name}"{color['RESET']}')
                    self.selected_set = set
                    self.selected_set_name = set.name
                    self.set_page('set_options')
                    return
                
        print(f'{color['WARNING']}Set doesn\'t exist.{color['RESET']}')
        self.set_page('choose_set_action')

    def delete_set(self, input):
        if len(input) != 0:
            for set in self.sets:
                if set.name == input:
                    self.sets.remove(set)
                    if self.selected_set_name == input:
                        self.selected_set_name = None
                        self.selected_set = None
                    print(f'{color['ACCENT']}Set {input} deleted.{color['RESET']}')
                    self.set_page('choose_set_action')
                    return
        print(f'{color['WARNING']}Set doesn\'t exist.{color['RESET']}')
        self.set_page('choose_set_action')

    def draw_card(self):
        self.current_card = self.selected_set.get_card()
        if self.current_card:
            self.last_question = self.current_card[0]
            self.selected_set.add_games_count()
            print(self.last_question)
        else:
            print(f'{color['WARNING']}Set doesn\'t have flashcards yet!{color['RESET']}')
            for i, set in enumerate(self.sets):
                if set.name == self.selected_set_name:
                    self.select_set(i + 1)
                    break

    def evaluate_answer(self, input):
        if input == self.current_card[1]:
            print(f'{color['ACCENT']}Correct!.{color['RESET']}')
            if self.attempts == 0:
                self.selected_set.add_score(1)
            elif self.attempts == 1:
                self.selected_set.add_score(0.5)
            self.attempts = 0
            self.draw_card()
        else:
            self.attempts += 1
            if self.attempts < 2:
                print(f'{color['WARNING']}Wrong answer! Try again.{color['RESET']}')
                print(self.current_card[0])
            else:
                print(f'{color['WARNING']}Wrong answer!{color['RESET']}')
                print(f'Correct answer should be: ' + self.current_card[1])
                self.attempts = 0
                self.draw_card()
        return

    def add_flashcard(self, input):
        if self.new_flashcard is None:
            if len(input) != 0:
                self.new_flashcard = input
                print(page_text.add_flashcard_page[1])
            else:
                print(f'{color['WARNING']}Flashcard question cannot be empty.{color['RESET']}')
                self.set_page('add_flashcard')
        else:
            self.selected_set.add_card(self.new_flashcard, input)
            print(f'{color['ACCENT']}New card added.{color['RESET']}')
            self.new_flashcard = None
            self.set_page('set_options')

    def show_statistics(self):
        stats = self.selected_set.statistics
        percent_correct = 0
        if stats['games_count'] > 0 :
            percent_correct = round(stats['score'] / stats['games_count'] * 100, 2)
        print(f'{color['ACCENT']}Statistics for set "{self.selected_set.name}"{color['RESET']}')
        print(f'Flashcards played: {color['NUMBER']}{self.selected_set.statistics['games_count']}{color['RESET']}')
        print(f'Score: {color['NUMBER']}{percent_correct}%{color['RESET']}')
        print('-------------------')
        self.set_page('set_options')

    def is_int(self, i):
        try:
            int(i)
            return True
        except ValueError:
            return False
            
    @classmethod
    def get_commands(cls):
        return cls.__commands
    
    @classmethod
    def get_game_page(cls):
        return cls.game_page
    