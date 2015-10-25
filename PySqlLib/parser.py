'''
Created on Oct 5, 2015

@author: rahul.bhartari
'''
from PySqlLib.constdata import *
from PySqlLib.resources import *

class pyCMD:
    def __init__(self,cmd_code,info):
        self.__cmd_code = cmd_code
        self.__info = info
        #every information related to the particular command is to be added

class pyParser(pyResources):
    def __init__(self):
        super().__init__()

    #Get input from console
    #Create a command string which MUST end with ';' character
    def __get_cinput(self):
        cmdstr = input("$>")
        if cmdstr[len(cmdstr)-1]!=';':
            cmdstr+=' '+self.__get_cinput()
        return cmdstr

    #Get input from a script file
    #Create a command string which MUST end with ';' character
    def __get_finput(self,_file_h):
        print("$",end='>')
        cmdstr = ""
        ch=' '
        while True:
            try:
                ch=_file_h.read(1)
                if ch=='$': # return if end of script char ('$') found
                    print(cmdstr)
                    return cmdstr
                cmdstr+=ch
                if ch==';': # return if end of command found
                    print(cmdstr)
                    return cmdstr
            except:
                print("Exception in File or Script Input")
                return None
        return None

    #Function to input command string
    #This is the input function to be called (not the above ones)
    def get_input(self):
        if self.get_io_source()==self.cmd_codes.FILE_INPUT:
            return self.__get_finput(self.__input_file)
        elif self.get_io_source()==self.cmd_codes.CONSOLE_INPUT:
            return self.__get_cinput()
        return None


    def create_stack(self,cmdstr):
        spchar = "<>,./(\\)[]{}-+=!~|%^&*@#$:;"
        tmpstk=cStack(2,None)
        tmp=""
        for i in range(len(cmdstr)):
            if cmdstr[i] not in spchar:
                if cmdstr[i]==' ':
                    try:
                        if len(tmp)>0:
                            tmpstk.push(tmp)
                    except EX_STACK_FULL:
                        #print("caught EX_STACK_FULL")
                        tmpstk.alter_size(5)#increment stack size by 5
                        tmpstk.push(tmp)
                    except:
                        print("Unexpected Stack Error!!")
                        print("Try Again!!")
                    tmp=""
                else:
                    tmp+=cmdstr[i]
            else:
                try:
                    if len(tmp)>0:
                        tmpstk.push(tmp)
                        tmp=""
                    if cmdstr[i] in "><=":
                        if cmdstr[i+1]=='=':
                            tmpstk.push(cmdstr[i]+cmdstr[i+1])
                            i+=1
                            continue
                    elif cmdstr[i]=='!':
                        if cmdstr[i+1]=='<':
                            tmpstk.push('>')
                            i+=1
                            continue
                        elif cmdstr[i+1]=='>':
                            tmpstk.push('<')
                            i+=1
                            continue
                        elif cmdstr[i+1]=='=':
                            tmpstk.push('!=')
                            i+=1
                            continue
                        else:
                            tmpstk.push(cmdstr[i])
                    else:
                            tmpstk.push(cmdstr[i])
                except EX_STACK_FULL:
                    #print("caught EX_STACK_FULL")
                    tmpstk.alter_size(5)#increment stack size by 5
                    if len(tmp)>0:
                        tmpstk.push(tmp)
                        tmp=""
                    tmpstk.push(cmdstr[i])
                except:
                    print("Unexpected Stack Error!!")
                    print("Try Again!!")
            #end-if
        #end-for
        #push in main stack so that first command is on the top of the stack
        self.cstack.clear()
        while tmpstk.is_empty()==False:
            self.cstack.push(tmpstk.pop())
        #end-while
        return self.cstack


