import argparse
import os.path
from dataclasses import dataclass, field
from enum import Enum

TokenType = Enum('TokenType', ['KEYWORD', 'SYMBOL', 'IDENTIFIER',
                               'INT_CONST', 'STRING_CONST'])

Keyword = Enum('Keyword', ['CLASS', 'METHOD', 'FUNCTION', 'CONSTRUCTOR',
                           'INT', 'BOOLEAN', 'CHAR', 'VOID', 'CAR', 'STATIC',
                           'FIELD', 'LET', 'DO', 'IF', 'ELSE', 'WHILE',
                           'RETURN', 'TRUE', 'FALSE', 'NULL', 'THIS'])

State = Enum('State', ['IN_COMMENT_A', 'IN_COMMENT_B', 'IN_STRING_A', 'IN_STRING_B'])

@dataclass
class Token:
    _type: TokenType
    value: str

    def __post_init__(self):
        self.tokens = {
                TokenType.KEYWORD     : 'keyword',
                TokenType.SYMBOL      : 'symbol',
                TokenType.IDENTIFIER : 'identifier',
                TokenType.INT_CONST   : 'integer_constant',
                TokenType.STRING_CONST: 'string_constant'
                }
        self.xml_trans = {
                '<':'&lt;',
                '>':'&gt;',
                '&':'&amp;'
                }

    def display(self):
        val =  self.xml_trans.get(self.value, self.value)
        print("<{}> {} </{}>".format(self.tokens[self._type], val, self.tokens[self._type]))

@dataclass
class Tokenizer:
    
    jack_file: str
    tokens: list[Token] = field(default=None, init=False)

    def __post_init__(self):
        self.cursor = 0
        self.tokens = []

        self.symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', 
                       '*', '/', '&', '|', '<', '>', '=', '~']

        self.keywords = ['class', 'constructor', 'function', 'method',
                    'field', 'static', 'var', 'int', 'char', 'boolean',
                    'void', 'true', 'false', 'null', 'this', 'let', 'do',
                    'if', 'else', 'while', 'return']

        with open(self.jack_file, "r") as f:
            self.jack_code = f.read()
        print(self.jack_code)

    def has_more_tokens(self):
        return self.cursor < len(self.jack_code)

    def get_next_token(self):
        if not self.has_more_tokens():
            return None

        cur_char  = self.jack_code[self.cursor]

        # integer constant
        if cur_char.isnumeric():  
            number = ''
            while self.has_more_tokens() and self.jack_code[self.cursor].isnumeric():
                number += self.jack_code[self.cursor]
                self.cursor += 1
            return Token(TokenType.INT_CONST, number)

        # in-line comments
        elif cur_char == '/' and self.jack_code[self.cursor + 1] == '/':
            while self.jack_code[self.cursor] != '\n':
                self.cursor += 1
            self.cursor += 1

        # multi-line comments
        elif cur_char == '/' and self.jack_code[self.cursor + 1] == '*':
            while not (self.jack_code[self.cursor] == '*' and self.jack_code[self.cursor + 1] == '/'):
                self.cursor += 1
            self.cursor += 2

        # symbol
        elif self.jack_code[self.cursor] in self.symbols:
            self.cursor += 1
            return Token(TokenType.SYMBOL, cur_char)

        # string constant, double quotes
        elif self.jack_code[self.cursor] == '"':
            s = ''
            self.cursor += 1
            while self.has_more_tokens() and self.jack_code[self.cursor] != '"':
                s += self.jack_code[self.cursor]
                self.cursor += 1
            self.cursor += 1
            return Token(TokenType.STRING_CONST, s)
        
        # string constant, single quotes
        elif self.jack_code[self.cursor] == "'":
            s = ''
            self.cursor += 1
            while self.has_more_tokens() and self.jack_code[self.cursor] != "'":
                s += self.jack_code[self.cursor]
                self.cursor += 1
            self.cursor += 1
            return Token(TokenType.STRING_CONST, s)
        
        # identifiers and keywords
        elif self.jack_code[self.cursor] not in [' ', '\n', '\t']:
            s = ''
            while self.has_more_tokens() and self.jack_code[self.cursor] not in [' ', '\n', '\t'] and self.jack_code[self.cursor] not in self.symbols:
                s += self.jack_code[self.cursor]
                self.cursor += 1
            if s in self.keywords:
                return Token(TokenType.KEYWORD, s)
            else:
                return Token(TokenType.IDENTIFIER, s)
        else:
            self.cursor += 1
    
    def tokenize(self):
        while self.has_more_tokens():
            if (token := self.get_next_token()):
                self.tokens.append(token)

    def dump_tokens(self):
        for token in self.tokens:
            token.display()


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


def create_output_filename(jack_file):
    return ''.join([os.path.splitext(jack_file)[0], '.xml'])


def main():

    # get path from command line arg
    path = get_path()

    # get list of .jack files to analyze
    jack_files = get_jack_files(path)

    # loop through jack files and process 
    for jack_file in jack_files:

        # test print input/output file paths
        print("{} -> {}".format(jack_file, create_output_filename(jack_file)))

        # instantiate Tokenizer
        tokenizer = Tokenizer(jack_file)

        '''
        while tokenizer.has_more_tokens():
            if (token := tokenizer.get_next_token()):
                token.display()
        '''
        # tokenize
        tokenizer.tokenize()

        # dump
        tokenizer.dump_tokens()

        # generate output file path
        # output_file = generate_output_filename(jack_file)

        # 
        # compilation_engine = CompilationEngine(tokenizer, output_file)

if __name__ == '__main__':

    main()
