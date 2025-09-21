import os
import re
from collections import defaultdict
from bitarray import bitarray
from emul.emul import Emulator


def programm_to_emul(emul: 'Emulator', programm_path: str) -> None:
    programm: list[bitarray] = []
    marks_table: dict[str, int] = defaultdict(str)

    start = emul.get_programm_addr()
    with open(programm_path, 'r') as f:
        programm_text = f.read().split('\n')
    
    for i, command in enumerate(programm_text, start=start):
        parts = command.split(': ')
        if len(parts) > 2:
            raise SyntaxError('Only one mark at start of command can be given.')
        if len(parts) == 2:
            mark, command = tuple(parts)
            if re.match('L[0-9]+', mark):
                marks_table[mark] = i
            else:
                raise SyntaxError(f'{mark=} does not match the mark pattern.')
        else:
            command = parts[0]
        if not re.match('^[A-Z]+( [L0-9]+(,[L0-9])*)?$', command):
            raise SyntaxError(f'{command=} does not match the command pattern.')

    for i, command in enumerate(programm_text, start=start):
        parts = command.split()
        if len(parts) > 3:
            raise ValueError('Too much arguments were given to command.')
        elif len(parts) == 3:
            mark, cop, args = parts
            args = args.split(',')
        elif len(parts) == 2:
            cop, args = parts
            args = args.split(',')
        else:
            cop, = parts
            args = []
        
        idx, pattern_args = emul.config.get_command_by_name(cop)
        if idx is None:
            raise ValueError(f'No such command: {cop}')
        if len(pattern_args) != len(args):
            raise ValueError(
                f'{len(pattern_args)} arguments were expected, '
                f'{len(args)} arguments were given.'
            )
        
        bits = bitarray(emul.config.command_size)
        bits.setall(0)
        bit_idx = emul.config.cop_size
        bits = bitarray(f'{idx:0{emul.config.cop_size}b}') + '_' + bits[bit_idx:]
        for size, arg in zip(pattern_args.values(), args):
            try:
                arg = int(arg)
                if (arg > 2 ** size):
                    raise TypeError(f'{arg=} is out of size: {2 ** size}')
                bits = bits[0:bit_idx] + bitarray(f'{arg:0{size}b}') + bits[bit_idx + size:]
                bit_idx += size
            except ValueError:
                bits = bits[0:bit_idx] + bitarray(f'{marks_table[arg]:0{size}b}') + bits[bit_idx + size:]
                bit_idx += size
        
        programm.append(bits)
    emul.load_commands(programm=programm)
