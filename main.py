import os, platform
from Flashcards import Flashcards

prompt = '>> '

def ask_user(message:str = ''):
    '''
    Returns user input.
    '''
    raw_input = input(f'{prompt} {message}' if message else prompt).strip()
    return raw_input

def clear_console():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def run():
    '''
    Main program loop.
    '''
    fls = Flashcards()

    #Welcome message.
    clear_console()
    fls.set_page()

    while True:
        try:
            input = ask_user()
            if input in [c[0] for c in fls.get_commands()]:
                if input != 'sv': # Don't clear console on save.
                    clear_console()
                getattr(fls, input)()
            else:
                clear_console()
                fls.process_input(input)
        except KeyboardInterrupt:
            fls.exit()

if __name__ == "__main__":
    run()