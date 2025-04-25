root_page = ['''Welcome to the \033[32mFlashcards\033[0m!
Enter the number of the option you\'d like to choose.
Type \033[32m\'help\'\033[0m if you need assistance.

[1] - Create set.
[2] - Choose set.
[3] - Delete set.
'''
]
choose_set_action_page = ['''Select next step by entering the number:
[1] - Create set.
[2] - Choose set.
[3] - Delete set.
''']
set_instatiation_page = [
    'Enter the name of the new set:',
    'Give your set a description.'
]
set_selection_page = [
    'Select set by it\'s name (case sensitive).To go back type \'\033[32mback\033[0m\'\nAvailable sets:' 
]
set_options_page = ['''Select option:
[1] - Play set
[2] - Add flashcard
[3] - Edit flashcards
[4] - Import flashcards
[5] - View statistics                     
'''
]
add_flashcard_page = [
    'Write a question that should appear on the card:',
    'Write the exact answer that needs to be given.'
]
help_page = ['''
This is the \033[32mhelp\033[0m page. It lists commands that are
available from any level of the system. Entering
one of these commands will execute it immediately.
'''
]
back_home_page = ['']
set_deletion_page = ['Enter the name of the set to be deleted:',]
play_page = ['']
edit_flashcards_page = ['''
Below is a list of cards from the selected set.
To delete a card, type '\033[32mdelete\033[0m' followed by the card number. 
e.g. '\033[32mdelete 12\033[0m'
To go back type '\033[32mback\033[0m'
''']