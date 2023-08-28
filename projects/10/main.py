import argparse
import os.path
from jack_compiler import Parser

def get_path():

    parser = argparse.ArgumentParser(
            prog='JackAnalyzer',
            description='Analyzes .jack files')
    parser.add_argument('path',
                        help='path to .jack file or dir containing .jack files')
    args = parser.parse_args()
    path = args.path

    return path


def get_jack_files(path):
    
    jack_files = []

    if os.path.isdir(path):                 # get all jack files in directory
        for file in os.listdir(path):
            ext = os.path.splitext(file)[1]
            if ext == '.jack':
                jack_files.append(''.join([path, '/', file]))
    elif os.path.splitext(path)[1] == '.jack': # ensure that this is a jack file
        jack_files.append(path)
    else:
        pass

    return jack_files


def main():

    # get path from command line arg
    path = get_path()

    # get list of .jack files to analyze
    jack_files = get_jack_files(path)

    # loop through jack files and process 
    for jack_file in jack_files:

        parser = Parser(jack_file)

        parser.parse()


if __name__ == '__main__':

    main()
