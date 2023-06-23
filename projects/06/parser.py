import re

spec = {
            r"^\d+":"NUMBER",
            r"^\"([^\"]*)\"":"STRING",
            r"^'([^']*)'":"STRING",
            r"^@\d+":"A-INST",
            

            # Skip single line comment
            r"^\/\/.*":None,

            r"^;": ";"
        }



class Parser:

    def __init__(self):
        self.s = ''

    def parse(self, s):
        self.s = s
        self.tokenizer = Tokenizer(s)
        self.lookahead = self.tokenizer.get_next_token()

        return self.Program()

    def Program(self):
        return {'type':'Program', 'body':self.StatementList()}

    def StatementList(self):
        statementList = [self.Statement()]

        while self.lookahead != None:
            statementList.append(self.Statement())

        return statementList

    def Statement(self):
        return self.ExpressionStatement()

    def ExpressionStatement(self):
        expression = self.Expression()
        self.eat(';')
        return {'type': 'ExpressionStatement','expression':expression}

    def Expression(self):
        return self.Literal()

    def Literal(self):
        match self.lookahead['type']:
            case 'NUMBER':
                return self.NumericLiteral()
            case 'STRING':
                return self.StringLiteral()
            case 'A-INST':
                return self.AInst()

    def NumericLiteral(self):
        token = self.eat('NUMBER')
        return {'type':'NumericLiteral', 'value': int(token['value'])}

    def StringLiteral(self):
        token = self.eat('STRING')
        return {'type': 'StringLiteral', 'value': token['value']}

    def AInst(self):
        token = self.eat('A-INST')
        return {'type': 'A-INST', 'value': token['value']}

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
        if (not self.has_more_tokens()):
            return None

        s = self.s[self.i:]

        for r, t in spec.items():
            if (matched := re.match(r, s)):
                self.i += len(matched[0])
                return { 'type': t, 'value': matched[0]}

        raise Exception("Unexpected token: {}".format(s[0]))

if __name__ == '__main__':

    import json

    parser = Parser()
    
    program = "42;"

    ast = parser.parse(program)

    print(json.dumps(ast, indent=4))
