import sys
registers = {
    "111": "FLAGS",
    "110": "R1",
    "101": "R5",
    "100": "R4",
    "011": "R3",
    "010": "R2",
    "001": "R1",
    "000": "R0"
}

register_value = {
    "PC": 0,
    "R0": "0000000000000000",
    "R1": "0000000000000000",
    "R2": "0000000000000000",
    "R3": "0000000000000000",
    "R4": "0000000000000000",
    "R5": "0000000000000000",
    "R6": "0000000000000000", 
    "FLAGS": "0000000000000000"   
     # Program Counter
}

memory_address = {}

opcodes = {
    "hlt": "11010",
    "je": "11111",
    "jgt": "11101",
    "jlt": "11100",
    "jmp": "01111",
    "cmp": "01110",
    "not": "01101",
    "and": "01100",
    "or": "01011",
    "xor": "01010",
    "ls": "01001",
    "rs": "01000",
    "div": "00111",
    "mul": "00110",
    "st": "00101",
    "ld": "00100",
    "movC": "00011",
    "movB": "00010",
    "sub": "00001",
    "add": "00000"
}

def add(bits):
    r1 = int(str(register_value[registers[bits[7:10]]]), 2)
    r2 = int(str(register_value[registers[bits[10:13]]]), 2)
    r3 = int(str(register_value[registers[bits[13:16]]]), 2)
    r1 = r2 + r3
    if r1 > 2**16-1:
        register_value["R1"] = "0000000000000000"
        register_value["FLAGS"] = "0000000000001000"   
    else :
        register_value[registers[bits[7:10]]] = format(r1, '016b') 
        register_value["FLAGS"] = "0000000000000000"    
    

def sub(bits):
    r1 = int(str(register_value[registers[bits[7:10]]]), 2)
    r2 = int(str(register_value[registers[bits[10:13]]]), 2)
    r3 = int(str(register_value[registers[bits[13:16]]]), 2)
    r1 = r2 - r3
    if r1 < 0:
        register_value["R1"] = "0000000000000000"
        register_value["FLAGS"] = "0000000000001000"   
    else :
        register_value[registers[bits[7:10]]] = format(r1, '016b') 
        register_value["FLAGS"] = "0000000000000000"

def mul(bits):
    r1 = int(str(register_value[registers[bits[7:10]]]), 2)
    r2 = int(str(register_value[registers[bits[10:13]]]), 2)
    r3 = int(str(register_value[registers[bits[13:16]]]), 2)
    r1 = r2 * r3
    if r1 > 2**16-1:
        register_value["R1"] = "0000000000000000"
        register_value["FLAGS"] = "0000000000001000"   
    else :
        register_value[registers[bits[7:10]]] = format(r1, '016b') 
        register_value["FLAGS"] = "0000000000000000"

def XOR(bits):
    r1 = int(str(register_value[registers[bits[7:10]]]), 2)
    r2 = int(str(register_value[registers[bits[10:13]]]), 2)
    r3 = int(str(register_value[registers[bits[13:16]]]), 2)
    r1 = r2 ^ r3
    register_value[registers[bits[7:10]]] = format(r1, '016b')
    register_value["FLAGS"] = "0000000000000000"

def OR(bits):
    r1 = int(str(register_value[registers[bits[7:10]]]), 2)
    r2 = int(str(register_value[registers[bits[10:13]]]), 2)
    r3 = int(str(register_value[registers[bits[13:16]]]), 2)
    r1 = r2 | r3
    register_value[registers[bits[7:10]]] = format(r1, '016b')
    register_value["FLAGS"] = "0000000000000000"

def AND(bits):
    r1 = int(str(register_value[registers[bits[7:10]]]), 2)
    r2 = int(str(register_value[registers[bits[10:13]]]), 2)
    r3 = int(str(register_value[registers[bits[13:16]]]), 2)
    r1 = r2 & r3
    register_value[registers[bits[7:10]]] = format(r1, '016b')
    register_value["FLAGS"] = "0000000000000000"

def move_imm(bits):
    r1 = registers[bits[6:9]]
    imm = bits[9:]
    register_value[r1] = format(int(imm, 2), '016b')
    register_value["FLAGS"] = "0000000000000000"

def right_shift(bits):
    r1 = registers[bits[6:9]]
    shift_val = int(bits[9:], 2)
    register_value[r1] = format(int(register_value[r1], 2) >> shift_val, '016b')
    register_value["FLAGS"] = "0000000000000000"
def left_shift(bits):
    r1 = registers[bits[6:9]]
    shift_val = int(bits[9:], 2)
    register_value[r1] = format(int(register_value[r1], 2) << shift_val, '016b')
    register_value["FLAGS"] = "0000000000000000"
def move_reg(bits):
    r1 = registers[bits[10:13]]
    r2 = registers[bits[13:16]]
    register_value[r1] = register_value[r2]
    register_value["FLAGS"] = "0000000000000000"
def div(bits):
    r1 = int(register_value[registers[bits[7:10]]], 2)
    r2 = int(register_value[registers[bits[10:13]]], 2)
    
    if r2 != 0:
        register_value["R0"] = format(r1//r2, '016b')
        register_value["R1"] = format(r1%r2, '016b')
        register_value["FLAGS"] = "0000000000000000"
    else:
        register_value["R0"] = format(0, '016b')
        register_value["R1"] = format(0, '016b')
        register_value["FLAGS"] == "0000000000001000"

def invert(bits):
    r1 = registers[bits[10:13]]
    r2 = registers[bits[13:16]]
    register_value[r1] = format(~int(register_value[r2], 2) & 0xFFFF, '016b')
    register_value["FLAGS"] = "0000000000000000"

def compare(bits, ):
    r1 = int(register_value[registers[bits[10:13]]], 2)
    r2 = int(register_value[registers[bits[13:16]]], 2)
    if r1 < r2:
        register_value["FLAGS"] = "0000000000000100"
        # jump_less(bits) # Set less-than flag
    elif r1 > r2:
        register_value["FLAGS"] = "0000000000000010" 
        # jump_greater(bits)# Set greater-than flag
    else:
        register_value["FLAGS"] = "0000000000000001"
        # jump_equal(bits)# Set equal flag

def load(bits):
    r1 = registers[bits[6:9]]
    address = int(bits[9:], 2)
    register_value[r1] = memory_address.get(address, "0000000000000000")
    register_value["FLAGS"] = "0000000000000000"
    

def store(bits):
    r1 = registers[bits[6:9]]
    address = int(bits[9:], 2)
    memory_address[address] = register_value[r1]
    register_value["FLAGS"] = "0000000000000000"
    

def uncondition(bits):
    decimal = int(bits[9:], 2)
    register_value["PC"] = decimal
    register_value["FLAGS"] = "0000000000000000"
    

def jump_less(bits):
    decimal = int(bits[9:], 2)
    if register_value["FLAGS"] == "0000000000000001":
        register_value["PC"] = decimal
        register_value["FLAGS"] = "0000000000000000"
    else:
        register_value["FLAGS"] = "0000000000000000"
        register_value["PC"] += 1
        
        
def jump_greater(bits):
    decimal = int(bits[9:], 2)
    if register_value["FLAGS"] == "0000000000000010":
        register_value["PC"] = decimal
        register_value["FLAGS"] = "0000000000000000"
    else:
        register_value["FLAGS"] = "0000000000000000"
        register_value["PC"] += 1
        
   

def jump_equal(bits):
    decimal = int(bits[9:], 2)
    if register_value["FLAGS"] == "0000000000000001":
        register_value["PC"] = decimal
        register_value["FLAGS"] = "0000000000000000"
    else:
        register_value["FLAGS"] = "0000000000000000"
        register_value["PC"] += 1
        
   
def printing(dict):
    for i in dict:
        if(i=="PC"):
            print(format(dict["PC"], '07b')+"        ",end='')
        else:
            print(dict[i]+" ",end='') 
    print('')
    
def halt():
    register_value["FLAGS"] = "0000000000000000"
    printing(register_value)       
    exit()

def print_memory_address(l0):
    n = 128 - len(l0)
    l1 = ["0000000000000000" for _ in range(n)]
    lf = l0 + l1
    # print(lf)
    for i in lf:
        print(i)
    
        

def decode_binary_instruction(binary_instruction):
    
    opcode = binary_instruction[:5]
    if opcode == "00001":        
        sub(binary_instruction)
        printing(register_value) 
        # print("\n")      
        register_value["PC"] += 1
        
        
    elif opcode == "00000":
        add(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "00110":
        mul(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "01010":
        XOR(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "01011":
        OR(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "01100":
        AND(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "00010":
        move_imm(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "01000":
        right_shift(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "01001":
        left_shift(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "00011":
        move_reg(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "00111":
        div(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode =="01101":
        invert(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "01110":
        compare(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "00100":
        load(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "00101":
        store(binary_instruction)
        printing(register_value)
        # print("\n")
        register_value["PC"] += 1
        
    elif opcode == "01111":
        print(format(register_value["PC"], '07b')+"        ",end='')
        uncondition(binary_instruction)
        for i in register_value:
            if(i!="PC"):
                print(register_value[i]+" ",end='') 
        print("")
        # register_value["PC"] += 1
        
    elif opcode == "11100":
        # print(register_value["PC"])
        print(format(register_value["PC"], '07b')+"        ",end='')
        jump_less(binary_instruction)
        for i in register_value:
            if(i!="PC"):
                print(register_value[i]+"          ",end='')
        print("")
        
        # register_value["PC"] += 1
    elif opcode == "11101":
        # register_value["PC"] += 1
        # print(register_value["PC"])
        print(format(register_value["PC"], '07b')+"        ",end='')
        jump_greater(binary_instruction)
        for i in register_value:
            if(i!="PC"):
                print(register_value[i]+" ",end='')
        print("")
        
    elif opcode == "11111":
        # print(register_value["PC"])
        print(format(register_value["PC"], '07b')+"        ",end='') 
        jump_equal(binary_instruction)
        for i in register_value:
            if(i!="PC"):
                print(register_value[i]+" ",end='')
        # register_value["PC"] += 1
        print("")
        
    else :
        exit()
    
instructions = []
for input in sys.stdin:
    input=input.strip()
    if input!="":
        instructions.append(input)
# with open("machinecode.txt", "r") as file:
#     instructions = [line.strip() for line in file.readlines()]
    # print(instructions)
while(instructions[register_value["PC"]][:5]!='11010' ):
    decode_binary_instruction(instructions[register_value["PC"]])
printing(register_value)
print_memory_address(instructions)
    # for i in instructions:
        # opcode = i[:5]
        # if opcode != '11010':
        # else :
    # printing(register_value)
            # break
