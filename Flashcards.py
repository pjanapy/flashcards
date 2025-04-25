import pickle, os
import pages
from Set import Set

class Flashcards:
    '''
    TODO:
        - scoring system,
        - display of the correct answer after two failed attempts,
        - autocomplete system for typing (set names),
        - statistics (player stats, set summary, number of flashcards, etc.),
        - import of a flashcard set from a CSV file,
        - saving the active set and automatically loading it when the program starts,
          with quick access to switch between sets,
    '''

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
                1: 'set_instatiation',
                2: 'set_selection',
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
                1: 'set_instatiation',
                2: 'set_selection',
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
                4: 'view_statistics'
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
    }

    # Location of data file.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(base_dir, "data.pkl")

    def __init__(self):
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
        if 'sets' in self.data:
            for set in self.data['sets']:
                self.sets.append(Set(set.name,
                                     set.description,
                                     set.cards,
                                     set.played_cards,
                                     set.statistics)
                                )
    
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
                    print('There is no option with value ' + input)
            else:
                print('\033[31mInvalid input.\033[0m')
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
            print(getattr(pages, page + '_page')[0])
            if 'pre_action' in self.__game_pages[page]:
                pre_action = self.__game_pages[page]['pre_action']
                getattr(self, pre_action)()
        else:
            print(f'Page {page} doesn\'t  exist.')

    def help(self):
        '''
        Prints help page.
        '''
        self.set_page('back_home')
        print(getattr(pages, 'help_page')[0])
        print('\033[32m{:<20}{}\033[0m'.format('Command', 'Description'))
        for item in self.__commands:
            print('{:<20}{}'.format(item[0], item[1]))

    def sv(self):
        self.data['sets'] = self.sets
        with open(self.data_file_path, "wb") as f:
            print('\033[31mSaving data.\033[0m')
            pickle.dump(self.data, f)
        return
    
    def load(self):
        data = {}
        if os.path.getsize(self.data_file_path) > 0:
            with open(self.data_file_path, 'rb') as f:
                data = pickle.load(f)
        return data
    
    def back(self):
        if len(self.page_history) > 1:
            page = self.page_history[-2]
            self.page_history = ['root']
            self.set_page(page)

    def xx(self):
        self.sv()
        print('\033[31mSystem closed.\033[0m')
        exit(0)
    
    def ex(self):
        print('\033[31mSystem closed.\033[0m')
        exit(0)

    def home(self, input=''):
        '''
        Sets page to system's root page.
        '''
        self.selected_set = None
        self.selected_set_name = None
        self.set_page('root')
            
    def create_set(self, input):
        if 'name' not in self.new_set:
            if len(input) != 0:
                self.new_set['name'] = input # Gives new temp set a name
                print(pages.set_instatiation_page[1])
            else:
                print('\033[31mSet name cannot be empty.\033[0m')
                self.set_page('set_instatiation')
        else:
            self.sets.append(Set(self.new_set['name'], input)) # Creates a Set
            print(f'\033[32mNew set \'{self.new_set['name']}\' has been added.\033[0m')
            self.new_set = {}
            self.set_page('choose_set_action')

    def print_sets(self):
        if len(self.sets) != 0:
            print('\033[32m{:<20}{}\033[0m'.format('Name', 'Description'))
            for set in self.sets:
                print('{:<20}{}'.format(set.name, set.description))
        else:
            print('\033[31mNo available sets. First create one.\033[0m')
            self.set_page('choose_set_action')

    def print_flashcards(self):
        self.current_cards = self.selected_set.get_cards()
        print('{:<16}{:<16}{}'.format('Number', 'Question', 'Answer'))
        for i, card in enumerate(self.current_cards, 1):
            print('{:<16}{:<16}{}'.format(i, card[0][:15], card[1][:15]))

    def delete_flashcard(self, input):
        try:
            number = input.split()[1]
            if self.is_int(number) and input.split()[0] == 'delete':
                self.selected_set.delete_card(self.current_cards[int(number) - 1])
                self.current_cards.remove(self.current_cards[int(number) - 1])
                print('\033[31mCard removed\033[0m')
        except KeyError:
            print('No such card number.')
        except IndexError:
            print('Use correct syntax.')

        self.set_page('edit_flashcards')

    def select_set(self, input):
        if len(input) != 0:
            for set in self.sets:
                if set.name == input:
                    print(f'You selected set \033[32m{input}\033[0m.')
                    self.selected_set = set
                    self.selected_set_name = input
                    self.set_page('set_options')
                    return
                
        print('\033[31mThe specified set does not exist.\033[0m')
        self.set_page('choose_set_action')

    def delete_set(self, input):
        if len(input) != 0:
            for set in self.sets:
                if set.name == input:
                    self.sets.remove(set)
                    if self.selected_set_name == input:
                        self.selected_set_name = None
                        self.selected_set = None
                    print(f'Set {input} deleted.')
                    self.set_page('choose_set_action')
                    return
        print('\033[31mThe specified set does not exist.\033[0m')
        self.set_page('choose_set_action')

    def draw_card(self):
        self.current_card = self.selected_set.get_card()
        if self.current_card:
            self.last_question = self.current_card[0]
            print(self.last_question)

    def evaluate_answer(self, input):
        if input == self.current_card[1]:
            print('\033[32mCorrect!.\033[0m')
            self.draw_card()
        else:
            print('\033[31mWrong answer! Try again.\033[0m')
            print(self.last_question)
        return

    def add_flashcard(self, input):
        if self.new_flashcard is None:
            if len(input) != 0:
                self.new_flashcard = input
                print(pages.add_flashcard_page[1])
            else:
                print('\033[31mFlashcard question cannot be empty.\033[0m')
                self.set_page('add_flashcard')
        else:
            self.selected_set.add_card(self.new_flashcard, input)
            print(f'\033[32mNew card added.\033[0m')
            self.new_flashcard = None
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
    