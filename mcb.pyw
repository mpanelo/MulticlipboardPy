#!/usr/bin/python3

# mcb.pyw - Saves and loads pieces of text to the clipboard.
# Usage: py.exe mcb.pyw save <keyword> - Saves clipboard to keyword.
#        py.exe mcb.pyw <keyword> - Loads keyword to clipboard.
#        py.exe mcb.pyw list - Loads all keywords to clipboard.
#        py.exe mcb.pyw delete - Deletes all keys in the shelf.
#        py.exe mcb.pyw delete <keyword> - Deletes specified keyword.

import sys, shelve, pyperclip, argparse

"""
# Conditional statement for when the user enters a keyword or the command
# 'list'.
if len(sys.argv) == 2:

    shelfFile = shelve.open('mydata')

    # Create a string that contains all of the keywords in the shelfFile, and
    # copy it to the clipboard.
    if sys.argv[1].lower() == 'list':

        keys = list(shelfFile.keys())
        longListOfKeys = ""

        for key in keys:
            longListOfKeys += key + '\n'

        pyperclip.copy(longListOfKeys)
    
    # Delete all the keywords in the shelf.
    elif sys.argv[1].lower() == 'delete':

        for keyword in shelfFile:
            del shelfFile[keyword]

    # User did not enter the command 'list' or 'delete'.
    else:

        # If user entered a keyword that does not exists, then prompt the user.
        if sys.argv[1] not in shelfFile.keys():
            print('This keyword does not exist. If you need to see the list of'
                    + ' possible keywords, then type the command \'list\'.')

        # Otherwise, copy the contents that the keyword stores in the shelfFile
        # to the clipboard.
        else:
            pyperclip.copy(shelfFile[sys.argv[1]])

    shelfFile.close()

# Conditional statement for when the user wants to save a keyword into the
# shelf.
elif len(sys.argv) == 3 and sys.argv[1].lower() == 'save':

    shelfFile = shelve.open('mydata')

    # Ensure the user does not use 'save' or 'list' as keywords for the shelf.
    if sys.argv[2] != 'save' and sys.argv[2] != 'list':

        if sys.argv[2] not in shelfFile.keys():
            shelfFile[sys.argv[2]] = pyperclip.paste()
        else:
            print('This key already exists.')

    else:
        print('This keyword cannot be used.')

    shelfFile.close()

# Conditional statement for when the user wants to delete a keyword from the
# shelf.
elif len(sys.argv) == 3 and sys.argv[1].lower() == 'delete':

    shelfFile = shelve.open('mydata')

    if sys.argv[2] in shelfFile.keys():
        del shelfFile[sys.argv[2]]
    else:
        print('This keyword does not exist.')

    shelfFile.close()

# When the user does not enter the command correctly.
else:
    print('''List of possible commands:
                ./mcb.pyw [save] [keyword]
                ./mcb.pyw [list]
                ./mcb.pyw [keyword]
          '''
"""

def getList():
    shelveFile = shelve.open('mydata')
    keys = list(shelveFile.keys())

    longListOfKeys = ""
    
    for key in keys:
        longListOfKeys += key + '\n'

    pyperclip.copy(longListOfKeys)
    shelveFile.close()


def deleteAllKeys():
    shelveFile = shelve.open('mydata')

    for key in shelveFile:
        del shelveFile[key]

    shelveFile.close()


def deleteKey(keyword):
    shelveFile = shelve.open('mydata')

    if keyword in shelveFile:
        del shelveFile[keyword]
    else:
        print('Cannot delete keyword that does not exist.')

    shelveFile.close()


def loadKey(keyword):
    shelveFile = shelve.open('mydata')

    if keyword not in shelveFile:
        print('This keyword does not exist in the shelve file. To view the' +
        ' current list of keywords please use the --list argument.')

    else:
        pyperclip.copy(shelveFile[keyword])

    shelveFile.close()


def saveKey(keyword):
    shelveFile = shelve.open('mydata')
    # List of words that cannot be used as keywords to avoid confusion.
    notKeywords = ['save', 'list', 'delete', 'load', 'special_key']

    if keyword not in notKeywords: 

        if keyword not in shelveFile.keys():
            shelveFile[keyword] = pyperclip.paste()
        else:
            print('This keyword already exists, and cannot be saved.')

    else:
        print('This word cannot be saved and used as keyword.') 
    
    shelveFile.close()


def main():

    descStr = """
    This program analyzes command line arguments to save and load pieces of
    text to the clipboard.
    """

    parser = argparse.ArgumentParser(description=descStr)
    group = parser.add_mutually_exclusive_group(required=True)

    # I decided to make the keyword argument optional, since --deleteAll and
    # --list do not require a keyword. If the user does not enter a keyword,
    # it gets set to a default value of 'special_key'.
    """
    parser.add_argument('keyword', nargs='?', default='special_key', 
                        help='Please use the keyword with one of the optional' +
                        ' arguments.')
    """

    group.add_argument('--delete', dest='delKey', help='Deletes the provided ' +
                        'argument from the shelve file.')

    group.add_argument('--deleteAll', dest='delAll', action='store_true',
                        help='Deletes all keywords saved in the shelve file. ' +
                        'Does not require positional argument.')

    group.add_argument('--load', dest='loadKey', help='Loads the value of ' +
                        'the provided argument to the clipboard.')

    group.add_argument('--save', dest='saveKey', help='Saves the contents of ' +
                        'clipboard to the shelve file using the provided ' +
                        'argument.')

    group.add_argument('--list', dest='getList', action='store_const',
                        const=getList, help='Saves all keywords to the ' +
                        'clipboard. Does not require positional argument.')

    args = parser.parse_args()

    if args.delKey:
        deleteKey(args.delKey)
    elif args.delAll:
        deleteAllKeys()
    elif args.getList:
        getList()
    elif args.saveKey:
        saveKey(args.saveKey)
    elif args.loadKey:
       loadKey(args.loadKey)
    else:
        print('Please use the help option: ./mcb.pyw -h, --help.')


if __name__ == '__main__':
    main()
