import argparse
import os.path
from dataclasses import dataclass, field
from enum import Enum
import typing
import re

TokenType = Enum('TokenType', ['KEYWORD', 'SYMBOL', 'IDENTIFIER',
                               'INT_CONST', 'STRING_CONST'])

Keyword = Enum('Keyword', ['CLASS', 'METHOD', 'FUNCTION', 'CONSTRUCTOR',
                           'INT', 'BOOLEAN', 'CHAR', 'VOID', 'CAR', 'STATIC',
                           'FIELD', 'LET', 'DO', 'IF', 'ELSE', 'WHILE',
                           'RETURN', 'TRUE', 'FALSE', 'NULL', 'THIS'])


@dataclass
class Token:
    _type            : TokenType
    value            : str
    tokens           : typing.ClassVar[dict[TokenType, str]] = {
        TokenType.KEYWORD     : 'keyword',
        TokenType.SYMBOL      : 'symbol',
        TokenType.IDENTIFIER  : 'identifier',
        TokenType.INT_CONST   : 'integer_constant',
        TokenType.STRING_CONST: 'string_constant',
    }
    xml_special_chars: typing.ClassVar[dict[str, str]] = {
        '<':'&lt;',
        '>':'&gt;',
        '&':'&amp;'
    }

    def display(self):
        val =  self.xml_special_chars.get(self.value, self.value)
        print("<{}> {} </{}>".format(
            self.tokens.get(self._type, "default"), 
            val, 
            self.tokens.get(self._type, "default")))

@dataclass
class Tokenizer:
    
    jack_file       : str
    tokens          : list[Token] = field(default_factory=list, init=False)
    cursor          : int = field(default=0, init=False)
    lexical_elements: typing.ClassVar[list[list[typing.Pattern, TokenType]]] = [
            # numbers
            [re.compile(r"^\d+"), TokenType.INT_CONST],
            # strings
            [re.compile(r"^\"[^\"]*\""), TokenType.STRING_CONST],
            [re.compile(r"^'[^']*.'"), TokenType.STRING_CONST],
            # comments
            [re.compile(r"^//.*"), None],
            [re.compile(r"^/\*.*\*/", flags=re.DOTALL), None],
            # whitespace
            [re.compile(r"^[\s\n]+"), None],
            # keywords
            [re.compile(r"""^
                class | constructor | function | method |
                field | static | var | int | char | boolean |
                void | true | false | null | this | let | do |
                if | else | while | return
                """, re.X), TokenType.KEYWORD],
            # symbols
            [re.compile(r"^[\{\}\(\)\[\]\.\,\;\+\-\*\/\&\|\<\>\=\~]"), TokenType.SYMBOL],
            # identifiers
            [re.compile(r"^[a-zA-Z][a-zA-Z0-9\_]*"), TokenType.IDENTIFIER]]

    def __post_init__(self):
        with open(self.jack_file, "r") as f:
            self.jack_code = f.read()

    def has_more_tokens(self):
        return self.cursor < len(self.jack_code)

    def get_next_token(self):

        if not self.has_more_tokens():
            return None

        cur_str = self.jack_code[self.cursor:]

        for regexp, token_type in self.lexical_elements:

            token = self.match_token(regexp, cur_str)

            # no match for this regex pattern
            if not token:
                continue

            # skip comments and whitespace
            if not token_type:
                return self.get_next_token()

            return Token(token_type, token)

        raise SyntaxError("Unexpected Token at position {} beginning with {}".format(self.cursor, cur_str[:10]))

    def match_token(self,regexp, s):
        if not (token := regexp.match(s)):
            return None
        self.cursor += len(token[0])
        return token[0]

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
