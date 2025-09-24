from dataclasses import dataclass, field
from bitarray import bitarray


@dataclass
class Processor:
    commands: list[bitarray] = field(default_factory=list)
    memory: list[bitarray] = field(default_factory=list)
    registers: list[bitarray] = field(default_factory=list)
    stack: list[bitarray] = field(default_factory=list)
    ra: bitarray = bitarray('0')
    command_idx: int = 0

    def init(
            self, 
            command_size: int, 
            literal_size: int, 
            commands_size: int,  
            memory_size: int, 
            register_file: int, 
        ):
        command_bits = bitarray(command_size)
        literal_bits = bitarray(literal_size)
        command_bits.setall(0)
        literal_bits.setall(0)
        self.commands.extend([command_bits]*2**commands_size)
        self.memory.extend([literal_bits]*2**memory_size)
        self.registers.extend([literal_bits]*2**register_file)

    def load_prog(self, programm: list[bitarray]):
        available_size = len(self.commands) - self.command_idx
        if len(programm) > available_size:
            raise IndexError(f'Got {len(programm)} size programm while {available_size=}.')
        for i, command in enumerate(programm, start=self.command_idx):
            if len(command) != len(self.commands[i]):
                [self.commands[j].setall(0) for j in range(self.command_idx, i)]
                raise ValueError(
                    f'Got {len(command)} size command '
                    f'while expecting {len(self.commands[i])} size command.'
                )
            self.commands[i] = command
        self.command_idx += len(programm)
    
    def clear_prog(self):
        [c.setall(0) for c in self.commands]
        self.command_idx = 0

    def clear(self):
        [m.setall(0) for m in self.memory]
        [r.setall(0) for r in self.registers]
        self.stack.clear()
        self.ra = bitarray('0')

    def __str__(self):
        commands = '\n'.join([f'\t\t{i:03d}: {cmd.to01()}' for i, cmd in enumerate(self.commands)])
        memory = '\n'.join([f'\t\t{i:03d}: {mem.to01()}' for i, mem in enumerate(self.memory)])
        registers = '\n'.join([f'\t\t{i}: {reg.to01()}' for i, reg in enumerate(self.registers)])
        stack = '\n'.join([f'\t\t{i}: {stk.to01()}' for i, stk in enumerate(self.stack)])
        if not stack:
            stack = f'[]'
        else:
            stack = f'[\n{stack}]'
        ra = self.ra.to01()
        str_ = (
            f'Processor(commands=[\n{commands}],\n'
            f'\tmemory=[\n{memory}],\n'
            f'\tregisters=[\n{registers}],\n'
            f'\tstack={stack},\n'
            f'\tra={ra},\n'
            f'\tcommand_idx={self.command_idx})'
        )
        return str_
