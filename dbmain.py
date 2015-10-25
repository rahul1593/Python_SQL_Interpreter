'''
Created on Oct 4, 2015

@author: rahul.bhartari
'''
import sys
from PySqlLib.constdata import *
from PySqlLib.parser import *
from PySqlLib.session_man import *

if __name__ == '__main__':
    pass

##DBMS initialization and infinite input loop

class dbmain(pySQL):
    def __init__(self):
        self.console = pyParser()
        self.session = None
    '''
    process_cmdstk:
    This method processes all the commands and passes the stack to the corresponding individual command processors
    '''
    def process_cmdstk(self,stk):
        cmd = self.console.get_command(stk.pop())
        if cmd == self.cmd_codes.EXIT:
            return self.cmd_codes.EXIT
        if 0<=cmd<=self.cmd_codes.code_max:
            if cmd == self.cmd_codes.LOGIN:
                self.session = Session(None)
                return self.session.login(stk)
            
            elif self.session != None:
                if cmd == self.cmd_codes.CREATE:
                    pass
                elif cmd == self.cmd_codes.DROP:
                    pass
                elif cmd == self.cmd_codes.ALTER:
                    pass
                elif cmd == self.cmd_codes.TRUNCATE:
                    pass
                elif cmd == self.cmd_codes.LOGIN:
                    pass
                elif cmd == self.cmd_codes.LOGIN:
                    pass
                elif cmd == self.cmd_codes.LOGIN:
                    pass
            else:
                print("Login First !!")
                return self.cmd_codes.ERR_UNAUTHORIZED
        pass#to be completed


    def start(self):
        # main code starts here
        print("    ________________ PySQL V-1.0 ________________")
        while True:
            tcmd=self.console.get_input()
            cstk=self.console.create_stack(tcmd)
            cstk.display()
            ret=self.process_cmdstk(cstk)
            if ret==self.cmd_codes.EXIT:
                break
        print("Exiting ^_^")
    
# start the command parser in continuous while loop
session = dbmain()
session.start()





