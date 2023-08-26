import argparse
import os.path
from dataclasses import dataclass, field
from enum import Enum
import typing
import re


TokenType = Enum('TokenType', ['KEYWORD', 'SYMBOL', 'IDENTIFIER',
                               'INT_CONST', 'STRING_CONST'])

'''
TODO: Move each class to its own file
'''

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
            self.tokens.get(self._type, "unknown token"), 
            val, 
            self.tokens.get(self._type, "unknown token")))

    def terminal(self):
        val =  self.xml_special_chars.get(self.value, self.value)
        return "<{}> {} </{}>".format(
            self.tokens.get(self._type, "unknown token"), 
            val,
            self.tokens.get(self._type, "unknown token"))


@dataclass
class Tokenizer:
    
    jack_file       : str
    tokens          : list[Token] = field(default_factory=list, init=False) #TODO: delete
    cursor          : int = field(default=0, init=False)
    lexical_elements: typing.ClassVar[list[list[typing.Pattern, TokenType]]] = [

            # numbers
            [re.compile(r"^\d+"), TokenType.INT_CONST],

            # strings
            [re.compile(r"^\"[^\"]*\""), TokenType.STRING_CONST],
            [re.compile(r"^'[^']*.'"), TokenType.STRING_CONST],

            # comments
            [re.compile(r"^//.*"), None],
            [re.compile(r"^\/\*.*?\*\/", flags=re.DOTALL), None],

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

    def get_next_token(self, advance_cursor=True):
        '''
        TODO: Fix this hacky approach to peeking
        '''

        if not self.has_more_tokens():
            return None

        cur_str = self.jack_code[self.cursor:]

        for regexp, token_type in self.lexical_elements:

            token = self.match_token(regexp, cur_str, advance_cursor)

            # no match for this regex pattern
            if not token:
                continue

            # skip comments and whitespace
            if not token_type:
                return self.get_next_token(advance_cursor)

            if not advance_cursor: self.cursor -= len(token) #TODO <- hackiness


            return Token(token_type, token)

        raise SyntaxError("Unexpected Token at position {} beginning with {}".format(self.cursor, cur_str[:10]))

    def match_token(self,regexp, s, advance_cursor):
        if not (token := regexp.match(s)):
            return None
        self.cursor += len(token[0])
        return token[0]

    def tokenize(self):
        # TODO: delete
        while self.has_more_tokens():
            if (token := self.get_next_token()):
                self.tokens.append(token)
        return self.tokens

    def dump_tokens(self):
        # TODO: delete
        print("TOKEN DUMP")
        for token in self.tokens:
            token.display()

@dataclass
class Parser:

    input_filename : str
    tokenizer      : Tokenizer = field(init=False)
    output_filename: str = field(init=False)
    lookahead      : Token = field(init=False)

    def __post_init__(self):
        self.tokenizer = Tokenizer(self.input_filename)
        self.output_filename = self.create_output_filename(self.input_filename)
        self.lookahead = self.tokenizer.get_next_token()
        #self.tokenizer.tokenize()
        #self.tokenizer.dump_tokens()

    def create_output_filename(self, jack_file):
        return ''.join([os.path.splitext(jack_file)[0], '.xml'])

    def advance_token(self):
        self.lookahead = self.tokenizer.get_next_token()

    def peek(self):
        '''
        TODO: Fix hackiness here
        '''
        return self.tokenizer.get_next_token(advance_cursor=False)

    def eat(self, token_type=None, token_value=None):
        '''
        TODO: consider having this return 1 if successful or 0 if not. Then I could do something like:
        if not (self.eat(token_value='static') or self.eat(token_value='field'):
            raise SyntaxError
        '''
        if not self.lookahead:
            raise SyntaxError("Unexpected end of input, expected {}".format(token_type))

        if not (token_type or token_value):
            raise SyntaxError("Must provide type or value")
        if token_type and self.lookahead._type != token_type:
            raise SyntaxError("Unexpected token type: {}, expected {}"
                              .format(self.lookahead._type, token_type))
        if token_value and self.lookahead.value != token_value:
            raise SyntaxError("Unexpected token value: {}, expected {}"
                              .format(self.lookahead.value, token_value))

        token = self.lookahead

        self.advance_token()

        print(token.terminal()) # TODO better printing function here which takes indentaion into account

    def parse(self):
        self.compile_class()

    def compile_class(self):

        print("<class>")
        self.eat(token_value='class')
        self.eat(token_type=TokenType.IDENTIFIER)
        self.eat(token_value='{')
        while self.lookahead.value in ['static', 'field']:
            self.compile_class_var()
        while self.lookahead.value in ['constructor', 'function', 'method']:
            self.compile_subroutine()
        self.eat(token_value='}')
        print("</class>")

    def compile_class_var(self):
        print("<classVarDec>")
        self.eat(token_type=TokenType.KEYWORD) #already ensured that token.value is static or field
        self.compile_type()
        self.eat(token_type=TokenType.IDENTIFIER)
        while self.lookahead.value == ',':
            self.eat(token_value=',')
            self.eat(token_type=TokenType.IDENTIFIER)
        self.eat(token_value=';')
        print("</classVarDec>")

    def compile_subroutine(self):
        print("<subroutine>")
        self.eat(token_type=TokenType.KEYWORD) # already ensured token.value is constructor, function, or method
        if self.lookahead.value == 'void':
            self.eat(token_value='void')
        else:
            self.compile_type()
        self.eat(token_type=TokenType.IDENTIFIER)
        self.eat(token_value='(')
        if self.lookahead.value != ')':
            self.compile_parameter_list()
        self.eat(token_value=')')
        self.compile_subroutine_body()
        print("</subroutine>")

    def compile_parameter_list(self):
        print("<parameterList>")
        self.compile_type()
        self.eat(token_type=TokenType.IDENTIFIER)
        while self.lookahead.value == ',':
            self.eat(token_value=',')
            self.compile_type()
            self.eat(token_type=TokenType.IDENTIFIER)
        print("</parameterList>")

    def compile_subroutine_body(self):
        print("<subroutineBody>")
        self.eat(token_value='{')
        while self.lookahead.value == 'var':
            self.compile_var()
        self.compile_statements()
        self.eat(token_value='}')
        print("</subroutineBody>")

    def compile_type(self):
        if self.lookahead._type == TokenType.IDENTIFIER:
            self.eat(token_type = TokenType.IDENTIFIER)
        else:
            match self.lookahead.value:
                case 'int':
                    self.eat(token_value = 'int')
                case 'char':
                    self.eat(token_value = 'char')
                case 'boolean':
                    self.eat(token_value = 'boolean')
                case _:
                    raise SyntaxError("Unexpected var type")
        
    def compile_var(self):

        print("<varDec>")
        self.eat(token_value='var')
        self.compile_type()
        self.eat(token_type=TokenType.IDENTIFIER)
        while self.lookahead.value == ',':
            self.eat(token_value=',')
            self.eat(token_type=TokenType.IDENTIFIER)
        self.eat(token_value=';')
        print("</varDec>")
        
    def compile_statements(self):
        while self.lookahead.value in ['let', 'if', 'while', 'do', 'return']:
            self.compile_statement()

    def compile_statement(self):
        match self.lookahead.value:
            case 'let':
                self.compile_let()
            case 'if':
                self.compile_if()
            case 'while':
                self.compile_while()
            case 'do':
                self.compile_do()
            case 'return':
                self.compile_return()

    def compile_let(self):
        print("<letStatement>")
        self.eat(token_value='let')
        self.eat(token_type=TokenType.IDENTIFIER) # var_name
        if self.lookahead.value == '[':
            self.eat(token_value='[')
            self.compile_expression()
            self.eat(token_value=']')
        self.eat(token_value='=')
        self.compile_expression()
        self.eat(token_value=';')
        print("</letStatement>")

    def compile_if(self):
        print("<ifStatement>")
        self.eat(token_value='if')
        self.eat(token_value='(')
        self.compile_expression()
        self.eat(token_value=')')
        self.eat(token_value='{')
        self.compile_statements()
        self.eat(token_value='}')
        if self.lookahead.value == 'else':
            self.eat(token_value='else')
            self.eat(token_value='{')
            self.compile_statements()
            self.eat(token_value='}')
        print("</ifStatement>")

    def compile_while(self):
        print("<whileStatement>")
        self.eat(token_value='while')
        self.eat(token_value='(')
        self.compile_expression()
        self.eat(token_value=')')
        self.eat(token_value='{')
        self.compile_statements()
        self.eat(token_value='}')
        print("</whileStatement>")

    def compile_do(self):
        print("<doStatement>")
        self.eat(token_value='do')
        self.compile_subroutine_call()
        self.eat(token_value=';')
        print("</doStatement>")

    def compile_return(self):
        print("<returnStatement>")
        self.eat(token_value='return')
        if self.lookahead.value != ';':
            self.compile_expression()
        self.eat(token_value=';')
        print("</returnStatement>")

    def compile_expression(self):
        print("<expression>")
        self.compile_term()
        while self.lookahead.value in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.eat(token_value=self.lookahead.value) # TODO this is hacky, fix
            self.compile_term()
        print("</expression>")

    def compile_term(self):
        print("<term>")

        # integer constant
        if self.lookahead._type == TokenType.INT_CONST:
            self.eat(token_type=TokenType.INT_CONST)

        # string constant
        elif self.lookahead._type == TokenType.STRING_CONST:
            self.eat(token_type=TokenType.STRING_CONST)

        # keyword constant
        elif self.lookahead.value in ['true', 'false', 'null', 'this']:
            self.eat(token_value=self.lookahead.value) # TODO: hacky like in compile_expression

        # unaryop term
        elif self.lookahead.value in ['-', '~']:
            self.eat(token_value=self.lookahead.value) # TODO: hacky like in compile_expression
            self.compile_term()

        # ( expression )
        elif self.lookahead.value == '(':
            self.eat(token_value='(')
            self.compile_expression()
            self.eat(token_value=')')

        elif self.lookahead._type == TokenType.IDENTIFIER:

        # [ expression ]
            if self.peek().value == '[':
                self.eat(token_type=TokenType.IDENTIFIER)
                self.eat(token_value='[')
                self.compile_expression()
                self.eat(token_value=']')
        # subroutine call
            elif self.peek().value in ['(', '.']:
                self.compile_subroutine_call()

        # var_name
            else:
                self.eat(token_type=TokenType.IDENTIFIER)
        else:
            raise SyntaxError("Unexpected input")
        print("</term>")

    def compile_subroutine_call(self):
        print("<subroutine_call>")
        self.eat(token_type=TokenType.IDENTIFIER) # eat subroutine_name or class_name or var_name
        if self.lookahead.value == '(':
            self.eat(token_value='(')
            if self.lookahead.value != ')':
                self.compile_expression_list()
            self.eat(token_value=')')
        elif self.lookahead.value == '.':
            self.eat(token_value='.')
            self.eat(token_type=TokenType.IDENTIFIER)
            # TODO: following three lines are redundant with above, consider moving out of if/else
            self.eat(token_value='(')
            if self.lookahead.value != ')':
                self.compile_expression_list()
            self.eat(token_value=')')
        else:
            raise SyntaxError("Expected `(` or `.`, got {}".format(self.lookahead.value))
        print("</subroutine_call>")

    def compile_expression_list(self):
        print("<expression_list>")
        self.compile_expression()
        while self.lookahead.value == ',':
            self.eat(token_value=',')
            self.compile_expression()
        print("</expression_list>")


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

        # dump to screen
        # parser.dump()

        # write to file
        # parser.write()

if __name__ == '__main__':

    main()
