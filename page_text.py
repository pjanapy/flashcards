from global_variables import color

root_page = [f'''Welcome to the {color['ACCENT']}Flashcards{color['RESET']}!
Enter the {color['NUMBER']}number{color['RESET']} of the option you\'d like to choose.
Type {color['ACCENT']}\'help\'{color['RESET']} if you need assistance.

[{color['NUMBER']}1{color['RESET']}] - Select set.
[{color['NUMBER']}2{color['RESET']}] - Create set.
[{color['NUMBER']}3{color['RESET']}] - Delete set.
'''
]
choose_set_action_page = [f'''Enter the number of the option you\'d like to choose.
[{color['NUMBER']}1{color['RESET']}] - Select set.
[{color['NUMBER']}2{color['RESET']}] - Create set.
[{color['NUMBER']}3{color['RESET']}] - Delete set.
''']
set_instatiation_page = [
    'Enter the name of the new set:',
    'Give your set a description.'
]
set_selection_page = [
    f'Select set by it\'s {color['NUMBER']}number{color['RESET']}. Available sets:' 
]
set_options_page = [f'''Select option:
[{color['NUMBER']}1{color['RESET']}] - Play set
[{color['NUMBER']}2{color['RESET']}] - Add flashcard
[{color['NUMBER']}3{color['RESET']}] - Edit flashcards
[{color['NUMBER']}4{color['RESET']}] - Import flashcards
[{color['NUMBER']}5{color['RESET']}] - View statistics                     
'''
]
add_flashcard_page = [
    'Write a question that should appear on the card:',
    'Write the exact answer that needs to be given.'
]
help_page = [f'''
This is the {color['ACCENT']}help{color['RESET']} page. It lists commands that are
available from any level of the system. Entering
one of these commands will execute it immediately.
'''
]
back_home_page = ['']
set_deletion_page = ['Enter the name of the set to be deleted:',]
play_page = ['']
edit_flashcards_page = [f'''Below is a list of cards from the selected set.
To delete a card, type "{color['ACCENT']}del{color['RESET']}" followed by the flashcard {color['NUMBER']}number{color['RESET']}. 
e.g. {color['ACCENT']}del 12{color['RESET']}
''']
view_statistics_page = ['']
import_flashcards_page = [f'''Flashcards can be imported from a .csv file (without headers). 
The first column should contain questions, and the second column should contain answers.
The .csv file should be placed in the "imports/" directory. 
If the file appears in the list below, type in its name to proceed with the import.
Only questions that are not already in the currently selected flashcard set will be imported.
'''
]