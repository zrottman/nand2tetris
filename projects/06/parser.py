class Parser:

    def __init__(self):
        self.s = ''

    def parse(self, s):
        self.s = s
        self.tokenizer = Tokenizer(s)
        self.lookahead = self.tokenizer.get_next_token()

        return self.Program()

    def Program(self):
        return {'type':'Program', 'body':self.Literal()}

    def Literal(self):
        match self.lookahead['type']:
            case 'NUMBER':
                return self.NumericLiteral()
            case 'STRING':
                return self.StringLiteral()

    def NumericLiteral(self):
        token = self.eat('NUMBER')
        return {'type':'NumericLiteral', 'value': int(token['value'])}

    def StringLiteral(self):
        token = self.eat('STRING')
        return {'type': 'StringLiteral', 'value': token['value']}

    def eat(self, token_type):
        token = self.lookahead

        if token == None:
            raise Exception("Unexpected end of input, expected {}".format(token_type))
    
        if token['type'] != token_type:
            raise Exception("Unexpected token: {}, expected {}".format(token['type'], token_type))

        # Advance to next token
        self.lookahead = self.tokenizer.get_next_token()

        return token


class Tokenizer:

    def __init__(self, s):
        self.s = s
        self.i = 0;

    def is_EOF(self):
        return self.i == len(self.s)

    def has_more_tokens(self):
        return self.i < len(self.s)

    def get_next_token(self):
        print("i={} (len(self.s)={})".format(self.i, len(self.s)))
        if (not self.has_more_tokens()):
            return None

        s = self.s[self.i:]

        # Numbers
        if(s[self.i].isnumeric()):
            num = ''
            while self.has_more_tokens() and s[self.i].isnumeric():
                num += s[self.i]
                self.i += 1
            return { 'type': 'NUMBER', 'value': num }

        # Strings
        if (s[0] == '"' or s[0] == "'"):
            strng = ''
            self.i += 1

            if s[0] == '"':
                while s[self.i] != '"' and not self.is_EOF():
                    strng += s[self.i]
                    self.i += 1
            elif s[0] == "'":
                while s[self.i] != "'" and not self.is_EOF():
                    strng += s[self.i]
                    self.i += 1

            self.i += 1
            return { 'type': 'STRING', 'value': strng }

        return None

if __name__ == '__main__':

    import json

    parser = Parser()
    
    program = "'42'"

    ast = parser.parse(program)

    print(json.dumps(ast, indent=4))
