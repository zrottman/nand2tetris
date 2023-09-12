from dataclasses import dataclass, field
import typing
import os

@dataclass
class VMWriter:

    input_filename  : str
    output_filename : str = field(init=False)
    write_file      : typing.IO = field(init=False)

    def __post_init__(self):
        self.output_filename = self.create_output_filename(self.input_filename)
        self.writefile = open(self.output_filename, 'w')

    def create_output_filename(self, jack_file):
        return ''.join([os.path.splitext(jack_file)[0], '.z', '.xml'])

    def write_push(self):
        pass

    def write_pop(self):
        pass

    def write_arithmetic(self):
        pass

    def write_label(self):
        pass

    def write_goto(self):
        pass

    def write_if(self):
        pass

    def write_call(self):
        pass

    def write_function(self):
        pass

    def write_return(self):
        pass

    def close(self):
        self.writefile.close()
