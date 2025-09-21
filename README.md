# Emulator Project

## Overview

This project implements a customizable emulator for a simple processor architecture. The emulator can be configured through a YAML file to support different instruction sets, memory sizes, and register configurations.

## Project Structure

```
.
├── config.yaml          # Processor configuration
├── main.py             # Main entry point
├── requirements.txt    # Project dependencies
├── emul/              # Emulator package directory
│   ├── __init__.py    # Package initialization
│   ├── config.py      # Configuration handling
│   ├── emul.py        # Emulator core
│   ├── proc.py        # Processor model
│   └── utils.py       # Utility functions
└── prog/
    └── fact2.asm      # Example program (factorial calculation)
```

## Installation and Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Recommended Setup (using virtual environment)

1. **Create a virtual environment**:
   ```bash
   # On Windows
   python -m venv .venv
   
   # On Linux/MacOS
   python3 -m venv .venv
   ```

2. **Activate the virtual environment**:
   ```bash
   # On Windows
   .venv\Scripts\activate
   
   # On Linux/MacOS
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

The requirements.txt file includes:
- `bitarray==3.7.1` - for efficient bit-level operations
- `PyYAML==6.0.2` - for parsing configuration files

### Running the Emulator
After setting up the environment and installing dependencies, run:
```bash
python main.py
```

### Deactivating the Virtual Environment
When you're done working with the project, you can deactivate the virtual environment:
```bash
deactivate
```

## Configuration (config.yaml)

The processor configuration is defined in `config.yaml` with the following structure:

### Key Parameters:
- `commands`: List of supported instructions with their parameter sizes
- `commands_size`: Number of bits for command addressing (2^7 = 128 commands)
- `command_size`: Total bits per command (19 bits)
- `cop_size`: Bits for operation code (4 bits)
- `memory_size`: Number of bits for memory addressing (2^7 = 128 memory cells)
- `register_file`: Number of bits for register addressing (2^2 = 4 registers)
- `literal_size`: Size of literal values (8 bits)

### Instruction Format:
Each instruction is defined with its parameters and their bit sizes:
```yaml
- LTM:
    memory_address: 7
    literal: 8
```

## Current Configuration Analysis

### Instruction Set:
1. **NOP** - No operation
2. **LTM** - Load to memory: `memory_address (7b)`, `literal (8b)`
3. **MTR** - Memory to register: `memory_address (7b)`, `register_address (2b)`
4. **JMPIF** - Conditional jump: `command_address (7b)`
5. **MULT** - Multiplication: `first_operand (2b)`, `second_operand (2b)`, `register_address (2b)`
6. **RTM** - Register to memory: `memory_address (7b)`, `register_address (2b)`
7. **DECR** - Decrement register: `register_address (2b)`
8. **JMP** - Unconditional jump: `command_address (7b)`
9. **PUSH** - Push register to stack: `register_address (2b)`
10. **POP** - Pop from stack to register: `register_address (2b)`
11. **LTRA** - Load to return address: `literal (8b)`
12. **RET** - Return from subroutine
13. **PUSHRA** - Push return address to stack
14. **POPRA** - Pop return address from stack
15. **RTR** - Register to register: `first_register (2b)`, `second_register (2b)`

### Memory Architecture:
- **Command memory**: 128 commands × 19 bits each
- **Data memory**: 128 cells × 8 bits each
- **Registers**: 4 registers × 8 bits each
- **Stack**: Dynamic stack storage
- **Return address**: 8-bit return address register

## Example Program: fact2.asm

This program calculates the factorial of a number using recursive function calls.

### Program Flow:
1. **Initialization**: Load value 3 into memory and register
2. **Function call setup**: Prepare return address and push parameters
3. **Recursive calculation**: 
   - Check base case (JMPIF)
   - Recursive call with decremented value
   - Multiply results
4. **Return handling**: Pop results and return to caller

### Instruction Execution:
The emulator processes instructions by:
1. Fetching the next command from command memory
2. Decoding the operation code (first 4 bits)
3. Extracting parameters based on the configuration
4. Executing the operation
5. Updating program counter

## Package Structure

The emulator is organized as a Python package (`emul/`) with the following modules:

- **`config.py`**: Handles configuration parsing and setup
- **`emul.py`**: Core emulator class with instruction execution logic
- **`proc.py`**: Processor model with memory, registers, and stack
- **`utils.py`**: Utility functions for program loading and parsing
- **`__init__.py`**: Package initialization file

## Usage

### Running the Emulator:
```bash
python main.py
```

### Creating Custom Configurations:
1. Modify `config.yaml` to define your instruction set
2. Update parameter sizes according to your needs
3. Write assembly programs using the defined instructions
4. Place programs in the `prog/` directory

### Writing Assembly Programs:
- Use the instruction mnemonics defined in config.yaml
- Labels must follow pattern `L[0-9]+` (e.g., L1, L2)
- Separate arguments with commas
- One instruction per line
- Labels can be placed at the beginning of lines followed by colon

## Customization

### Adding New Instructions:
1. Add the instruction to `config.yaml` with parameter sizes
2. Implement the execution logic in `emul.py` in the `execute_programm` method
3. Add pattern matching for the new instruction

### Modifying Architecture:
- Change memory sizes in config.yaml
- Adjust register file size
- Modify command and literal sizes
- Update cop_size for different instruction encoding

## Implementation Details

### Bit-level Operations:
The emulator uses the `bitarray` library for precise bit-level manipulation, ensuring accurate representation of the processor's binary operations.

### Command Encoding:
Each command is encoded as:
```
[COP (4 bits)][PARAMETERS (15 bits)]
```

### Memory Organization:
- Commands: Stored as bitarrays in sequential memory
- Data: 8-bit values in addressable memory
- Registers: 4 general-purpose 8-bit registers
- Stack: LIFO structure for function calls and temporary storage

## Example Output

After running the factorial calculation, the emulator will display:
- Final state of all memory locations
- Register values
- Stack contents
- Return address value
- Program counter position

This emulator provides a flexible framework for experimenting with different processor architectures and instruction sets while maintaining accurate binary-level execution.

## License

This project is open source and available under the MIT License.