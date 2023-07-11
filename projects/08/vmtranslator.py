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

                case Command.PUSH:
                    self.writer.write_push(self.arg_1(line), self.arg_2(line))
                case Command.POP:
                    self.writer.write_pop(self.arg_1(line), self.arg_2(line))
                case Command.ARITHMETIC:
                    self.writer.write_arithmetic(self.arg_1(line))
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

    def write_filename(self):
        '''
        Write current .vm filename as comment
        '''
        self.file.write("//\n// {}\n//\n".format(self.file_id))

    def write_vm_line(self, line):
        '''
        Write original VM line as comment
        '''
        self.file.write("//" + line + "\n")

    def write_push(self, segment, index):
        '''
        Write push command
        '''
        if segment != 'static':
            self._start_write_push(index)
        if segment != 'constant':
            self._mid_write_push(segment, index)
        self._end_write_push()

    def write_pop(self, segment, index):
        '''
        Write pop command
        '''

        self._start_write_pop(segment, index)
        self._mid_write_pop(segment)
        self._end_write_pop()

    def write_arithmetic(self, command):
        '''
        Write arithmetic commend
        '''
        self._start_write_arithmetic(command)
        self._mid_write_arithmetic(command)
        self._end_write_arithmetic()

    def close(self):
        '''
        Close write file
        '''
        self.file.close()

    def _start_write_arithmetic(self, command):
        '''
        If unary command: set D=RAM[--SP]
        Else: set D=RAM[--SP] and then A=RAM[--SP] (two SP decrements)
        '''
        # SP--
        self.file.write("@SP\n")
        self.file.write("M=M-1\n")
        self.file.write("A=M\n")

        if command != 'neg' and command != 'not':
            # D=RAM[SP]
            self.file.write("D=M\n")

            # A=RAM[--SP]
            self.file.write("@SP\n")
            self.file.write("M=M-1\n")
            self.file.write("A=M\n")

    def _mid_write_arithmetic(self, command):
        '''
        Handle conditional command or binary/unary operation.
        '''

        if command == 'eq' or command == 'gt' or command == 'lt':
            # D=y-x
            self.file.write("D=D-M\n")
            # set jump destination with unique file/line-specific label
            self.file.write("@TRUE.{}${}\n".format(self.file_id, self.counter))

            # Jump command
            match command:
                case 'eq':
                    self.file.write("D;JEQ\n")
                case 'gt':
                    self.file.write("D;JLT\n")
                case 'lt':
                    self.file.write("D;JGT\n")

            # D=0 by default
            self.file.write("D=0\n")
            self.file.write("@ENDIF.{}${}\n".format(self.file_id, self.counter))
            self.file.write("0;JMP\n")
            # D=-1 if condition is true
            self.file.write("(TRUE.{}${})\n".format(self.file_id, self.counter))
            self.file.write("D=-1\n")
            self.file.write("(ENDIF.{}${})\n".format(self.file_id, self.counter))
            # RAM[SP]=D
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("M=D\n")

            self.counter += 1

        else:
            match command:
                case 'add':
                    self.file.write("M=D+M\n")
                case 'sub':
                    self.file.write("M=M-D\n")
                case 'and':
                    self.file.write("M=D&M\n")
                case 'or':
                    self.file.write("M=D|M\n")
                case 'neg':
                    self.file.write("M=-M\n")
                case 'not':
                    self.file.write("M=!M\n")

    def _end_write_arithmetic(self):
        '''
        SP++
        '''
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")

    def _start_write_push(self, index):
        '''
        D=i
        '''
        self.file.write("@{}\n".format(index))
        self.file.write("D=A\n")

    def _mid_write_push(self, segment, index):
        '''
        If static: D=@xyz.i
        Else: D=<segment>+i
        '''
        match segment:
            case 'local':
                self.file.write("@LCL\n")
                self.file.write("A=D+M\n")
            case 'argument':
                self.file.write("@ARG\n")
                self.file.write("A=D+M\n")
            case 'this':
                self.file.write("@THIS\n")
                self.file.write("A=D+M\n")
            case 'that':
                self.file.write("@THAT\n")
                self.file.write("A=D+M\n")
            case 'static':
                self.file.write("@{}.{}\n".format(self.file_id, index))
            case 'temp':
                self.file.write("@5\n")
                self.file.write("A=D+A\n")
            case 'pointer':
                self.file.write("@3\n")
                self.file.write("A=D+A\n")
        self.file.write("D=M\n")

    def _end_write_push(self):
        '''
        RAM[SP]=D
        SP++
        '''
        #RAM[SP]=D
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        #SP++
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")

    def _start_write_pop(self, segment, index):
        '''
        If static: D=@xyz.i
        Else: D=i
        '''
        if segment == 'static':
            self.file.write("@{}.{}\n".format(self.file_id, index))
        else:
            self.file.write("@{}\n".format(index))
        self.file.write("D=A\n")

    def _mid_write_pop(self, segment):
        '''
        D=i+<segment>
        '''
        match segment:
            case 'local':
                self.file.write("@LCL\n")
                self.file.write("D=D+M\n")
            case 'argument':
                self.file.write("@ARG\n")
                self.file.write("D=D+M\n")
            case 'this':
                self.file.write("@THIS\n")
                self.file.write("D=D+M\n")
            case 'that':
                self.file.write("@THAT\n")
                self.file.write("D=D+M\n")
            case 'temp':
                self.file.write("@5\n")
                self.file.write("D=D+A\n")
            case 'pointer':
                self.file.write("@3\n")
                self.file.write("D=D+A\n")

    def _end_write_pop(self):
        '''
        RAM[R13]=RAM[segment+i]
        D=RAM[--SP]
        RAM[segment+i]=D
        '''
        # RAM[R13] = RAM[segment+i]
        self.file.write("@R13\n")
        self.file.write("M=D\n")
        # D=RAM[--SP]
        self.file.write("@SP\n")
        self.file.write("M=M-1\n")
        self.file.write("A=M\n")
        self.file.write("D=M\n")
        # RAM[segment+i]=D
        self.file.write("@R13\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")


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
    path = sys.argv[1]
    file_list, write_path = get_files(path)

    # parse all files in `file_list`
    for file in file_list:
        Parser(file, write_path).parse()

