from enum import Enum

TokenType   = Enum('TokenType', ['KEYWORD', 'SYMBOL', 'IDENTIFIER',
                               'INT_CONST', 'STRING_CONST'])

SymbolKind  = Enum('SymbolKind', ['STATIC', 'FIELD', 'ARG', 'VAR'])

SymbolScope = Enum('SymbolScope', ['CLASS', 'SUBROUTINE'])

Segment     = Enum('Segment', ['CONST', 'ARG', 'LOCAL', 'STATIC', 'THIS',
                           'THAT', 'POINTER', 'TEMP'])

Command     = Enum('Command', ['ADD', 'SUB', 'NEG', 'EQ', 'GT', 'LT', 
                           'AND', 'OR', 'NOT'])
