from enum import Enum
TokenType = Enum('TokenType', ['KEYWORD', 'SYMBOL', 'IDENTIFIER',
                               'INT_CONST', 'STRING_CONST'])

# TODO: Delete keyword enum
Keyword = Enum('Keyword', ['CLASS', 'METHOD', 'FUNCTION', 'CONSTRUCTOR', 
                           'INT', 'BOOLEAN', 'CHAR', 'VOID', 'VAR',
                           'STATIC', 'FIELD', 'LET', 'DO', 'IF', 
                           'ELSE', 'WHILE', 'RETURN', 'TRUE', 
                           'FALSE', 'NULL', 'THIS'])

SymbolKind = Enum('SymbolKind', ['STATIC', 'FIELD', 'ARG', 'VAR'])
SymbolScope = Enum('SymbolScope', ['CLASS', 'SUBROUTINE'])

Segment = Enum('Segment', ['CONST', 'ARG', 'LOCAL', 'STATIC', 'THIS',
                           'THAT', 'POINTER', 'TEMP'])

Command = Enum('Command', ['ADD', 'SUB', 'NEG', 'EQ', 'GT', 'LT', 'AND', 'OR', 'NOT'])
