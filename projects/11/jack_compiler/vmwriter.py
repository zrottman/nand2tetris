from dataclasses import dataclass, field
import typing
import os
from .enums import Segment, Command

@dataclass
class VMWriter:

    input_filename  : str
    output_filename : str = field(init=False)
    write_file      : typing.IO = field(init=False)
    segment_lookup  : dict[Segment, str] = field(init=False)
    command_lookup  : dict[Command, str] = field(init=False)

    def __post_init__(self):
        self.output_filename = self.create_output_filename(self.input_filename)
        self.writefile = open(self.output_filename, 'w')
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

    def create_output_filename(self, jack_file):
        return ''.join([os.path.splitext(jack_file)[0], '.z', '.vm'])

    def write_push(self, segment: Segment, idx: int):
        self.write_file.write(' '.join(['push', segment_lookup[segment], idx]))

    def write_pop(self, segment: Segment, idx: int):
        self.write_file.write(' '.join(['pop', segment_lookup[segment], idx]))

    def write_arithmetic(self, command: Command):
        self.write_file.write(command_lookup[command])

    def write_label(self, label: str):
        self.write_file.write(' '.join(['label', label]))

    def write_goto(self, label: str):
        self.write_file.write(' '.join(['goto', label]))

    def write_if(self, label: str):
        self.write_file.write(' '.join(['if', label]))

    def write_call(self, name: str, n_args: int):
        self.write_file.write(' '.join(['call', name, str(n_args)]))

    def write_function(self, name: str, n_locals: int):
        self.write_file.write(' '.join(['function', name, str(n_locals)]))

    def write_return(self):
        self.write_file.write('return')

    def close(self):
        self.writefile.close()
