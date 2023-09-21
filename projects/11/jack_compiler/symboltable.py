from dataclasses import dataclass, field
from .enums import TokenType, SymbolKind, SymbolScope
import pprint

@dataclass
class SymbolTable:

    symbols      : dict[SymbolScope, dict[str, dict[str, str, int]]] = field(init=False)
    '''
    Symbol Table Structure
    ----------------------
    symbols = {

        SymbolScope.CLASS: {
            my_var1: {
                'type': 'int' | 'char' | 'bool' | <class name>,
                'kind': 'static' | 'field'
                'idx' : <int> },
            my_var2: {
                'type': 'int' | 'char' | 'bool' | <class name>,
                'kind': 'static' | 'field' | 'arg' | 'var'
                'idx' : <int> }
                },

        SymbolScope.SUBROUTINE: {
            my_var1: {
                'type': 'int' | 'char' | 'bool' | <class name>,
                'kind': 'arg' | 'var'
                'idx' : <int> },
            my_var2: {
                'type': 'int' | 'char' | 'bool' | <class name>,
                'kind': 'arg' | 'var'
                'idx' : <int> }
                },

    }
    '''

    idx_lookup   : dict[SymbolKind, int]  = field(init=False)
    scope_lookup : dict[SymbolKind, SymbolScope] = field(init=False)
    #kind_lookup  : dict[str, SymbolKind] = field(init=False) # TODO: delete

    def __post_init__(self):
        self.symbols = {
                SymbolScope.CLASS      : {},
                SymbolScope.SUBROUTINE : {}
                }


        '''
        self.idx_lookup = {
                SymbolKind.STATIC : 0,
                SymbolKind.FIELD  : 0,
                SymbolKind.ARG    : 0,
                SymbolKind.VAR    : 0 
                }
        '''

        self.idx_lookup = {
                'static' : 0,
                'field'  : 0,
                'arg'    : 0,
                'var'    : 0 
                }
        
        '''
        self.scope_lookup = {
                SymbolKind.STATIC : SymbolScope.CLASS,
                SymbolKind.FIELD  : SymbolScope.CLASS,
                SymbolKind.ARG    : SymbolScope.SUBROUTINE,
                SymbolKind.VAR    : SymbolScope.SUBROUTINE 
                }
        '''
        self.scope_lookup = {
                'static' : SymbolScope.CLASS,
                'field'  : SymbolScope.CLASS,
                'arg'    : SymbolScope.SUBROUTINE,
                'var'    : SymbolScope.SUBROUTINE 
                }

        # TODO: delete; store kind as str not enum
        '''
        self.kind_lookup = {
                'static': SymbolKind.STATIC,
                'field' : SymbolKind.FIELD,
                'arg'   : SymbolKind.ARG,
                'var'   : SymbolKind.VAR
                }
        '''

    def define(self, name: str, symbol_type: str, symbol_kind: str):
        #symbol_kind = self.kind_lookup[symbol_kind]

        self.symbols[self.scope_lookup[symbol_kind]][name] = {
                'type': symbol_type,
                'kind': symbol_kind,
                'idx' : self.idx_lookup[symbol_kind]
                }

        self.idx_lookup[symbol_kind] += 1


        # Logging
        print("Adding to symbols table")
        pprint.PrettyPrinter(depth=4).pprint(self.symbols)
        print()

    def start_subroutine(self, f_name):
        '''
        self.idx_lookup[SymbolKind.ARG] = 0
        self.idx_lookup[SymbolKind.VAR] = 0
        '''
        self.idx_lookup['arg'] = 0
        self.idx_lookup['var'] = 0
        self.symbols[SymbolScope.SUBROUTINE] = {}

    def var_count(self, symbol_kind: str) -> int:
        return self.idx_lookup.get(symbol_kind, 0)

    def kind_of(self, name: str) -> str:
        if name in self.symbols[SymbolScope.SUBROUTINE]:
            return self.symbols[SymbolScope.SUBROUTINE][name]['kind']
        elif name in self.symbols[SymbolScope.CLASS]:
            return self.symbols[SymbolScope.CLASS][name]['kind']
        else:
            raise SyntaxError("Unknown symbol {}".format(name))

    def type_of(self, name: str) -> str:
        if name in self.symbols[SymbolScope.SUBROUTINE]:
            return self.symbols[SymbolScope.SUBROUTINE][name]['type']
        elif name in self.symbols[SymbolScope.CLASS]:
            return self.symbols[SymbolScope.CLASS][name]['type']
        else:
            raise SyntaxError("Unknown symbol {}".format(name))

    def index_of(self, name: str) -> int:
        if name in self.symbols[SymbolScope.SUBROUTINE]:
            return self.symbols[SymbolScope.SUBROUTINE][name]['idx']
        elif name in self.symbols[SymbolScope.CLASS]:
            return self.symbols[SymbolScope.CLASS][name]['idx']
        else:
            raise SyntaxError("Unknown symbol {}".format(name))

    def contains(self, name: str) -> bool:
        if name in self.symbols[SymbolScope.SUBROUTINE]:
            return True
        elif name in self.symbols[SymbolScope.CLASS]:
            return True
        else:
            return False
