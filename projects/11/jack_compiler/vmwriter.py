from dataclasses import dataclass, field
import typing
import os
from .enums import Segment, Command

@dataclass
class VMWriter:

    input_filename  : str
    output_filename : str = field(init=False)
    write_file      : typing.IO = field(init=False)

    def __post_init__(self):
        self.output_filename = self.create_output_filename(self.input_filename)
        self.writefile = open(self.output_filename, 'w')

    def create_output_filename(self, jack_file):
        return ''.join([os.path.splitext(jack_file)[0], '.z', '.vm'])

    def write_push(self, segment: Segment, idx: int):
        pass

    def write_pop(self, segment: Segment, idx: int):
        pass

    def write_arithmetic(self, command: Command):
        pass

    def write_label(self, label: str):
        pass

    def write_goto(self, label: str):
        pass

    def write_if(self, label: str):
        pass

    def write_call(self, name: str, n_args: int):
        pass

    def write_function(self):
        pass

    def write_return(self):
        pass

    def close(self):
        self.writefile.close()
