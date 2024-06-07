import sys
labels={}  #dictionary for label

labeldic={} #stoes variables

errorlist=[]#stores all error

outputlist=[]#stores all machinecode

opcodes = {
    "add": "00000",
    "sub": "00001",
    "mov": "00010",
    "ld": "00100",
    "st": "00101",
    "mul": "00110",
    "div": "00111",
    "rs": "01000",
    "ls": "01001",
    "xor": "01010",
    "or": "01011",
    "and": "01100",
    "not": "01101",
    "cmp": "01110",
    "jmp": "01111",
    "jlt": "11100",
    "jgt": "11101",
    "je": "11111",
    "hlt": "11010"
}

registers = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111"
}



def labeler(mainfile,x):
    countr = x*(-1)+1
    j=1
    for temp in mainfile:

        temp_lable = temp.split()
        if temp_lable and temp_lable[0].endswith(":"):  # making sure that label is followed by :
            label = temp_lable[0][:-1]  # remove the colon from the label


            labels[label] = "$"+str(countr)
        countr += 1

def no_variable(file):
    countr = 1


    for line in file:
        words = line.split()
        if len(words) >= 2 and words[0] == "var":
            countr += 1
            for i in range(1,len(words)):

                variable_name = words[i]
                labeldic[variable_name] = "$"

        else:
            break
    return countr
def variable(file,x):
    countr = 1

    leng=len(file)-x+1
    for line in file:
        words = line.split()
        if len(words) >= 2 and words[0] == "var":
            countr += 1
            for i in range(1,len(words)):

                variable_name = words[i]
                labeldic[variable_name] = "$"+str(leng)
                leng+=1
        else:
            break
    return countr

def errordetection(line,TOTAL_lines,count,errorlist):  #temp-->single line instr, count-->no of instr,TOTAL_lines-->last instr of file
        lst=line.split()
        mlabel=lst[0]
        templ=len(mlabel)

        if(mlabel[:templ-1] in labels.keys()):
            lst.remove(lst[0])  #removing label name if already exist

        if(len(lst)==4):
            label=lst[0]
            r1=lst[1]
            r2=lst[2]
            r3=lst[3]
            if(label =="and" or label =="xor"or  label=="or"  or label=="add" or label =="mul" or label =="sub" ):
                if( r1 in registers and r2 in registers and r3 in registers  ):
                    return 1
                else :
                    errorlist.append("Inavlid register at line no"+ str(count))

            else :
                errorlist.append("Typo in instruction name on line NO "+ str(count))



        elif(len(lst)==3):
            label=lst[0]
            var1=lst[1]
            var2=lst[2]
            if( label=="rs" or label=="ls" or label=="mov"  or label=="not" or label=="ld" or label=="div" or label=="st" or label=="cmp"):
                if(var1 in registers.keys()):
                   if(label=="mov"):
                       if(( var2 in registers.keys()) or (var2[0]=="$"and 0<=int(var2[1:])<=127)):
                           return 1
                       else:
                           errorlist.append("Invalid Syntax for mov on line NO "+ str(count))

                           return 0
                   elif(label=="div" or  label=="cmp" or label=="not"):
                       if(var2 in registers.keys()):
                           return 1
                       else :
                           errorlist.append("Invalid second registers "+str(count))

                           return 0
                   elif(label=="ls" or label=="rs"):
                       if (0 <= int(var2[1:]) <= 127 and var2[0] == "$" ):
                           return 1
                       else:
                           errorlist.append("Invalid value for ls and rs type instruction on line NO "+str(count))

                   elif(label=="st" or label=="ld"):
                       if(var2 in labeldic.keys()): #checking if mem_add is correct binary
                           return 1
                       else :
                           errorlist.append("Invalid variable on line NO "+str(count))

                           return 0
                else:
                    errorlist.append("invalid registers instruction on line NO "+str(count))

            else:
                errorlist.append("Invalid instruction syntax on line NO "+str(count))

                return 0


        elif(len(lst)==2):
            label=lst[0]
            value=lst[1]    # making sure var is alphanumeric or _

            if( label=="je" or label=="jgt" or label=="jlt" or label=="jmp" or label=="var"):
                if(label=="var"):
                    if(value not in labeldic.keys()):
                        errorlist.append("VAR not declared at top,error on line NO "+str(count))

                    else:
                        for i in value:
                            if(i in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_"):
                                continue
                            else:
                                errorlist.append("variable name incorrect ,on line NO "+str(count))

                                return 0
                elif(  label=="je" or label=="jgt" or label =="jmp"  or label=="jlt"):
                    x=labels.keys()
                    if(value in x):
                        return 1
                    else:
                        errorlist.append("incorrect label label not declared"+str(count))

                        return 0
            else:
                errorlist.append("Typo error in instruction name,on line NO "+str(count))

                return 0

        elif(len(lst)==1):
            if(count==TOTAL_lines and lst[0]=="hlt"):  #making sure hlt is last

                return 1
            elif(count!=TOTAL_lines and lst[0]=="hlt"):
                errorlist.append("hlt is not present at last ,present at line NO "+str(count))
                return 0
            else:
                errorlist.append("invalid syntax error at line NO "+str(count))

        else:
            errorlist.append("general syntax error,on line NO "+str(count))




def d2b(num): #Converts decimal number to a binary number of 7 bits
    num=int(num[1:])
    s = bin(num).replace("0b", "")
    s = str(s)
    if len(s) < 7:
        while len(s) < 7:
            s = "0" + s

    return s


def assembler(lines):
    counter=1
    for instruction in lines:
        wordlist =instruction.split()
        templ=len(wordlist[0])
        if(wordlist[0][:templ-1] in labels):
            wordlist.remove(wordlist[0])
        if(len(wordlist)==1 and wordlist[0]=="hlt"):
            outputlist.append("1101000000000000")

            break
        else:

            if(len(wordlist)==2):
                strng=""
                if(wordlist[0]!="var"):
                    if(wordlist[0][-1]==":" and wordlist[1]=="hlt"):

                        outputlist.append("1101000000000000")

                    else:
                        strng=""
                        strng+=opcodes[wordlist[0]]+"0000"
                        Str2=d2b(str(labels[wordlist[1]]))
                        strng+=Str2
                        outputlist.append(strng)



            elif(len(wordlist)==3):
                strng=""
                if(wordlist[0]=="mov"):
                    if(wordlist[2] in registers):
                        strng="00011"
                        strng+="00000"
                        strng+=registers[wordlist[1]]
                        strng+=registers[wordlist[2]]
                        outputlist.append(strng)
                    else:
                        strng=opcodes[wordlist[0]]
                        strng+="0"
                        strng+=registers[wordlist[1]]
                        Str2=d2b(wordlist[2])

                        strng+=Str2
                        outputlist.append(strng)

                elif wordlist[0] in {"div", "cmp", "not"}:
                    strng=""
                    strng+=opcodes[wordlist[0]]
                    strng+="00000"
                    strng+=registers[wordlist[1]]
                    strng+=registers[wordlist[2]]
                    outputlist.append(strng)
                elif wordlist[0] in {"ld", "st",}:
                    strng=""
                    strng+=opcodes[wordlist[0]]
                    strng+="0"
                    strng+=registers[wordlist[1]]
                    Str2=d2b(labeldic[wordlist[2]])
                    strng+=Str2
                    outputlist.append(strng)
                elif wordlist[0] in {"rs", "ls"}:
                    strng=""
                    strng+=opcodes[wordlist[0]]
                    strng+="0"
                    strng+=registers[wordlist[1]]
                    Str2=d2b(wordlist[2])
                    strng += Str2
                    outputlist.append(strng)
            elif(len(wordlist)==4):
                strng=""
                strng+=opcodes[wordlist[0]]
                strng+="00"
                strng+=registers[wordlist[1]]
                strng+=registers[wordlist[2]]
                strng+=registers[wordlist[3]]
                outputlist.append(strng)
        counter+=1


def main():
    

    mainfile=[]
    extra=[]
    for line in sys.stdin:
            extra.append(line)
    for line in extra:
        if(line!="" or line!="\n"):
            mainfile.append(line)

    xx=mainfile[-1].split()



    flag=1

    x=no_variable(mainfile)
    variable(mainfile,x)

    labeler(mainfile,x)


    counter=1
    if(len(mainfile)<=128+x-1):
        for line in mainfile:
            if (counter>128):
                break
            else:
                flag=errordetection(line,len(mainfile),counter,errorlist)
                counter+=1

        dell=mainfile[-1].strip()
        # print(dell[len(dell)-3:])
        if(dell[len(dell)-3:]!='hlt'):
            errorlist.append("hlt is missing at the end")

        # if(xx[0].strip()!="hlt" or xx[1].strip()!="hlt" ):
            # errorlist.append("hlt is missing at the end")


        if(len(errorlist)>0):
            for i in errorlist:
                print(i)


        else:
            assembler(mainfile)
            for i in outputlist:
                print(i)

    else:
        print("NO OF INSTRUCTIONS EXCEED 128")



if __name__=="main_":
    main()