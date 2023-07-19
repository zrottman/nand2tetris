import sys, os
from enum import Enum
from pathlib import Path

Command = Enum('Command', [
    'ARITHMETIC', 'PUSH', 'POP', 'LABEL', 
    'GOTO', 'IF', 'FUNCTION', 'RETURN', 'CALL'
])

class Parser:
    '''
    Parser object for each .vm file which is responsible for looping through 
    input file, parsing each line, and passing the parsed result to CodeWriter
    object, which writes assembly translation to file.

    Parameters
        read_path: path to input file
        write_path: path to output file
        final_parser (default False): for projects with multiple .vm files, 
            flags whether current .vm file is the final one, in which case 
            write an infinite loop at program end.
    '''

    def __init__(self, read_path, write_path, final_parser=False):
        self.path = read_path               # input file path
        self.file = open(self.path, 'r')    # file object

        # instantiate CodeWriter with root and write path args
        self.writer = CodeWriter(read_path.split('.')[0], write_path) # <- improve using pathlib?

    def advance(self):
        '''
        Advance to next non-empty line after stripping comments and return `line`
        '''
        while (line := self.file.readline()) and not (line := line.split('//')[0].strip()):
            continue
        return line

    def command_type(self, line):
        '''
        Return command type.
        '''
        command = line.split()[0]   # get first element from `line`
        match command:
            case 'push':
                return Command.PUSH
            case 'pop':
                return Command.POP
            case 'add' | 'sub' | 'neg' | 'eq' | 'gt' | 'lt' | 'and' | 'or' | 'not':
                return Command.ARITHMETIC
            case 'label':
                return Command.LABEL
            case 'goto':
                return Command.GOTO
            case 'if-goto':
                return Command.IF
            case 'Function':
                return Command.FUNCTION
            case 'Call':
                return Command.CALL
            case 'return':
                return Command.RETURN
            case _:
                pass

    def arg_1(self, line):
        '''
        If arithmetic command, returns first element from line, else 
        returns second element.
        '''
        if self.command_type(line) == Command.ARITHMETIC:
            return line.split()[0]
        else:
            return line.split()[1]

    def arg_2(self, line):
        '''
        Return third element from line
        '''
        return line.split()[2]
    
    def parse(self):
        '''
        Main parsing function
        '''

        # Write filename as comment
        self.writer.write_filename()

        # Loop through file and process
        while (line := self.advance()):

            # write VM line as comment
            self.writer.write_vm_line(line)

            # parse and write line
            match self.command_type(line):

                case Command.PUSH | Command.POP:
                    self.writer.write_pushpop(self.command_type(line), self.arg_1(line), self.arg_2(line))
                case Command.ARITHMETIC:
                    self.writer.write_arithmetic(self.arg_1(line))
                case Command.LABEL:
                    self.writer.write_label(self.arg_1(line))
                case Command.GOTO:
                    self.writer.write_goto(self.arg_1(line))
                case Command.IF:
                    self.writer.write_if(self.arg_1(line))
                case Command.FUNCTION:
                    pass
                case Command.CALL:
                    pass
                case Command.RETURN:
                    pass
                case _:
                    pass

        # Close input file
        self.file.close()

        # Close writer file
        self.writer.close()

class CodeWriter:

    def __init__(self, file, write_path):
        self.write_path = write_path + '.asm'           # output file
        self.file_id = file.rstrip('/').split('/')[-1]  # for label/static disambiguation
        self.counter = 0                                # for label disambiguation

        # open output file
        self.file = open(self.write_path, 'a')

        self.commands = {
                "inc": "\n".join(["@SP", "M=M+1"]),
                "dec": "\n".join(["@SP", "M=M-1"]),
                }
        self.commands.update({ 
                "push": "\n".join(["@SP", "A=M", "M=D", self.commands['inc']]),
                "pop": "\n".join(["@R13", "M=D", self.commands['dec'], "A=M", "D=M", "@R13", "A=M", "M=D"]),
                "unary_load": "\n".join([self.commands['dec'], "A=M"]), 
                })
        self.commands.update({ 
                "binary_load": "\n".join([self.commands['unary_load'], "D=M", self.commands['unary_load']]) 
                })

    def write_filename(self):
        '''
        Write current .vm filename as comment
        '''
        asm = "\n".join(["//", "// START VM FILE: {}".format(self.file_id), "//", ""])
        self.file.write(asm)

    def write_vm_line(self, line):
        '''
        Write original VM line as comment
        '''
        asm = "\n".join(["// {}".format(line), ""])
        self.file.write(asm)

    def write_pushpop(self, command, segment, index):
        '''
        Write push and pop commands
        '''
        asm = None 
        address = {
                "local": "@LCL", "argument": "@ARG", "this": "@THIS", 
                "that": "@THAT", "static": "@{}.{}".format(self.file_id, index),
                "temp": "@{}".format(5+int(index)), "pointer": "@{}".format(3+int(index))
                }

        if segment in ["local", "argument", "this", "that"]:
            match command:
                case Command.PUSH:
                    asm = "\n".join(["@{}".format(index), "D=A", address[segment], "A=D+M", "D=M", self.commands['push'], ""])
                case Command.POP:
                    asm = "\n".join(["@{}".format(index), "D=A", address[segment], "D=D+M"], self.commands['pop'], "")

        elif segment in ["static", "temp", "pointer"]:
            match command:
                case Command.PUSH:
                    asm = "\n".join([address[segment], "D=M", self.commands['push'], ""])
                case Command.POP:
                    asm = "\n".join([address[segment], "D=A"], self.commands['ppop'], "")

        elif segment == "constant" and command == Command.PUSH:
            asm = "\n".join(["@{}".format(index), "D=A", self.commands['push'], ""])

        assert asm is not None

        self.file.write(asm)

    def write_arithmetic(self, command):
        '''
        Write arithmetic commend
        '''
        asm = None

        # unary computation
        if command in ["neg", "not"]:
            match command:
                case "neg":
                    asm = "\n".join([self.commands['unary_load'], "M=-M", self.commands['inc'], ""])
                case "not":
                    asm = "\n".join([self.commands['unary_load'], "M=!M", self.commands['inc'], ""])

        # binary computation
        elif command in ["add", "sub", "and", "or"]:
            match command:
                case "add":
                    asm = "\n".join([self.commands['binary_load'], "M=D+M", self.commands['inc'], ""])
                case "sub":
                    asm = "\n".join([self.commands['binary_load'], "M=M-D", self.commands['inc'], ""])
                case "and":
                    asm = "\n".join([self.commands['binary_load'], "M=D&M", self.commands['inc'], ""])
                case "or":
                    asm = "\n".join([self.commands['binary_load'], "M=D|M", self.commands['inc'], ""])

        # binary comparison
        elif command in ["eq", "gt", "lt"]:
            jumps = { "eq": "D;JEQ", "gt": "D;JLT", "lt": "D;JGT" }
            asm = "\n".join([
                self.commands['binary_load'], 
                "D=D-M", 
                "@TRUE.{}${}".format(self.file_id, self.counter), 
                jumps[command], 
                "D=0", 
                "@ENDIF.{}${}".format(self.file_id, self.counter), 
                "0;JMP", 
                "(TRUE.{}${})".format(self.file_id, self.counter),
                "D=-1",
                "(ENDIF.{}${})".format(self.file_id, self.counter),
                "@SP",
                "A=M",
                "M=D",
                self.commands['inc'],
                ""
                ])
            self.counter += 1

        assert asm is not None

        self.file.write(asm)

    def write_label(self, label):
        self.file.write("({})\n".format(label));

    def write_goto(self, label):
        self.file.write("@{}\n".format(label));
        self.file.write("0;JMP\n");

    def write_if(self, label):
        # pop top from stack
        self.file.write('\n'.join([self.commands['dec'], '']))
        self.file.write("A=M\n")
        self.file.write("D=M\n")
        # if 0, jump
        self.file.write("@{}\n".format(label))
        self.file.write("D;JNE\n")

    def write_function(self, label, local_vars):

        #"{}.{}".format(self.file_id, label) # Foo.bar

        '''
        - local variables segment initialize to zeros
        - this, that, pointer, temp are undefined
        - push return value back to stack
        '''
        pass

    def write_call(self, function):
        pass

    def write_return(self):
        pass
    
    def close(self):
        '''
        Close write file
        '''
        self.file.close()

def get_files(path):
    '''
    Return list of files for processing from CLI input. If user inputs a single .vm
    file, function returns a list with one item; if user inputs a directory, function
    returns a list of all .vm functions in `path`.
    '''
    file_list = []
    write_path = ''

    if os.path.isfile(path) and path.endswith('.vm'):

        # Single .vm file provided
        file_list.append(path)
        write_path = os.path.splitext(path)[0]

    elif os.path.isdir(path):

        # Directory provided; add all .vm files
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.vm'):
                file_list.append(file_path)
        write_path = path.rstrip('/')

    return file_list, write_path


if __name__ == '__main__':

    # validate argv
    if len(sys.argv) != 2:
        print("Usage: python3 vm.py <argument>")
        sys.exit(1)

    # get path for vm file or directory with multiple vm files
    read_path = sys.argv[1]
    file_list, write_path = get_files(read_path)

    # parse all files in `file_list`
    for file in file_list:
        Parser(file, write_path).parse()

