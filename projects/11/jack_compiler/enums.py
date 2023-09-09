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
