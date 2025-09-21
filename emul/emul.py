from bitarray import bitarray
from emul.config import Config, setup_config
from emul.proc import Processor


class Emulator:
    def __init__(self) -> None:
        self.config: Config | None = None
        self.proc: Processor = Processor()

    def get_programm_addr(self) -> int:
        return self.proc.command_idx

    def load_commands(self, programm: list[bitarray]) -> None:
        self.proc.load_prog(programm=programm)

    def clear_commands(self) -> None:
        self.proc.clear_prog()

    def execute_programm(self) -> None:
        program = self.proc.commands
        program_size = len(program)
        cop_size = self.config.cop_size
        literal_size = self.config.literal_size
        i = 0
        while i != program_size:
            command = program[i]
            cop = int(command[0:cop_size].to01(), 2)
            pattern = self.config.commands[cop]
            for cmd, args in pattern.items():
                match cmd:
                    case 'NOP':
                        i += 1
                    case 'LTM': 
                        memory_address = args['memory_address']
                        literal = args['literal']
                        memory_idx = int(command[cop_size:cop_size + memory_address].to01(), 2)
                        value = command[cop_size + memory_address:cop_size + memory_address + literal]
                        self.proc.memory[memory_idx] = value
                        i += 1
                    case 'MTR':
                        memory_address = args['memory_address']
                        register_address = args['register_address']
                        memory_idx = int(command[cop_size:cop_size + memory_address].to01(), 2)
                        register_idx = int(command[cop_size + memory_address:cop_size + memory_address + register_address].to01(), 2)
                        self.proc.registers[register_idx] = self.proc.memory[memory_idx]
                        i += 1
                    case 'JMPIF':
                        command_address = args['command_address']
                        value = int(self.proc.registers[0].to01(), 2)
                        if value > 1:
                            i = int(command[cop_size:cop_size + command_address].to01(), 2)
                        else:
                            i += 1
                    case 'MULT':
                        first_operand = args['first_operand']
                        second_operand = args['second_operand']
                        register_address = args['register_address']
                        register_idx_1 = int(command[cop_size:cop_size + first_operand].to01(), 2)
                        register_idx_2 = int(command[cop_size + first_operand:cop_size + first_operand + second_operand].to01(), 2)
                        register_idx_3 = int(command[cop_size + first_operand + second_operand:cop_size + first_operand + second_operand + register_address].to01(), 2)
                        value1 = int(self.proc.registers[register_idx_1].to01(), 2)
                        value2 = int(self.proc.registers[register_idx_2].to01(), 2)
                        value3 = value1 * value2
                        self.proc.registers[register_idx_3] = bitarray(f'{value3:0{literal_size}b}')
                        i += 1
                    case 'RTM':
                        memory_address = args['memory_address']
                        register_address = args['register_address']
                        memory_idx = int(command[cop_size:cop_size + memory_address].to01(), 2)
                        register_idx = int(command[cop_size + memory_address:cop_size + memory_address + register_address].to01(), 2)
                        self.proc.memory[memory_idx] = self.proc.registers[register_idx]
                        i += 1
                    case 'DECR':
                        register_address = args['register_address']
                        register_idx = int(command[cop_size:cop_size + register_address].to01(), 2)
                        value = int(self.proc.registers[register_idx].to01(), 2) - 1
                        self.proc.registers[register_idx] = bitarray(f'{value:0{literal_size}b}')
                        i += 1
                    case 'JMP':
                        command_address = args['command_address']
                        i = int(command[cop_size:cop_size + command_address].to01(), 2)
                    case 'PUSH':
                        register_address = args['register_address']
                        register_idx = int(command[cop_size:cop_size + register_address].to01(), 2)
                        value = self.proc.registers[register_idx]
                        self.proc.stack.append(value)
                        i += 1
                    case 'POP':
                        register_address = args['register_address']
                        register_idx = int(command[cop_size:cop_size + register_address].to01(), 2)
                        value = self.proc.stack.pop()
                        self.proc.registers[register_idx] = value
                        i += 1
                    case 'LTRA':
                        literal = args['literal']
                        value = command[cop_size:cop_size + literal]
                        self.proc.ra = value
                        i += 1
                    case 'RET':
                        i = int(self.proc.ra.to01(), 2)
                    case 'PUSHRA':
                        value = self.proc.ra
                        self.proc.stack.append(value)
                        i += 1
                    case 'POPRA':
                        value = self.proc.stack.pop()
                        self.proc.ra = value
                        i += 1
                    case 'RTR':
                        first_register = args['first_register']
                        second_register = args['second_register']
                        register_idx_1 = int(command[cop_size:cop_size + first_register].to01(), 2)
                        register_idx_2 = int(command[cop_size + first_register:cop_size + first_register + second_register].to01(), 2)
                        self.proc.registers[register_idx_2] = self.proc.registers[register_idx_1]
                        i += 1
                    case _: pass
    
    def clear_proc(self) -> None:
        self.proc.clear()

    def __str__(self):
        return f'Emulator(config={self.config!s},\n\tproc={self.proc!s})'


emul = Emulator()


def setup_emul(config_path: str) -> Emulator:
    setup_config(emul, config_path)
    return emul
