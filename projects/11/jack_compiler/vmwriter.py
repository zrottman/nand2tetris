from dataclasses import dataclass, field
import typing
import os
from .enums import Segment, Command

@dataclass
class VMWriter:

    input_filename  : str
    output_filename : str = field(init=False)
    write_file      : typing.IO = field(init=False)
    segment_lookup  : dict[str, str] = field(init=False)
    #segment_lookup  : dict[Segment, str] = field(init=False)
    #command_lookup  : dict[Command, str] = field(init=False)

    def __post_init__(self):
        self.output_filename = self.create_output_filename(self.input_filename)
        self.write_file = open(self.output_filename, 'w')

        '''
        segment_lookup = {
                Segment.CONST   : 'constant',
                Segment.ARG     : 'argument',
                Segment.LOCAL   : 'local',
                Segment.STATIC  : 'static',
                Segment.THIS    : 'this',
                Segment.THAT    : 'that',
                Segment.POINTER : 'pointer',
                Segment.TEMP    : 'temp'
                }
        '''

        self.segment_lookup = {
                'constant': 'constant',
                'arg'     : 'argument',
                'var'     : 'local',
                'static'  : 'static',
                'field'   : 'this',
                'that'    : 'that', # ??????
                'pointer' : 'pointer', # ??????
                'temp'    : 'temp' #?????
                }

        '''
        command_lookup = {
                Command.ADD : 'add',
                Command.SUB : 'sub',
                Command.NEG : 'neg',
                Command.EQ  : 'eq',
                Command.GT  : 'gt',
                Command.LT  : 'lt', 
                Command.AND : 'and',
                Command.OR  : 'or',
                Command.NOT : 'not'
                }
        '''

    def create_output_filename(self, jack_file):
        return ''.join([os.path.splitext(jack_file)[0], '.z', '.vm'])

    def write_line(self, line):
        self.write_file.write(line)
        self.write_file.write('\n')

    def write_push(self, segment: str, idx: int):
        # push <segment> <idx>
        self.write_line(' '.join(['push', self.segment_lookup[segment], str(idx)]))

    def write_pop(self, segment: str, idx: int):
        # pop <segment> <idx>
        self.write_line(' '.join(['pop', self.segment_lookup[segment], str(idx)]))

    def write_arithmetic(self, command: str):
        # add | sub | call Math.multiply 2 | call Math.divide 2 | 
        # and | or | lt | gt | eq | neg | not
        self.write_line(command)

    def write_label(self, label: str):
        # label <label>
        self.write_line(' '.join(['label', label]))

    def write_goto(self, label: str):
        # goto <label>
        self.write_line(' '.join(['goto', label]))

    def write_if(self, label: str):
        # if-goto <label>
        self.write_line(' '.join(['if-goto', label]))

    def write_call(self, name: str, n_args: int):
        # call <name> <n_args>
        self.write_line(' '.join(['call', name, str(n_args)]))

    def write_function(self, name: str, n_locals: int):
        # function <name> <n_locals>
        self.write_line(' '.join(['function', name, str(n_locals)]))

    def write_return(self):
        # return
        self.write_line('return')

    def close(self):
        self.write_file.close()
