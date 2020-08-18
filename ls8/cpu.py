"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 8 registers
        self.reg = [0] * 8
        # Point counter
        self.pc = 0
        # Memory with 256 bits
        self.ram = [0b0] * 256



    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        
        while running:
            # Set the instruction register using the point counter
            ir = self.ram[self.pc]
            # save the next two operands; some programs will use them
            operand_a = self.ram[self.pc +1]
            operand_b = self.ram[self.pc +2]
            
            # Tell the CPU what to do when given a specific instruction
            # HLT
            if ir == 0b00000001:
                # Stop the program
                running = False
                # Increment counter, even though the program is stopped
                self.pc += 1

            # LDI - set the value of a register to an integer
            # Uses pc and pc+1, pc+2
            elif ir == 0b10000010:
                # Use operand_a and operand_b
                self.reg[operand_a] = operand_b
                # Increase pc by 3
                self.pc += 3
            # PRN - Print the value stored in the given register
            # Use operand_a
            elif ir == 0b01000111:
                # print value in register
                print(self.reg[operand_a])
                self.pc += 2

    def ram_read(self, address):
        """Accept the address to read and return the value stored there"""
        return self.ram[address]

    def ram_write(self, address, value):
        """Accept a value to write and the address to write it to"""
        self.ram[address] = value
    
