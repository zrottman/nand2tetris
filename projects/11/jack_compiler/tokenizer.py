from dataclasses import dataclass, field
import typing
import re
from .enums import TokenType

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
        TokenType.INT_CONST   : 'integerConstant',
        TokenType.STRING_CONST: 'stringConstant',
    }

    def display_token(self):
        val =  self.xml_special_chars.get(self.value, self.value)
        return "<{}> {} </{}>".format(
            self.tokens.get(self._type, "unknown token"), 
            val,
            self.tokens.get(self._type, "unknown token"))

@dataclass
class Tokenizer:
    
    jack_file       : str
    cursor          : int = field(default=0, init=False)
    lexical_elements: typing.ClassVar[list[list[typing.Pattern, TokenType]]] = [

            # numbers
            [re.compile(r"^(\d+)"), TokenType.INT_CONST],

            # strings
            [re.compile(r"^(\"[^\"]*\")"), TokenType.STRING_CONST],
            [re.compile(r"^('[^']*.')"), TokenType.STRING_CONST],

            # comments
            [re.compile(r"^(//.*)"), None],
            [re.compile(r"^(\/\*.*?\*\/)", flags=re.DOTALL), None],

            # whitespace
            [re.compile(r"^([\s\n]+)"), None],

            # keywords
            # TODO: This regex needs to be updated, since variable names that start with
            # any of these keywords (i.e., `double` or `classic`) will erroneously match
            # and compile as KEYWORDs rather than IDENTIFIERs. One solution is to wrap each
            # regex statement in parens to group then, and then to include [^a-zA-Z0-9] in the
            # regex below, and then to extract the matched group with `match[1]` syntax in
            # `match_token()` function
            [re.compile(r"""^
                (class | constructor | function | method |
                field | static | var | int | char | boolean |
                void | true | false | null | this | let | do |
                if | else | while | return)[^a-zA-Z0-9]
                """, re.X), TokenType.KEYWORD],

            # symbols
            [re.compile(r"^([\{\}\(\)\[\]\.\,\;\+\-\*\/\&\|\<\>\=\~])"), TokenType.SYMBOL],

            # identifiers
            [re.compile(r"^([a-zA-Z][a-zA-Z0-9\_]*)"), TokenType.IDENTIFIER]]

    def __post_init__(self):
        with open(self.jack_file, "r") as f:
            self.jack_code = f.read()

    def has_more_tokens(self):
        return self.cursor < len(self.jack_code)

    def get_next_token(self, advance_cursor=True):
        '''
        TODO: Fix hacky approach to peeking with `advance_cursor
        '''
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
                return self.get_next_token(advance_cursor)

            # remove outer quotes when matching strings
            if token_type == TokenType.STRING_CONST:
                token = token[1:-1]

            # if advance_cursor == False, undo cursor advance from self.match_token()
            if not advance_cursor: self.cursor -= len(token)

            return Token(token_type, token)

        raise SyntaxError("Unexpected Token at position {} beginning with {}".format(self.cursor, cur_str[:10]))

    def match_token(self, regexp, s):
        if not (token := regexp.match(s)):
            return None
        self.cursor += len(token[1])
        return token[1]
