import typing
import yaml
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from emul.emul import Emulator


@dataclass
class Config:
    commands: list[dict]
    commands_size: int
    command_size: int
    cop_size: int
    memory_size: int
    register_file: int
    literal_size: int

    def get_command_by_name(self, command_name) -> tuple[int, dict] | None:
        cmd = [(i, command[command_name]) for i, command in enumerate(self.commands) if command_name in command]
        if cmd:
            return cmd[0]
        else:
            return None
        
    def __str__(self):
        commands = '\n'.join([f'\t\t{i:02d}: {cmd}' for i, cmd in enumerate(self.commands)])
        str_ = (
            f'Processor(commands=[\n{commands}],\n'
            f'\tcommands_size={self.commands_size},\n'
            f'\tcommand_size={self.command_size},\n'
            f'\tcop_size={self.cop_size},\n'
            f'\tmemory_size={self.memory_size},\n'
            f'\tregister_file={self.register_file},\n'
            f'\tliteral_size={self.literal_size})'
        )
        return str_


def setup_config(emul: 'Emulator', config_path: str):
    with open(config_path, 'r') as f:
        raw_config = yaml.safe_load(f)
    
    emul.config = Config(
        commands=raw_config['commands'],
        commands_size=raw_config['commands_size'],
        command_size=raw_config['command_size'],
        cop_size=raw_config['cop_size'],
        memory_size=raw_config['memory_size'],
        register_file=raw_config['register_file'],
        literal_size=raw_config['literal_size'],
    )

    emul.proc.init(
        emul.config.command_size, 
        emul.config.literal_size,
        emul.config.commands_size,
        emul.config.memory_size,
        emul.config.register_file,
    )
