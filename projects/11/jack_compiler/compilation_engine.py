from .tokenizer import Tokenizer, Token
import os.path
import typing
from dataclasses import dataclass, field
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
    cur_class      : str = field(init=False) # TODO: Hacky - to keep track of current class
    op_lookup      : dict[str, str] = field(init=False)
    unaryop_lookup : dict[str, str] = field(init=False)
    label_num      : int = field(init=False)

    def __post_init__(self):
        self.tokenizer = Tokenizer(self.input_filename)
        self.advance_token()
        self.symbols = SymbolTable()
        self.vmwriter = VMWriter(self.input_filename)
        self.label_num = 0

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

    def advance_token(self):
        self.lookahead = self.tokenizer.get_next_token()

    def add_symbol(self, symbol: dict[str, str]):
        self.symbols.define(symbol['name'], symbol['type'], symbol['kind'])

    def get_label_num(self):
        tmp = self.label_num
        self.label_num += 1
        return str(tmp)

    def peek(self):
        '''
        TODO: Fix hackiness here
        '''
        return self.tokenizer.get_next_token(advance_cursor=False)

    def eat(self, token_type=None, token_value=None):

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

        # Write XML to stout for debugging
        self.write_line(token.display_token()) 

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

        # set cur_class for use in compiling functions
        self.cur_class = self.eat(token_type=TokenType.IDENTIFIER) 

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

        self.compile_parameter_list() 
        
        self.eat(token_value=')')

        
        # emit VM: function <class>.<func_name> <n_locals>
        # self.vmwriter.write_function('.'.join([self.cur_class, f_name]), self.symbols.var_count('var')) 

        # is this where I allocate memory for constructors?

        self.compile_subroutine_body(f_name, subroutine_kind)

        '''
        if subroutine_kind == 'constructor':
            # push pointer 0
            # return
        '''


        self.write_line("</subroutineDec>")




    def compile_parameter_list(self):
        self.write_line("<parameterList>")

        cur_symbol = {}

        if self.lookahead.value != ')':
            cur_symbol['kind'] = 'arg'
            cur_symbol['type'] = self.compile_type() # 'int' | 'char' | 'boolean' | class name
            cur_symbol['name'] = self.eat(token_type=TokenType.IDENTIFIER)

            # add param to symbols table
            self.add_symbol(cur_symbol)

            # add additional params to symbols table
            while self.lookahead.value == ',':
                self.eat(token_value=',')
                cur_symbol['type'] = self.compile_type()
                cur_symbol['name'] = self.eat(token_type=TokenType.IDENTIFIER)
                self.add_symbol(cur_symbol)

        self.write_line("</parameterList>")

        return

    def compile_subroutine_body(self, f_name, sub_kind):
        self.write_line("<subroutineBody>")
        self.eat(token_value='{')
        while self.lookahead.value == 'var':
            self.compile_var()

        # emit VM: function <class>.<func_name> <n_locals>: needs to happen here to have access to var count
        self.vmwriter.write_function('.'.join([self.cur_class, f_name]), self.symbols.var_count('var')) 

        # deal with memory allocation for constructors
        if sub_kind == 'constructor':
            # push constant <num fields>
            self.vmwriter.write_push('constant', self.symbols.var_count('field'))
            # call Memory.alloc 1 (arg is the number of fields to allocate space for)
            self.vmwriter.write_call('Memory.alloc', 1)
            # pop pointer 0
            self.vmwriter.write_pop('pointer', 0)



        elif sub_kind == 'method':
            self.vmwriter.write_push('arg', 0) # Seems not quite right... I think we want to look up `this` and push that
            self.vmwriter.write_pop('pointer', 0)

        
        self.compile_statements() # return statement gets compiled here

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
                self.vmwriter.write_comment('<let>')
                self.compile_let()
                self.vmwriter.write_comment('</let>')
            case 'if':
                self.vmwriter.write_comment('<if>')
                self.compile_if()
                self.vmwriter.write_comment('</if>')
            case 'while':
                self.vmwriter.write_comment('<while>')
                self.compile_while()
                self.vmwriter.write_comment('</while>')
            case 'do':
                self.vmwriter.write_comment('<do>')
                self.compile_do()
                self.vmwriter.write_comment('</do>')
            case 'return':
                self.vmwriter.write_comment('<return>')
                self.compile_return()
                self.vmwriter.write_comment('</return>')

    def compile_let(self):
        self.write_line("<letStatement>")
        self.eat(token_value='let')

        var_name = self.eat(token_type=TokenType.IDENTIFIER)

        # TODO: deal with arrays
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
        # get unique label IDs
        label_else = ''.join(['L', self.get_label_num()])
        label_endif = ''.join(['L', self.get_label_num()])

        self.write_line("<ifStatement>")
        self.eat(token_value='if')
        self.eat(token_value='(')
        self.compile_expression()
        self.eat(token_value=')')
        self.vmwriter.write_arithmetic('not')
        self.vmwriter.write_if(label_else)
        self.eat(token_value='{')
        self.compile_statements()
        self.eat(token_value='}')
        self.vmwriter.write_goto(label_endif)
        self.vmwriter.write_label(label_else)
        if self.lookahead.value == 'else':
            self.eat(token_value='else')
            self.eat(token_value='{')
            self.compile_statements()
            self.eat(token_value='}')
        self.vmwriter.write_label(label_endif)
        self.write_line("</ifStatement>")

    def compile_while(self):
        label_start = ''.join(['L', self.get_label_num()])
        label_end = ''.join(['L', self.get_label_num()])
        self.write_line("<whileStatement>")
        self.eat(token_value='while')
        self.eat(token_value='(')
        self.vmwriter.write_label(label_start)
        self.compile_expression()
        self.eat(token_value=')')
        self.vmwriter.write_arithmetic('not')
        self.vmwriter.write_if(label_end)
        self.eat(token_value='{')
        self.compile_statements()
        self.eat(token_value='}')
        self.vmwriter.write_goto(label_start)
        self.vmwriter.write_label(label_end)
        self.write_line("</whileStatement>")

    def compile_do(self):
        self.write_line("<doStatement>")
        self.eat(token_value='do')
        self.compile_subroutine_call()
        self.eat(token_value=';')
        self.vmwriter.write_pop('temp', 0)
        self.write_line("</doStatement>")

    def compile_return(self):
        '''
        we want to know what kind of subroutine we're returning from at this point, because
        if it's a constructor, we need to push pointer 0 prior to returning
        '''

        self.write_line("<returnStatement>")
        self.eat(token_value='return')
        if self.lookahead.value != ';':
            self.compile_expression()
        else:
            self.vmwriter.write_push('constant', 0)
        self.vmwriter.write_return()
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
                # if you encounter `this`
                self.vmwriter.write_push('pointer', 0)

        # unaryop term
        elif self.lookahead.value in ['-', '~']:
            op = self.eat(token_value=self.lookahead.value) # TODO: hacky like in compile_expression
            self.compile_term()
            self.vmwriter.write_arithmetic(self.unaryop_lookup[op])

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

        # <className> '.' <subroutineName> '(' <expressionList> ')'
        # This is the class function case
        # Math.multiply(x, y)
        # call <subroutineName> <n_args>
        # * Do not pass `this`
        
        # <subroutineName> '(' <expressionList> ')'
        # akin to self.my_method() in python -- internal invocation OR constructor function
        # my_func(this, arg1, arg2)
        # call <subroutineName> <n_args>
        # query subroutine_scope symbol table for count_of arguments
        # do moveUp()
        # if `this` is in symbol table, then it's an internal invocation of a cuntion: push the kind and idx of `this`
        # else we're in a constructor, so do something... 

        # <varName> '.' <subroutineName> '(' <expressionList> ')'
        # this is a object's method -- external invocation
        # class_instance.class_method(this, arg1, arg2)
        # call <subroutineName> <n_args>


        token = self.eat(token_type=TokenType.IDENTIFIER) # <subroutine_name> | <class_name> | <var_name>
        n_expressions = 0


        if self.lookahead.value == '(':
            # Scenario 1: <subroutine name>.(<expression list>)
            # This is either a method being called from within the class OR a constructor
            # `token` above is the name of the subroutine

            # Scenario 1A: Internal invocation of class method
            # In this case, `this` should be in the symbol table, so push kind and idx of this:
            # self.vmwriter.write_push(self.symbols.kind_of('this'), self.symbols.index_of('this'))

            # Scenario 1B: Constructor
            # In this case, `this` will not be in the symbol table, so push this?
            call_name = '.'.join([self.cur_class, token])

            if self.symbols.contains('this'):
                # Internal invocation of class method
                self.vmwriter.write_push(self.symbols.kind_of('this'), self.symbols.index_of('this'))
            else:
                # Constructor function: Since we're in a constructor function, we need to push the newly-allocated object
                # onto the stack for use as the first arg to this class method
                self.vmwriter.write_push('pointer', 0)

            n_expressions += 1
            pass
        elif self.lookahead.value == '.':
            # Scenario 2 or 3: `token` is either class_name or var name
            self.eat(token_value='.')
            if self.symbols.contains(token):
                # Scenario 2: <varName>.<subroutineName>(<expressionList>)
                # This is an external invocation of a method on object `token`
                call_name = '.'.join([self.symbols.type_of(token), self.eat(token_type=TokenType.IDENTIFIER)])
                self.vmwriter.write_push(self.symbols.kind_of(token), self.symbols.index_of(token))
                n_expressions += 1
            else:
                # Scenario 3: <className>.<subroutineName>(<expressionList>)
                # This is a function
                call_name = '.'.join([token, self.eat(token_type=TokenType.IDENTIFIER)]) # subroutine_name 

        else:
            raise SyntaxError("Expected `(` or `.`, got {}".format(self.lookahead.value))

        self.eat(token_value='(')
        n_expressions += self.compile_expression_list() 
        self.eat(token_value=')')

        self.vmwriter.write_call(call_name, n_expressions) # not working when it's a method and needs to default to one expression

    def compile_expression_list(self):
        n_expressions = 0
        self.write_line("<expressionList>")
        if self.lookahead.value != ')':
            self.compile_expression()
            n_expressions += 1
            while self.lookahead.value == ',':
                self.eat(token_value=',')
                self.compile_expression()
                n_expressions += 1
        self.write_line("</expressionList>")
        return n_expressions
