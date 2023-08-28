from dataclasses import dataclass, field
from .tokenizer import Tokenizer, Token
import os.path
import typing
from .enums import TokenType

# TODO: Add indentation support
@dataclass
class Parser:

    input_filename : str
    tokenizer      : Tokenizer = field(init=False)
    output_filename: str = field(init=False)
    lookahead      : Token = field(init=False)
    write_file     : typing.IO = field(init=False)

    def __post_init__(self):
        self.tokenizer = Tokenizer(self.input_filename)
        self.output_filename = self.create_output_filename(self.input_filename)
        self.lookahead = self.tokenizer.get_next_token()
        self.write_file = open(self.output_filename, "w")
        #self.tokenizer.tokenize()
        #self.tokenizer.dump_tokens()

    def create_output_filename(self, jack_file):
        return ''.join([os.path.splitext(jack_file)[0], '.z', '.xml'])

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

        self.write_line(token.display_token())

    def write_line(self, line):
        self.write_file.write(line)
        self.write_file.write('\n')

    def parse(self):
        self.compile_class()
        self.close() # close write file

    def compile_class(self):

        self.write_line("<class>")
        self.eat(token_value='class')
        self.eat(token_type=TokenType.IDENTIFIER)
        self.eat(token_value='{')
        while self.lookahead.value in ['static', 'field']:
            self.compile_class_var()
        while self.lookahead.value in ['constructor', 'function', 'method']:
            self.compile_subroutine()
        self.eat(token_value='}')
        self.write_line("</class>")

    def compile_class_var(self):
        self.write_line("<classVarDec>")
        self.eat(token_type=TokenType.KEYWORD) #already ensured that token.value is static or field
        self.compile_type()
        self.eat(token_type=TokenType.IDENTIFIER)
        while self.lookahead.value == ',':
            self.eat(token_value=',')
            self.eat(token_type=TokenType.IDENTIFIER)
        self.eat(token_value=';')
        self.write_line("</classVarDec>")

    def compile_subroutine(self):
        self.write_line("<subroutineDec>")
        self.eat(token_type=TokenType.KEYWORD) # already ensured token.value is constructor, function, or method
        if self.lookahead.value == 'void':
            self.eat(token_value='void')
        else:
            self.compile_type()
        self.eat(token_type=TokenType.IDENTIFIER)
        self.eat(token_value='(')
        '''
        if self.lookahead.value != ')':
            self.compile_parameter_list()
        '''
        self.compile_parameter_list()
        self.eat(token_value=')')
        self.compile_subroutine_body()
        self.write_line("</subroutineDec>")

    def compile_parameter_list(self):
        self.write_line("<parameterList>")
        if self.lookahead.value != ')':
            self.compile_type()
            self.eat(token_type=TokenType.IDENTIFIER)
            while self.lookahead.value == ',':
                self.eat(token_value=',')
                self.compile_type()
                self.eat(token_type=TokenType.IDENTIFIER)
        self.write_line("</parameterList>")

    def compile_subroutine_body(self):
        self.write_line("<subroutineBody>")
        self.eat(token_value='{')
        while self.lookahead.value == 'var':
            self.compile_var()
        self.compile_statements()
        self.eat(token_value='}')
        self.write_line("</subroutineBody>")

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

        self.write_line("<varDec>")
        self.eat(token_value='var')
        self.compile_type()
        self.eat(token_type=TokenType.IDENTIFIER)
        while self.lookahead.value == ',':
            self.eat(token_value=',')
            self.eat(token_type=TokenType.IDENTIFIER)
        self.eat(token_value=';')
        self.write_line("</varDec>")
        
    def compile_statements(self):
        self.write_line("<statements>")
        while self.lookahead.value in ['let', 'if', 'while', 'do', 'return']:
            self.compile_statement()
        self.write_line("</statements>")

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
        self.write_line("<letStatement>")
        self.eat(token_value='let')
        self.eat(token_type=TokenType.IDENTIFIER) # var_name
        if self.lookahead.value == '[':
            self.eat(token_value='[')
            self.compile_expression()
            self.eat(token_value=']')
        self.eat(token_value='=')
        self.compile_expression()
        self.eat(token_value=';')
        self.write_line("</letStatement>")

    def compile_if(self):
        self.write_line("<ifStatement>")
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
        self.write_line("</ifStatement>")

    def compile_while(self):
        self.write_line("<whileStatement>")
        self.eat(token_value='while')
        self.eat(token_value='(')
        self.compile_expression()
        self.eat(token_value=')')
        self.eat(token_value='{')
        self.compile_statements()
        self.eat(token_value='}')
        self.write_line("</whileStatement>")

    def compile_do(self):
        self.write_line("<doStatement>")
        self.eat(token_value='do')
        self.compile_subroutine_call()
        self.eat(token_value=';')
        self.write_line("</doStatement>")

    def compile_return(self):
        self.write_line("<returnStatement>")
        self.eat(token_value='return')
        if self.lookahead.value != ';':
            self.compile_expression()
        self.eat(token_value=';')
        self.write_line("</returnStatement>")

    def compile_expression(self):
        self.write_line("<expression>")
        self.compile_term()
        while self.lookahead.value in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.eat(token_value=self.lookahead.value) # TODO this is hacky, fix
            self.compile_term()
        self.write_line("</expression>")

    def compile_term(self):
        self.write_line("<term>")

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
        self.write_line("</term>")

    def compile_subroutine_call(self):
        self.eat(token_type=TokenType.IDENTIFIER) # eat subroutine_name or class_name or var_name
        if self.lookahead.value == '(':
            pass
        elif self.lookahead.value == '.':
            self.eat(token_value='.')
            self.eat(token_type=TokenType.IDENTIFIER)
        else:
            raise SyntaxError("Expected `(` or `.`, got {}".format(self.lookahead.value))

        self.eat(token_value='(')
        self.compile_expression_list() 
        self.eat(token_value=')')

    def compile_expression_list(self):
        self.write_line("<expressionList>")
        if self.lookahead.value != ')':
            self.compile_expression()
            while self.lookahead.value == ',':
                self.eat(token_value=',')
                self.compile_expression()
        self.write_line("</expressionList>")

    def close(self):
        self.write_file.close()
