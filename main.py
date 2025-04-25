import os, platform
from Flashcards import Flashcards

def clear_console():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def run():
    '''
    Main program loop.
    '''
    flashcards = Flashcards()

    #Welcome message.
    clear_console()
    flashcards.set_page()

    while True:
        try:
            input = flashcards.get_user_input()
            if input in [c[0] for c in flashcards.get_commands()]:
                if input != 'sv': # Don't clear console on save.
                    clear_console()
                getattr(flashcards, input)()
            else:
                clear_console()
                flashcards.process_input(input)
        except KeyboardInterrupt:
            flashcards.exit()

if __name__ == "__main__":
    run()