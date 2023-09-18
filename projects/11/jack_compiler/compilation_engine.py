from .tokenizer import Tokenizer, Token
import os.path
import typing
from .enums import TokenType, SymbolScope, SymbolKind, Segment, Command
from .symboltable import SymbolTable
from .vmwriter import VMWriter

# TODO: Add indentation support
@dataclass
class CompilationEngine:

    input_filename : str
    tokenizer      : Tokenizer = field(init=False)
    lookahead      : Token = field(init=False)
    symbols        : SymbolTable = field(init=False)
    vmwriter       : VMWriter = field(init=False)
    cur_class      : str = field(init=False) # Hacky - to keep track of current class TODO
    op_lookup      : dict[str, str] = field(init=False)
    unaryop_lookup : dict[str, str] = field(init=False)

    # TODO: delete - relocated to VMWriter
    #output_filename: str = field(init=False)
    #write_file     : typing.IO = field(init=False)
    
    def __post_init__(self):
        self.tokenizer = Tokenizer(self.input_filename)
        self.advance_token()
        self.symbols = SymbolTable()
        self.vmwriter = VMWriter(self.input_filename)

        self.op_lookup = {
                '+': 'add',
                '-': 'sub',
                '*': 'call Math.multiply 2', # TODO: correct?
                '/': 'call Math.divide 2',
                '&': 'and',
                '|': 'or',
                '<': 'lt',
                '>': 'gt',
                '=': 'eq'
                }

        self.unaryop_lookup = {
                '-': 'neg',
                '~': 'not'
                }

        # TODO: delete - relocated to VMWriter
        #self.output_filename = self.create_output_filename(self.input_filename)
        #self.write_file = open(self.output_filename, "w")

    '''
    # TODO: delete - Moved to VMWriter
    def create_output_filename(self, jack_file):
        return ''.join([os.path.splitext(jack_file)[0], '.z', '.xml'])
    '''

    def advance_token(self):
        self.lookahead = self.tokenizer.get_next_token()

    def add_symbol(self, symbol: dict[str, str]):
        self.symbols.define(symbol['name'], symbol['type'], symbol['kind'])

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

        # TODO: vmwriter write line -- is this where it goes?
        self.write_line(token.display_token()) # TODO: remove write_line()

        return token.value # return the value of the token just consumed

   
    # TODO: Remove once finished, along with all calls to write_line
    def write_line(self, line):
        '''
        self.write_file.write(line)
        self.write_file.write('\n')
        '''
        print(line)
   

    def parse(self):
        self.compile_class()
        #self.close() # close write file
        self.vmwriter.close()

    def compile_class(self):
        self.write_line("<class>")
        self.eat(token_value='class')

        self.cur_class = self.eat(token_type=TokenType.IDENTIFIER) # set cur_class for use in compiling functions

        self.eat(token_value='{')
        while self.lookahead.value in ['static', 'field']:
            self.compile_class_var()
        while self.lookahead.value in ['constructor', 'function', 'method']:
            self.compile_subroutine()
        self.eat(token_value='}')
        self.write_line("</class>")

    def compile_class_var(self):
        self.write_line("<classVarDec>")

        cur_symbol = {}

        cur_symbol['kind'] = self.eat(token_type=TokenType.KEYWORD) # 'static' | 'field'
        cur_symbol['type'] = self.compile_type() # 'int' | 'char' | 'boolean' | class_name
        cur_symbol['name'] = self.eat(token_type=TokenType.IDENTIFIER) # TODO: consider reinstating compile_var_name()

        # add symbol to symbols table
        self.add_symbol(cur_symbol)

        # add additional symbols to symbols table
        while self.lookahead.value == ',':
            self.eat(token_value=',')
            cur_symbol['name'] = self.eat(token_type=TokenType.IDENTIFIER)
            self.add_symbol(cur_symbol)

        self.eat(token_value=';')
        self.write_line("</classVarDec>")

    def compile_subroutine(self):
        self.write_line("<subroutineDec>")


        subroutine_kind = self.eat(token_type=TokenType.KEYWORD) # constructor | function | method

        if self.lookahead.value == 'void':
            self.eat(token_value='void')
        else:
            self.compile_type()
        f_name = self.eat(token_type=TokenType.IDENTIFIER) # function name
        self.symbols.start_subroutine(f_name) # init subroutine symbols
        if subroutine_kind == 'method':
            self.add_symbol({'name':'this', 'type':f_name, 'kind':'arg'})
        self.eat(token_value='(')

        self.compile_parameter_list() # consider not having this return num params
        self.eat(token_value=')')

        self.compile_subroutine_body()

        self.vmwriter.write_function('.'.join([self.cur_class, f_name]), self.symbols.var_count('var')) # function <class>.<func_name> <>

        self.write_line("</subroutineDec>")

    def compile_parameter_list(self):
        self.write_line("<parameterList>")
        #n_params = 0

        cur_symbol = {}

        if self.lookahead.value != ')':
            cur_symbol['kind'] = 'arg'
            cur_symbol['type'] = self.compile_type() # 'int' | 'char' | 'boolean' | class name
            cur_symbol['name'] = self.eat(token_type=TokenType.IDENTIFIER)

            # add param to symbols table
            self.add_symbol(cur_symbol)
            #n_params += 1

            # add additional params to symbols table
            while self.lookahead.value == ',':
                self.eat(token_value=',')
                cur_symbol['type'] = self.compile_type()
                cur_symbol['name'] = self.eat(token_type=TokenType.IDENTIFIER)
                self.add_symbol(cur_symbol)
                #n_params += 1

        self.write_line("</parameterList>")
        return

    def compile_subroutine_body(self):
        self.write_line("<subroutineBody>")
        self.eat(token_value='{')
        while self.lookahead.value == 'var':
            self.compile_var()
        self.compile_statements()

        # query symbol table for var_count for 'var'
        # emit vm: function <class.func_name> <n_vars from above>

        self.eat(token_value='}')
        self.write_line("</subroutineBody>")

    def compile_type(self):
        if self.lookahead._type == TokenType.IDENTIFIER:
            return self.eat(token_type=TokenType.IDENTIFIER)
        else:
            match self.lookahead.value:
                case 'int':
                    return self.eat(token_value='int')
                case 'char':
                    return self.eat(token_value='char')
                case 'boolean':
                    return self.eat(token_value='boolean')
                case _:
                    raise SyntaxError("Unexpected var type")
        
    def compile_var(self):
        self.write_line("<varDec>")

        cur_symbol = {}
        cur_symbol['kind'] = self.eat(token_value='var')
        cur_symbol['type'] = self.compile_type()
        cur_symbol['name'] = self.eat(token_type=TokenType.IDENTIFIER)

        # add var to symbols table
        self.add_symbol(cur_symbol)

        # add additional vars to symbols table
        while self.lookahead.value == ',':
            self.eat(token_value=',')
            cur_symbol['name'] = self.eat(token_type=TokenType.IDENTIFIER)
            self.add_symbol(cur_symbol)

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

        var_name = self.eat(token_type=TokenType.IDENTIFIER)

        # deal with arrays
        if self.lookahead.value == '[':
            self.eat(token_value='[')
            self.compile_expression()
            self.eat(token_value=']')

        self.eat(token_value='=')
        self.compile_expression()
        self.eat(token_value=';')

        self.vmwriter.write_pop(self.symbols.kind_of(var_name), self.symbols.index_of(var_name))

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
        self.vmwriter.write_pop('temp', 0)
        self.write_line("</doStatement>")

    def compile_return(self):
        self.write_line("<returnStatement>")
        self.eat(token_value='return')
        if self.lookahead.value != ';':
            self.compile_expression()
        else:
            self.vmwriter.write_push('constant', 0)
        self.eat(token_value=';')
        self.write_line("</returnStatement>")

    def compile_expression(self):
        self.write_line("<expression>")

        self.compile_term()

        while self.lookahead.value in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            op = self.eat(token_value=self.lookahead.value) # TODO this is hacky, fix
            self.compile_term()
            self.vmwriter.write_arithmetic(self.op_lookup[op])

        self.write_line("</expression>")

    def compile_term(self):
        self.write_line("<term>")

        # integer constant
        if self.lookahead._type == TokenType.INT_CONST:
            num = self.eat(token_type=TokenType.INT_CONST)
            self.vmwriter.write_push('constant', num) # push constant n

        # string constant
        elif self.lookahead._type == TokenType.STRING_CONST:
            string = self.eat(token_type=TokenType.STRING_CONST)

            str_len = len(string)

            # push constant str_len
            self.vmwriter.write_push('constant', str_len)

            # call String.new 1
            self.vmwriter.write_function('String.new', 1) # check syntax
            # top of stack is pointer to the string

            for c in string:

                # TODO: USE fzf!!!

                # -----
                # STACK
                # -----
                # *(string)
                # character code
                # call String.appendChar 2

                self.vmwriter.write_push('constant', ord(c))
                self.vmwriter.write_function('String.appendChar', 2)


        # keyword constant
        elif self.lookahead.value in ['true', 'false', 'null', 'this']:
            keyword = self.eat(token_value=self.lookahead.value) # TODO: hacky like in compile_expression
            if keyword in ['null', 'false']:
                self.vmwriter.write_push('constant', 0)
            elif keyword == 'true':
                self.vmwriter.write_push('constant', 1)
                self.vmwriter.write_arithmetic('neg')
            else:
                # if you encounter `this`, you must be inside a class method, where `this` is arg 0
                self.vmwriter.write_push('arg', 0) # this

        # unaryop term
        elif self.lookahead.value in ['-', '~']:
            op = self.eat(token_value=self.lookahead.value) # TODO: hacky like in compile_expression
            self.compile_term()
            self.vmwrite_arithmetic(self.unaryop_lookup[op])

        # ( expression )
        elif self.lookahead.value == '(':
            self.eat(token_value='(')
            self.compile_expression()
            self.eat(token_value=')')

        # var_name | varname [ expression ] | subroutine call
        elif self.lookahead._type == TokenType.IDENTIFIER:

        # var_name [ expression ] -> array notation?
            if self.peek().value == '[':
                self.eat(token_type=TokenType.IDENTIFIER) # symboltable: either var, static, or field
                self.eat(token_value='[')
                self.compile_expression()
                self.eat(token_value=']')
        # subroutine call
            elif self.peek().value in ['(', '.']:
                self.compile_subroutine_call()

        # var_name
            else:
                var_name = self.eat(token_type=TokenType.IDENTIFIER) # symboltable: either var, static, or field
                self.vmwriter.write_push(self.symbols.kind_of(var_name), self.symbols.index_of(var_name)) # push <kind> <idx>

        else:
            raise SyntaxError("Unexpected input")
        self.write_line("</term>")

    def compile_var_name(self, kind):
        # TODO: delete
        self.eat(token_type=TokenType.IDENTIFIER)

    def compile_subroutine_name(self):
        # TODO: delete
        self.eat(token_type=TokenType.IDENTIFIER)

    def compile_class_name(self):
        # TODO: delete
        self.eat(token_type=TokenType.IDENTIFIER)

    def compile_subroutine_call(self):

        # DON'T PASS THIS
        # <className> '.' <subroutineName> '(' <expressionList> ')'
        # This is the class function case
        # e.g., Math.multiply(x, y)
        # call <subroutineName> <n_expressions>
        
        # PASS THIS
        # akin to self.my_method() in python -- internal invocation
        # <subroutineName> '(' <expressionList> ')'
        # this is an object's method called from within an object/class
        # my_func(arg1, arg2)
        # commision(this, arg1, arg2)
        # call <subroutineName> <n_args>
        # query subroutine_scope symbol table for count_of arguments

        # <varName> '.' <subroutineName> '(' <expressionList> ')'
        # this is a object's method -- external invocation
        # class_instance.class_method(this, arg1, arg2)
        # push arg 0 first for class instance
        # e.g., my_bank_account.get_info()
        # call <subroutineName> <n_expressions>

        # Function
        # push x 
        # push y 
        # call my_func 2

        # Method
        # push var_name where var_name is class instance
        # push x
        # push y
        # call my_func 3


        token = self.eat(token_type=TokenType.IDENTIFIER) # <subroutine_name> | <class_name> | <var_name>

        # if token in self.symbols[SymbolsScope.SUBROUTINE] : <- then it's a <varname>.<method>() format
        # in that case, get kind and index of <varname> from symbols table 

        # if it's not in the symbol table, it is a subroutine name or class name


        if self.lookahead.value == '(':
            pass
        elif self.lookahead.value == '.':
            self.eat(token_value='.')
            self.eat(token_type=TokenType.IDENTIFIER) # subroutine_name -- thus first identifier above was either class_name or var_name
        else:
            raise SyntaxError("Expected `(` or `.`, got {}".format(self.lookahead.value))

        self.eat(token_value='(')
        n_args = self.compile_expression_list() 
        self.eat(token_value=')')

        # let compile_parameter_list do the pushing of the requisite variables

        # self.vmwriter.write_call(call <func name> <n args>)
        # to figure out n_args, query symbol table for var_count of args

    def compile_expression_list(self):
        self.write_line("<expressionList>")
        n_expressions = 0 # replace this with symbol_table.get_count()
        if self.lookahead.value != ')':
            self.compile_expression()
            n_expressions += 1
            while self.lookahead.value == ',':
                self.eat(token_value=',')
                self.compile_expression()
                n_expressions += 1
        self.write_line("</expressionList>")
        return n_expressions

    '''
    # Relocated to VMWriter
    def close(self):
        self.write_file.close()
    '''
