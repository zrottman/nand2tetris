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
    xml_special_chars: typing.ClassVar[dict[str, str]] = {
        '<':'&lt;',
        '>':'&gt;',
        '&':'&amp;'
    }
    tokens           : typing.ClassVar[dict[TokenType, str]] = {
        TokenType.KEYWORD     : 'keyword',
        TokenType.SYMBOL      : 'symbol',
        TokenType.IDENTIFIER  : 'identifier',
        TokenType.INT_CONST   : 'integer_constant',
        TokenType.STRING_CONST: 'string_constant',
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
        return self.tokens

    def dump_tokens(self):
        print("TOKEN DUMP")
        for token in self.tokens:
            token.display()

@dataclass
class Parser:

    tokens         : list[Token]
    input_filename : str
    cursor         : int = field(default=0, init=False)
    output_filename: str = field(init=False)
    lookahead      : Token = field(init=False)

    def __post_init__(self):
        self.output_filename = self.create_output_filename(self.input_filename)
        self.lookahead = self.get_next_token()

    def create_output_filename(self, jack_file):
        return ''.join([os.path.splitext(jack_file)[0], '.xml'])

    def has_more_tokens(self):
        return self.cursor < len(self.tokens)

    def get_next_token(self):
        return self.tokens[self.cursor]

    def advance_token(self):
        self.cursor += 1
        self.lookahead = self.get_next_token()

    def program(self):
        return {
                'type': 'Program',
                'body': self.compile_class() 
                }

    def literal(self):
        match self.lookahead._type:
            case TokenType.INT_CONST:
                return self.number_literal()
            case TokenType.STRING_CONST:
                return self.string_literal()
        raise SyntaxError("Unexpected Literal")

    def number_literal(self):
        token = self.eat(TokenType.INT_CONST)
        return {
                'type': 'integer constant',
                'value': int(token.value)
                }

    def string_literal(self):
        token = self.eat(TokenType.STRING_CONST)
        return {
                'type': 'string constant',
                'value': token.value
                }
    
    def eat(self, token_type):

        if not self.lookahead:
            raise SyntaxError("Unexpected end of input, expected {}".format(token_type))

        if self.lookahead._type != token_type:
            raise SyntaxError("Unexpected token: {}, expected {}".format(token.value, token_type))

        self.advance_token()

        return token




    def parse(self):
        return self.compile_class()

    def compile_class(self):

        tokens = []

        if self.lookahead.value != 'class':
            raise SyntaxError("Unexpected token {}".format(self.lookahead.value))

        tokens.append(self.lookahead)
        self.advance_token()

        if self.lookahead._type != TokenType.IDENTIFIER:
            raise SyntaxError("Unexpected token {}".format(self.lookahead.value))

        tokens.append(self.lookahead)
        self.advance_token()

        if self.lookahead.value != "{":
            raise SyntaxError("Unexpected token {}".format(self.lookahead.value))

        while (class_var_dec := self.compile_class_var_dec()):
            pass


    def compile_subroutine(self):
        pass

    def compile_parameter_list(self):
        pass

    def compile_var_dec(self):

        pass

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass

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

        # instantiate Tokenizer
        tokenizer = Tokenizer(jack_file)

        # tokenize
        tokens = tokenizer.tokenize()

        # dump
        tokenizer.dump_tokens()

        # parse
        parser = Parser(tokens, jack_file)

        # dump to screen
        # parser.dump()

        # write to file
        # parser.write()

if __name__ == '__main__':

    main()
