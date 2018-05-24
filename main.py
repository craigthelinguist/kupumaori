
from __future__ import print_function
from os import listdir, system
from os.path import isfile
import random
import readchar
from sys import exit
from time import sleep


# Control sequences for various keys.
KEY_RIGHT_ARROW = '\\x1b[C'
KEY_DOWN_ARROW = '\\x1b[B'
KEY_ESC = '\\x03'
KEY_ETX = '\\x1b\\x1b'


def clear():
    system('clear')



def read_key():
    """
    Read a single key input from the `readchar` library.

    :return: The string returned is the character pushed. The representation for this is the UNIX terminal control
        sequence which transmits the key press. This is a blocking function.
    """
    return repr(readchar.readkey()) \
            .lstrip("'") \
            .rstrip("'")


def load_word_list(fpath):
    """
    Load a wordlist from the given filepath.
    :param fpath: Location from which the wordlist should be loaded.
    :return: The wordlist, represented as a dictionary of words to their meaning.
    """
    if not isfile(fpath):
        return None
    word_list = {}
    with open(fpath, 'r') as f:
        for line in f:
            line = line.rstrip().lstrip()
            if line == '': continue
            line = line.split('\t')
            line = list(filter(lambda x: x != '', line))
            word_list[line[0]] = line[1]
    return word_list


def test_word_list(list_name, word_list):

    total_num_words = len(word_list)
    done = False

    while len(word_list) > 0 and not done:

        clear()
        print('\n Testing `{}` ({}/{} left)\n'.format(list_name, len(word_list), total_num_words))

        # Select a random pair and display the choice to the user.
        test_engl = bool(random.getrandbits(1))
        word = random.choice(list(word_list))
        definition = word_list[word]
        if test_engl:
            print('   Meaning: {}'.format(definition))
            print('   What is the word? (Push any key to see the answer)')
        else:
            print('   Word: {}'.format(word))
            print('   What is the meaning? (Push any key to see the answer)')
        print('\n   ', end='')

        if read_key() in [KEY_ESC, KEY_ETX]:
            done = True
            continue

        if test_engl:
            print('Word: {}'.format(word))
        else:
            print('Meaning: {}'.format(definition))
        print()

        # Remove from the `word_list` if the user says they got it right.
        print('   Did you get it right? If so, push `right arrow`, otherwise push `down arrow`.')
        print('\n   ', end='')
        while True:
            key = read_key()
            if key == KEY_RIGHT_ARROW:
                del(word_list[word])
                break
            elif key == KEY_DOWN_ARROW:
                break
            elif key in [KEY_ESC, KEY_ETX]:
                done = True
                # Below should really be a `continue "outer loop"`, but this can't be done in Python.
                # Since it is the last statement in the loop, "break" will do the same thing.
                break

    # Print a nice exit message if they went through the whole word_list.
    if len(word_list) == 0:
        print("\n   All done!")
        sleep(0.5)


def main():
    while True:

        clear()

        print('\n Kia ora. Word lists available are: ')
        for file in sorted(listdir('data')):
            print('   {}'.format(file.rstrip('.txt')))
        print('')

        fname = input(' Enter name of a word list (type "exit" when done): ')
        if fname.lower() in ['exit', 'quit', 'done']:
            print('')
            exit()
        fpath = 'data/{}.txt'.format(fname)
        if not isfile(fpath):
            print(' No file located at {}'.format(fpath))
            continue
        else:
            test_word_list(fname, load_word_list(fpath))
            clear()


if __name__ == '__main__':
    main()
