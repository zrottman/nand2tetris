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
    '''

    def __init__(self, read_path, code_writer):
        self.file = open(read_path, 'r')    # file object
        self.writer = code_writer 
        self.writer.set_file_id(read_path.rstrip('/').split('/')[-1])  # for label/static disambiguation

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
            case 'function':
                return Command.FUNCTION
            case 'call':
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
                    self.writer.write_function(self.arg_1(line), self.arg_2(line))
                case Command.CALL:
                    self.writer.write_call(self.arg_1(line), self.arg_2(line))
                case Command.RETURN:
                    self.writer.write_return()
                case _:
                    pass

        # Close input file
        self.file.close()


class CodeWriter:

    def __init__(self, write_path):
        self.write_path = write_path # + '.asm'           # output file
        print("CodeWriter writing to: {}".format(write_path))
        #self.file_id = file.rstrip('/').split('/')[-1]  # for label/static disambiguation
        self.counter = 0                                # for label disambiguation
        self.file_id = "Bootstrap" # Default file id


        # open output file
        self.file = open(self.write_path, 'w')

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

        self.write_init()

    def write_init(self):
        '''
        TODO: Is this right?
        '''
        asm = "\n".join(["////////// START BOOTSTRAP", "@256", "D=A", "@SP", "M=D", "// call Sys.init 0", ""])
        self.file.write(asm)
        self.write_call("Sys.init", "0")

    def set_file_id(self, file_id):
        self.file_id = file_id

    def write_filename(self):
        '''
        Write current .vm filename as comment
        '''
        asm = "\n".join(["////////// START VM FILE: {}".format(self.file_id), ""])
        self.file.write(asm)

    def write_vm_line(self, line):
        '''
        Write original VM line as comment
        '''
        asm = "\n".join(["// {}".format(line), ""])
        self.file.write(asm)

    def write_pushpop(self, command, segment, arg):
        '''
        Write push and pop commands
        TODO: Consider writing temp/pointer commands out in long assembly rather than doing math with python
        '''
        asm = None 
        address = {
                "local": "@LCL", "argument": "@ARG", "this": "@THIS", 
                "that": "@THAT", "static": "@{}.{}".format(self.file_id, arg),
                "temp": "@5", "pointer": "@3"
                }

        if segment in ["local", "argument", "this", "that"]:
            match command:
                case Command.PUSH:
                    asm = "\n".join(["@{}".format(arg), "D=A", address[segment], "A=D+M", "D=M", self.commands['push'], ""])
                case Command.POP:
                    asm = "\n".join(["@{}".format(arg), "D=A", address[segment], "D=D+M", self.commands['pop'], ""])

        elif segment in ["temp", "pointer"]:  # TODO clean this up -- try to consolidate
            match command:
                case Command.PUSH:
                    asm = "\n".join(["@{}".format(arg), "D=A", address[segment], "A=D+A", "D=M", self.commands['push'], ""])
                case Command.POP:
                    asm = "\n".join(["@{}".format(arg), "D=A", address[segment], "D=D+A", self.commands['pop'], ""])

        elif segment in ["static"]:
            match command:
                case Command.PUSH:
                    asm = "\n".join([address[segment], "D=M", self.commands['push'], ""])
                case Command.POP:
                    asm = "\n".join([address[segment], "D=A", self.commands['pop'], ""])

        elif segment == "constant" and command == Command.PUSH:
            asm = "\n".join(["@{}".format(arg), "D=A", self.commands['push'], ""])

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
        asm = "\n".join(["({})".format(label), ""])
        self.file.write(asm)

    def write_goto(self, label):
        asm = "\n".join(["@{}".format(label), "0;JMP", ""])
        self.file.write(asm)

    def write_if(self, label):
        asm = "\n".join([self.commands['dec'], "A=M", "D=M", "@{}".format(label), "D;JNE", ""])
        self.file.write(asm)

    def write_function(self, label, local_vars):
        # asm = "\n".join(["({})".format(label), ""]) 
        self.write_label(label)
        for _ in range(int(local_vars)):
            # asm = "\n".join(["@LCL", "D=A", "@{}".format(i), "A=D+A", "M=0", "@SP", "M=M+1"])
            self.write_pushpop(Command.PUSH, "constant", "0");
        # self.file.write(asm)
        
    def write_call(self, function, n):
        '''
        TODO: rely on self.counter to disambiguate (except for static variables).
        '''
        ret_label = "{}.{}".format(self.file_id, self.counter)
        asm = "\n".join(["@SP", "D=M", "@5", "D=D-A", "@{}".format(n), "D=D-A", "@ARG", "M=D", "@SP", "D=M", "@LCL", "M=D", ""])

        self.file.write("// call: push return-address\n")
        self.write_pushpop(Command.PUSH, "constant", ret_label)

        self.file.write("// call: push LCL\n")
        self.file.write("\n".join(["@LCL", "D=M", self.commands['push'], ""]))
        #self.write_pushpop(Command.PUSH, "constant", "0") # "0" formerly "LCL"

        self.file.write("// call: push ARG\n")
        self.file.write("\n".join(["@ARG", "D=M", self.commands['push'], ""]))
        #self.write_pushpop(Command.PUSH, "constant", "0") # "0" formerly "ARG"

        self.file.write("// call: push THIS\n")
        self.file.write("\n".join(["@THIS", "D=M", self.commands['push'], ""]))
        #self.write_pushpop(Command.PUSH, "constant", "0") # "0" formerly "THIS"

        self.file.write("// call: push THAT\n")
        self.file.write("\n".join(["@THAT", "D=M", self.commands['push'], ""]))
        #self.write_pushpop(Command.PUSH, "constant", "0") # "0" formerly "THAT"

        self.file.write("// call: ARG = SP-n-5; LCL = SP\n") # <- this seems to be where my bug is
        self.file.write(asm)
        self.file.write("// call: goto f\n")
        self.write_goto(function)
        self.file.write("// call: (return-address)\n")
        self.write_label(ret_label)

        self.counter += 1

    def write_return(self):
        asm = None
        asm = "\n".join([
            # FRAME = LCL
            "// return: FRAME = LCL",
            "@LCL", "D=M", "@FRAME", "M=D", 
            # RET = *(FRAME-5)
            "// return: RET = *(FRAME-5)",
            #"@5", "D=D-A", "@RET", "M=D", 
            "@5", "A=D-A", "D=M", "@RET", "M=D", 
            # *ARG = pop()
            "// return: *ARG = pop()",
            #"@ARG", "D=M", # Old version -- failed for function call
            "@SP", "M=M-1", "A=M", "D=M", "@ARG", "A=M", "M=D", "@ARG", "D=M",
            # SP = ARG+1
            "// return: SP = ARG+1",
            "@SP", "M=D+1", 
            # THAT = *(FRAME-1)
            "// return: THAT = *(FRAME-1)",
            "@FRAME", "D=M", "@1", "A=D-A", "D=M", "@THAT", "M=D",
            # THIS = *(FRAME-2)
            "// return: THIS = *(FRAME-2)",
            "@FRAME", "D=M", "@2", "A=D-A", "D=M", "@THIS", "M=D",
            # ARG = *(FRAME-3)
            "// return: ARG = *(FRAME-3)",
            "@FRAME", "D=M", "@3", "A=D-A", "D=M", "@ARG", "M=D",
            # LCL = *(FRAME-4)
            "// return: LCL = *(FRAME-4)",
            "@FRAME", "D=M", "@4", "A=D-A", "D=M", "@LCL", "M=D", 
            # goto RET
            "// return: goto RET",
            "@RET", "A=M", "0;JMP", ""
            #"@RET", "0;JMP", ""
            ])
        self.file.write(asm)

    def close(self):
        '''
        Close write file
        '''
        self.file.write("// END WRITE\n")
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
        write_path = os.path.join(path, os.path.basename(os.path.normpath(path)))

    write_path += ".asm"

    return file_list, write_path

def add_line_nums(asm_file):

    out = asm_file.split(".asm")[0] + ".numbered.asm"
    lc = 0
    write_file = open(out, "w")

    print("Adding line numbers to: {}".format(out))

    with open(asm_file, "r") as f:
        while (line := f.readline()):
            if lc % 10 == 0:
                write_file.write("// line: {}\n".format(lc))
            write_file.write(line)
            if not (line.startswith('//') or line.startswith('(')):
                lc += 1

    write_file.close()


if __name__ == '__main__':

    # validate argv
    if len(sys.argv) != 2:
        print("Usage: python3 vm.py <argument>")
        sys.exit(1)

    # get path for vm file or directory with multiple vm files
    read_path = sys.argv[1]
    file_list, write_path = get_files(read_path)

    # create single codewriter object to pass to parsers
    codewriter = CodeWriter(write_path) # <- improve using pathlib?

    # parse all files in `file_list`
    for file in file_list:
        Parser(file, codewriter).parse()

    # close codewriter
    codewriter.close()

    # write line nums file
    add_line_nums(write_path)

