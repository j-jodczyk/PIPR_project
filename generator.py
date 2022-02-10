from operations import (
    create_synonym,
    expand_with_adj,
    change_to_rhyme,
    make_rhyme
)
from errors import SynonymError, RhymeNotFoudError


def main():
    keep_going = True
    while keep_going:
        original_sentence = input('''
        Welcome to paraphraze generator!
        Enter your sentence:
        ''')
        invalid_input = True
        while invalid_input:
            try:
                chosen_action = int(input('''
                Choose what you want to do with the sentence:
                (enter corresponding number)
                1. Replace random word with synonym
                2. Expand sentence with adjectives
                3. Change last word, but keep the rhyme
                4. Enter another sentence and make little poem of of them.
                '''))
                if chosen_action in range(1, 5):
                    invalid_input = False
                else:
                    print('You must choose number between 1-4')
            except ValueError:
                print('You must choose integer number!')
        if chosen_action in [1, 2, 3]:
            print("Paraphrazed sentence:")
        if chosen_action == 1:
            try:
                print(create_synonym(original_sentence))
            except SynonymError as s:
                print(s)
        if chosen_action == 2:
            print(expand_with_adj(original_sentence))
        if chosen_action == 3:
            try:
                print(change_to_rhyme(original_sentence))
            except RhymeNotFoudError as r:
                print(r)
        if chosen_action == 4:
            second_sentence = input(
                '''
                Enter your second sentence:
                '''
            )
            try:
                print("Your little poem:")
                print(make_rhyme(original_sentence, second_sentence))
            except RhymeNotFoudError as r:
                print(r)
        check_keep_going = input('''
        Do you want to continue generating paraphrazes? [Y/n]
        ''')
        while check_keep_going not in ['Y', 'n']:
            check_keep_going = input('Incorrect input, try again')
        if check_keep_going == 'Y':
            continue
        if check_keep_going == 'n':
            keep_going = False


if __name__ == "__main__":
    main()
