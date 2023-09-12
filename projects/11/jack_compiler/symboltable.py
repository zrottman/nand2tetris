from dataclasses import dataclass, field
from .enums import TokenType, SymbolKind, SymbolScope
import pprint

@dataclass
class SymbolTable:

    symbols      : dict[SymbolScope, dict[str, dict[str, int]]] = field(init=False)
    '''
    Symbol Table Structure
    ----------------------
    symbols = {

        SymbolScope.CLASS: {
            my_var1: {
                'type': 'int' | 'char' | 'bool' | <class name>,
                'kind': <SymbolKind.STATIC> | <SymbolKind.FIELD>,
                'idx' : <int> },
            my_var2: {
                'type': 'int' | 'char' | 'bool' | <class name>,
                'kind': <SymbolKind.STATIC> | <SymbolKind.FIELD>,
                'idx' : <int> }
                },

        SymbolScope.SUBROUTINE: {
            my_var1: {
                'type': 'int' | 'char' | 'bool' | <class name>,
                'kind': <SymbolKind.ARG> | <SymbolKind.VAR>,
                'idx' : <int> },
            my_var2: {
                'type': 'int' | 'char' | 'bool' | <class name>,
                'kind': <SymbolKind.ARG> | <SymbolKind.VAR>,
                'idx' : <int> }
                },

    }
    '''

    idx_lookup   : dict[SymbolKind, int]  = field(init=False)
    scope_lookup : dict[SymbolKind, SymbolScope] = field(init=False)
    kind_lookup  : dict[str, SymbolKind] = field(init=False)

    def __post_init__(self):
        self.symbols = {
                SymbolScope.CLASS      : {},
                SymbolScope.SUBROUTINE : {}
                }

        self.idx_lookup = {
                SymbolKind.STATIC : 0,
                SymbolKind.FIELD  : 0,
                SymbolKind.ARG    : 0,
                SymbolKind.VAR    : 0 
                }

        self.scope_lookup = {
                SymbolKind.STATIC : SymbolScope.CLASS,
                SymbolKind.FIELD  : SymbolScope.CLASS,
                SymbolKind.ARG    : SymbolScope.SUBROUTINE,
                SymbolKind.VAR    : SymbolScope.SUBROUTINE 
                }

        self.kind_lookup = {
                'static': SymbolKind.STATIC,
                'field' : SymbolKind.FIELD,
                'arg'   : SymbolKind.ARG,
                'var'   : SymbolKind.VAR
                }

    def define(self, name: str, symbol_type: str, symbol_kind: str):
        symbol_kind = self.kind_lookup[symbol_kind]

        self.symbols[self.scope_lookup[symbol_kind]][name] = {
                'type': symbol_type,
                'kind': symbol_kind,
                'idx' : self.idx_lookup[symbol_kind]
                }

        self.idx_lookup[symbol_kind] += 1


        # Logging
        '''
        print("Adding to symbols table")
        pprint.PrettyPrinter(depth=4).pprint(self.symbols)
        print()
        '''

    def start_subroutine(self):
        self.idx_lookup[SymbolKind.ARG] = 0
        self.idx_lookup[SymbolKind.VAR] = 0
        self.symbols[SymbolScope.SUBROUTINE] = {}

    def var_count(self, symbol_kind: SymbolKind) -> int:
        return self.idx_lookup.get(symbol_kind, 0)

    def kind_of(self, name: str) -> SymbolKind:
        if name in symbols[SymbolScope.SUBROUTINE]:
            return symbols[SymbolScope.SUBROUTINE][name]['kind']
        elif name in symbols[SymbolScope.CLASS]:
            return symbols[SymbolScope.CLASS][name]['kind']
        else:
            raise SyntaxError("Unknown symbol {}".format(name))

    def type_of(self, name: str) -> TokenType:
        if name in symbols[SymbolScope.SUBROUTINE]:
            return symbols[SymbolScope.SUBROUTINE][name]['type']
        elif name in symbols[SymbolScope.CLASS]:
            return symbols[SymbolScope.CLASS][name]['type']
        else:
            raise SyntaxError("Unknown symbol {}".format(name))

    def index_of(self, name: str) -> int:
        if name in symbols[SymbolScope.SUBROUTINE]:
            return symbols[SymbolScope.SUBROUTINE][name]['idx']
        elif name in symbols[SymbolScope.CLASS]:
            return symbols[SymbolScope.CLASS][name]['idx']
        else:
            raise SyntaxError("Unknown symbol {}".format(name))
