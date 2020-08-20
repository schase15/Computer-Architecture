"""CPU functionality."""

import sys

import sys

# MAIN OPCODES
ADD = 0b10100000
CALL = 0b01010000
CMP = 0b10100111
HLT = 0b00000001
JEQ = 0b01010101
JMP = 0b01010100
JNE = 0b01010110
LDI = 0b10000010
MUL = 0b10100010
NOP = 0b00000000
POP = 0b01000110
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
SUB = 0b10100001

# BITWISE ALU OPCODES
MOD = 0b10100100
SHL = 0b10101100
SHR = 0b10101101
XOR = 0b10101011
OR = 0b10101010
NOT = 0b01101001



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 8 registers
        self.reg = [0] * 8
        # Stack pointer - reg 7 per spec
        self.reg[7] = 0xf4
        # Point counter
        self.pc = 0
        # Memory with 256 bits
        self.ram = [0b0] * 256
        self.running = True
        self.address = 0
        self.flag = 0b00000000
        # branch_table
        self.branch_table = {
            ADD: self.ADD,
            CALL: self.CALL,
            CMP: self.CMP,
            HLT: self.HLT,
            JEQ: self.JEQ,
            JMP: self.JMP,
            JNE: self.JNE,
            LDI: self.LDI,
            MUL: self.MUL,
            NOP: self.NOP,
            POP: self.POP,            
            PRN: self.PRN,
            PUSH: self.PUSH,
            RET: self.RET,
            SUB: self.SUB,
            MOD: self.MOD,
            SHL: self.SHL,
            SHR: self.SHR,
            XOR: self.XOR,
            OR: self.OR,
            NOT: self.NOT
        }

    def load(self):
        """Load a program into memory."""

        import sys

        if len(sys.argv) != 2:
            print("usage: comp.py progname")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    temp = line.split()

                    if len(temp) == 0:
                        continue
                        
                    if temp[0][0] == "#":
                        continue

                    try:
                        self.ram[self.address] = int(temp[0], 2)

                    except ValueError:
                        print(f"Invlaid number: {temp[0]}")
                        sys.exit(1)

                    self.address += 1

        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)

        if self.address == 0:
            print('Program was empty!')
            sys.exit(3)


    'Create handles for each method in branch_table'

    def HLT(self, operand_a = None, operand_b= None):
        # Turn running to false
        self.running = False

    def LDI(self, operand_a = None, operand_b = None):
        # Set the value of a register to an integer
        self.reg[operand_a] = operand_b

    def PRN(self, operand_a = None, operand_b = None):
        # Print the value stored in the given register
        print(self.reg[operand_a])

    def MUL(self, operand_a = None, operand_b = None):
        # Multiply the two values - handled by alu
        self.alu("MUL", operand_a, operand_b)

    def SUB(self, operand_a = None, operand_b = None):
        # Subtract the two values - handled by alu
        self.alu("SUB", operand_a, operand_b)

    def ADD(self, operand_a = None, operand_b = None):
        # Add the two values - handled by alu
        self.alu("ADD", operand_a, operand_b)

    def CMP(self, operand_a = None, operand_b = None):
        # Comparison of the two values - handled by the alu
        self.alu('CMP', operand_a, operand_b)

    def PUSH(self, operand_a = None, operand_b = None):
        # Decement the sp
        self.reg[7] -= 1
        # Get value in given register
        value = self.reg[operand_a]
        # Store it at the top of the stack
        self.ram[self.reg[7]] = value

    def POP(self, operand_a = None, operand_b = None):
        # Copy value from the sp reg
        value = self.ram[self.reg[7]]
        # Store it in the given register
        self.reg[operand_a] = value
        # Increment the sp by 1
        self.reg[7] += 1

    def CALL(self, operand_a = None, operand_b = None):
        # Address we want to come back to after the call
        ret_addr = self.pc +2
        # Push return address to stack
        self.reg[7] -= 1
        self.ram[self.reg[7]] = ret_addr
    
        # Call the subroutine (function calls)
        # PC +1 will tell us which register to look at that holds the function to call
        reg_num = self.ram[operand_a]
        self.pc = self.reg[reg_num]

    def RET(self, operand_a = None, operand_b = None):
        # Pop the retrun addr off the stack
        ret_addr = self.ram[self.reg[7]]
        # Increment the sp
        self.reg[7] +=1
        # Set the PC to it
        self.pc = ret_addr

    def NOP(self, operand_a = None, operand_b = None):
        # No operation, do nothing
        pass
    
    def JMP(self, operand_a = None, operand_b = None):
        # jump to the address stored in the given register
        self.pc = self.reg[operand_a]


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # Add the value in two registers and store the result in registerA
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        # Compare the values in two registers
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            else:
                self.flag = 0b00000000


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
        
        while self.running:
            # Set the instruction register using the point counter
            ir = self.ram[self.pc]
            # save the next two operands; some programs will use them
            operand_a = self.ram[self.pc +1]
            operand_b = self.ram[self.pc +2]

            if ir in self.branch_table:
                self.branch_table[ir](operand_a, operand_b)

            # Catch-all
            else:
                self.pc += 1
                print(f"Unknown instruction {ir} at address {self.pc}")
                sys.exit(1)

            # If the 5th digit is a 1, then don't automatically set the pc
            # Mask everything but the digit we are interested in
            if ir & 0b00010000 == 0:
                # print(f'Setting PC for ir: {ir}')
                # Read the number of arguments from the program byte, 
                # increment the pc from that info

                # Shift the ir to the right 6 to leave just the two bits telling the num of arguments 
                number_of_arguments = ir >> 6
                # Add 1 to account for the first instruction (plus the two arguments)
                size_of_this_instruction = number_of_arguments + 1
                # Adjust the pc accordingly
                self.pc += size_of_this_instruction
            # else:
                # print('not resetting the pc')

    def ram_read(self, address):
        """Accept the address to read and return the value stored there"""
        return self.ram[address]

    def ram_write(self, address, value):
        """Accept a value to write and the address to write it to"""
        self.ram[address] = value
    

