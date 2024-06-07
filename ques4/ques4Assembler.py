instruction=[]
registers={"FLAGS":"111","R6":"110","R5":"101","R4":"100","R3":"011","R2":"010","R1":"001","R0":"000"}
opcodes={"hlt":"11010","je":"11111","jgt":"11101","jlt":"11100","jmp":"01111","cmp":"01110","not":"01101","and":"01100","or":"01011",
        "xor":"01010", "ls":"01001","rs":"01000","div":"00111","mul":"00110","st":"00101","ld":"00100","movC":"00011","movB":"00010","sub":"00001","add":"00000","Lcm": "11000","Hcf":"10111","Power":"10100","Seq": "11001","Cub":"11110"}
file = open("co.txt", 'r')
# def remove_empty(l):
#     c = l.count('\n')
#     for i in range(c):
#         l.remove('\n')
#     return l
# # for line in sys.stdin():
#     instruction =line.strip().split()
# file.close()



instruction = file.readlines()
# print(instruction)
# for input in file.readlines():
#     input=input.strip()
#     if input!="":
#         instruction.append(input)

# file.close()
# for input in sys.stdin:
#     input=input.strip()
#     if input!="":
#         instruction.append(input)
error=''
memory_dict={}
var_dict={}

def countoccurrences(str, word):
    a = str.split()
    count = 0
    for i in range(0, len(a)):
        if (word == a[i]):
           count = count + 1
            
    return count 




def binary(num, bits=7):
    binary_string = bin(num)[2:]
    return str('{0:0>{1}}'.format(binary_string, bits))

def typing_error_register(inputline):
    global error
    error=f"typing error in register in {str(inputline)}" 

def typing_error_instruction(inputline):
    global error
    error=f"typing error in instruction in {str(inputline)}"

def general_syntax_error(inputline):
    global error
    error=f"general synatx error in {str(inputline)}"

def typeA(i, text, inputline):
    if (i[1] not in registers.keys()):
        typing_error_register(inputline)
    if (i[2] not in registers.keys()):
        typing_error_register(inputline)
    if (i[3] not in registers.keys()):
        typing_error_register(inputline)
    text= text+ "00"+registers[i[1]]+registers[i[2]]+registers[i[3]]
    return text

def typeB(i, text, inputline):
    global error
    if (i[1] not in registers.keys()):
        typing_error_register(inputline)
    # sys.stdout.write(i[2])
    if(int(i[2][1:])<0 or int(i[2][1:])>127):
        error=("Syntax Error : Immediate value out of range, line with error is : " + str(inputline))
    # sys.stdout.write(i[2])
    num = int(i[2][1:])
    # sys.stdout.write(num)
    text=text+ '0'+registers[i[1]]+binary(num)
    return text


def typeD(i, text, inputline):
    global error
    if i[1] not in registers:
        typing_error_register(inputline)
    text = text + '0' + registers[i[1]]

    if i[2] in var_dict:
        text = text + var_dict[i[2]]
    else:
        if i[2] in memory_dict:
            error=f" Error in line {str(inputline)}: No variable named {i[2]}"
        else:
            error = ("Syntax Error: Use of undefined variable, line with error is: "+str(inputline))
            return 0

    return text


def typeE(i, text, inputline):
    global error
    if(i[1] in var_dict.keys()):
        error=("Syntax Error: misuse of Variable as Label, line with error is : " + str(inputline))
        return 0
    elif(i[1] not in memory_dict.keys()):
        error=f" Error in line {str(inputline)}: No label named {i[1]}"
        return 0
    text = text+'0000'+ memory_dict[i[1]]
    return text

def typeF(i, text, inputline):
    text+='00000000000'
    return text

def typeC(i, text,inputline):
    if (i[1] not in registers.keys()):
        typing_error_register()
    if (i[1] not in registers.keys()):
        typing_error_register()
    text=text+'00000'+ registers[i[1]]+ registers[i[2]]
    return text
counter=0
for j in instruction:
    i=j.split()

    if i[0]!='var':
        break
    counter+=1
# sys.stdout.write(counter)
hltcounter=0
for i in instruction:
    hltcounter+=countoccurrences(i,"hlt")
if(hltcounter>1):
    general_syntax_error()
if (hltcounter==0):
    error=("No hlt instruction present")
    # exit() 
elif (countoccurrences(instruction[-1],"hlt")==0):
    error=("Syntax Error : hlt not being used as the last instruction")

countoutputlines=0
count_var=0

for j in instruction:
    i=j.split()
    if i[0][-1]==':':
        memory_dict[i[0][:-1]] = binary(countoutputlines)
    if i[0]!='var':
        countoutputlines+=1
    else:
        # var_dict[i[1]]=binary(+count_var)
        var_dict[i[1]]=0
        count_var+=1
c = (len(instruction)-count_var)
for i in var_dict.keys():
    var_dict[i]=binary(c)
    c=c+1
inputline=0
binarygeneratedcode=[]
with open("machinecode.txt", 'w') as f:
    f.close()
for j in instruction:
    inputline+=1
    i=j.split()
    text=''
    if i[0]!='var':

        if (i[0][-1]==':'):
            i.remove(i[0])
        if 'FLAGS' in i and i[0]!='mov':    # flag register name is FLAGS
                error(f"Illegal use of flag register, line with error is : {str(inputline)}")
                break
                
        if (i[0]=='mov'):
            if(i[2][0]=='R' or i[2]=='FLAGS'):
                i[0]='movC'
            else:
                i[0]='movB'
        if i[0] in opcodes.keys():
            text+=opcodes[i[0]]
        else:
            typing_error_instruction(inputline)
            break

        if i[0]=='add' or i[0]=='mul' or i[0]=='sub' or i[0]=='xor' or i[0]=='or' or i[0]=='and' or i[0]=='Lcm' or i[0]=='Hcf' or i[0]=='Power':
            if len(i)!=4:
                general_syntax_error(inputline)
            text=typeA(i, text, inputline)
            binarygeneratedcode.append(text)

        elif ((i[0]=='movB' and i[2][0]=='$') or i[0]=='rs' or i[0]=='ls'):
            if len(i)!=3:
                general_syntax_error(inputline)
            text = typeB(i, text, inputline)
            binarygeneratedcode.append(text)
        elif (i[0]=='movC') or i[0]=='div' or i[0]=='cmp' or i[0]=='not' or i[0]=='Seq' or i[0]=='Cub':
            if len(i)!=3:
                general_syntax_error(inputline)
            text=typeC(i, text, inputline)
            binarygeneratedcode.append(text)
        elif (i[0]=='ld') or i[0]=='st':
            if len(i)!=3:
                general_syntax_error(inputline)
            text = typeD(i, text, inputline)
            binarygeneratedcode.append(text)
        elif i[0]=='jmp' or i[0]=='jlt' or i[0]=='jgt' or i[0]=='je':
            if len(i)!=2:
                general_syntax_error(inputline)
            text=typeE(i, text, inputline)
            binarygeneratedcode.append(text)
        elif i[0]=='hlt':
            if len(i)!=1:
                general_syntax_error(inputline)
            text=typeF(i, text, inputline)
            binarygeneratedcode.append(text)
    else:
        if inputline<=counter:
            pass
        else:
            error="variables must be declared at the beginning"
with open("machinecode.txt", 'a') as f:
    if (error==""):
        for k in binarygeneratedcode:
            f.write(f"{k}")
            f.write("\n")
    else:
        f.write(error)
# if error=="":
#     for i in binarygeneratedcode:
#         sys.stdout.write(i+"\n")
# else:
#     sys.stdout.write(error+"\n")