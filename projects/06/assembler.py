from enum import Enum
import sys

command = Enum('command', ['A_COMMAND', 'C_COMMAND', 'L_COMMAND'])

class Parser:

    def __init__(self, path):

        self.current_command = ''
        self.path = path[:path.find('.')]

        self.input = []
        self.without_labels = []
        self.output = []

        self.code = Code()
        self.symbol_table = SymbolTable()

        # read assembly file to `input`
        with open (path, "r") as f:
            while (line := f.readline()):

                # strip comments
                comment = line.find('//')
                if comment >= 0: 
                    line = line[:comment]

                # strip newline/space
                line = line.strip()

                # if there's a line, append it
                if line:
                    self.input.append(line)


    def has_more_commands(self):
        return len(self.without_labels) > 0

    def advance(self):
        self.current_command = self.without_labels.pop(0)

    def command_type(self):
        '''
        Return command type based on initial character of `current_command`
        '''
        match self.current_command[0]:
            case '@':
                return command.A_COMMAND
            case '(':
                return command.L_COMMAND
            case _:
                return command.C_COMMAND

    def dest(self):
        '''
        Parse dest component of `current_command`
        '''
        d_end = self.current_command.find('=')
        if d_end >= 0:
            d = self.current_command[:d_end]
            return self.code.dest_table.get(d, '000')
        else:
            return '000'

    def comp(self):
        '''
        Parse compute component of `current_command`
        '''
        c_start = self.current_command.find('=') + 1
        c_end = self.current_command.find(';')
        if c_end > 0:
            c = self.current_command[c_start:c_end]
        else:
            c = self.current_command[c_start:]
        return self.code.comp_table.get(c, '0000000')

    def jump(self):
        '''
        Parse jump component of `current_command`.
        '''
        j_start = self.current_command.find(';') + 1
        if j_start > 0:
            j = self.current_command[j_start:]
            return self.code.jump_table.get(j, '000')
        else:
            return '000'

    def int_to_binstring(self, i):
        '''
        Convert integer to 15-bit bitstring.
        '''
        i = int(i)
        i = min(i, 2 ** 15 - 1)    # limit i to 2**15 - 1
        s = bin(i)[2:]
        return '0000000000000000'[len(s):] + s

    def write(self):
        '''
        Write `output` to input file path + file name and append `_z.hack`
        to differentiate it from files assembled with built-in assembler.
        '''
        outfile = self.path + '_z.hack'
        with open(outfile, 'w') as f:
            f.writelines([line + '\n' for line in self.output])

    def parse_A_command(self):
        '''
        Parse A command. If address is numeric, convert it to binstring. If address
        is a symbol, look up in symbol table (adding if necessary) and convert the
        returned address to binstring.
        '''
        addr = self.current_command[1:]
        if addr.isnumeric():
            pass
        elif self.symbol_table.contains(addr):
            addr = self.symbol_table.get_address(addr)
        else:
            addr = self.symbol_table.add_entry(addr)
        
        return self.int_to_binstring(addr)

    def parse_L_command(self):
        '''
        Returns label without opening/closing parens
        '''
        return self.current_command[1:-1]

    def parse(self):

        # First pass: add loop commands to symbols dict. and delete from input
        lc = 0
        for line in self.input:
            if line.startswith('(') and not self.symbol_table.contains(line[1:-1]):
                self.symbol_table.add_entry(line[1:-1], lc)
            else:
                self.without_labels.append(line)
                lc += 1


        # Second pass: parse input to assembly
        self.advance()
        loop = True

        while loop:

            match self.command_type():

                case command.A_COMMAND:
                    self.output.append(self.parse_A_command())
                
                case command.L_COMMAND:
                    pass

                case command.C_COMMAND:
                    self.output.append('111' + self.comp() + self.dest() + self.jump())

            if not self.has_more_commands():
                loop = False
            else:
                self.advance()

        self.write()


class Code:

    def __init__(self):
        self.dest_table = {
                'M'  :'001',
                'D'  :'010',
                'MD' :'011',
                'A'  :'100',
                'AM' :'101',
                'AD' :'110',
                'AMD':'111'
                }
        self.jump_table = {
                'JGT':'001',
                'JEQ':'010',
                'JGE':'011',
                'JLT':'100',
                'JNE':'101',
                'JLE':'110',
                'JMP':'111'
                }
        self.comp_table = {
                '0'  :'0101010',
                '1'  :'0111111',
                '-1' :'0111010',
                'D'  :'0001100',
                'A'  :'0110000',
                'M'  :'1110000',
                '!D' :'0001101',
                '!A' :'0110001',
                '!M' :'1110001',
                '-D' :'0001111',
                '-A' :'0110011',
                '-M' :'1110011',
                'D+1':'0011111',
                'A+1':'0110111',
                'M+1':'1110111',
                'D-1':'0001110',
                'A-1':'0110010',
                'M-1':'1110010',
                'D+A':'0000010',
                'D+M':'1000010',
                'D-A':'0010011',
                'D-M':'1010011',
                'A-D':'0000111',
                'M-D':'1000111',
                'D&A':'0000000',
                'D&M':'1000000',
                'D|A':'0010101',
                'D|M':'1010101',
                }


    def dest(self, dest): return self.dest_table[dest]
    
    def comp(self, comp): return self.jump_table[compy]

    def jump(self, jump): return self.jump_table[jump]


class SymbolTable:

    def __init__(self):
            self.symbols = {
                    'SP'    :0,
                    'LCL'   :1,
                    'ARG'   :2,
                    'THIS'  :3,
                    'THAT'  :4,
                    'R0'    :0,
                    'R1'    :1,
                    'R2'    :2,
                    'R3'    :3,
                    'R4'    :4,
                    'R5'    :5,
                    'R6'    :6,
                    'R7'    :7,
                    'R8'    :8,
                    'R9'    :9,
                    'R10'   :10,
                    'R11'   :11,
                    'R12'   :12,
                    'R13'   :13,
                    'R14'   :14,
                    'R15'   :15,
                    'SCREEN':16384,
                    'KBD'   :24576
                    }
            self.cur_mem = 16


    def add_entry(self, s, a=None): 
        '''
        to do: only increment self.cur_mem if a == None, otherwise don't
        '''
        if not a:
            a = self.cur_mem
            self.cur_mem += 1
        self.symbols[s] = a
        return self.symbols[s]

    def contains(self, s): return s in self.symbols

    def get_address(self, s): return self.symbols[s]


if __name__ == '__main__':

    parser = Parser(sys.argv[1])

    parser.parse()

    parsed = parser.output
    

    '''
    to do:
    C_INST: split on '=' and ';'
    {:015b} formatting
    dest : "".join(['1' if c in mnd else '0' for c in 'ADM'])
    return s in self,symbols: return self,table,get(symbol) is not None
    '''


