'''
Created on Oct 4, 2015

@author: rahul.bhartari
'''
import sys
from PySqlLib.constdata import *
from PySqlLib.parser import *

if __name__ == '__main__':
    pass

##DBMS initialization and infinite input loop

class dbmain(pySQL):
    def __init__(self):
        self.console = pyParser()

    def process_cmdstk(self,stk):
        return self.cmd_codes.EXIT

    def start(self):
        # main code starts here
        print("    ________________ PySQL V-1.0 ________________")
        while True:
            tcmd=self.console.get_input()
            cstk=self.console.create_stack(tcmd)
            if self.process_cmdstk(cstk)==self.cmd_codes.EXIT:
                break
        print("Exiting ^_^")
    
# start the command parser in continuous while loop
session = dbmain()
session.start()

