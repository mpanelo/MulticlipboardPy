#!/usr/bin/python3

# mcb.pyw - Saves and loads pieces of text to the clipboard.
# Usage: ./mcb.pyw --save <keyword> - Saves clipboard to keyword.
#        ./mcb.pyw --load <keyword> - Loads keyword to clipboard.
#        ./mcb.pyw --list - Loads all keywords to clipboard.
#        ./mcb.pyw --deleteAll - Deletes all keys in the shelf.
#        ./mcb.pyw --delete <keyword> - Deletes specified keyword.

import sys, shelve, pyperclip, argparse


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
