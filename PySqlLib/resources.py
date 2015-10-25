'''
Created on Oct 17, 2015

@author: rahul.bhartari
'''
import sys
import os
from PySqlLib.constdata import *
from io import *

class pyTable:
    def __init__(self,name,column_dict,):
        '''
        {column_name:[type_code,constraint_name,constraint_code,condition_string]}
        '''
        self.name = name
        self.column_dict = column_dict
        

class pyDB:
    def __init__(self,name,file):
        self.name=name
        self.file=file
        self.tlist=[]
        #to be completed

class pySQL:
    '''
    Top level class for database SQL interpreter
    Direct Subclasses are the following:
        > class pyData
        > class Resources
        > pyOperations
        > class FileIO
    '''
    #private static variables
    __name = "pySQL Database Manager"
    __version="1.0"
    #public static variables
    #supported set of commands
    cmd_set=("EXIT","CREATE","INSERT","DELETE","UPDATE","SELECT","LOGIN","ACTIVE","EXECUTE","DUMMY",\
          "INT","STRING","FILE","FOREIGN","KEY","PRIMARY","UNIQUE",\
          "TABLE","INTO","VALUES","RENAME","FROM","USER","PASS","ADMIN","GROUP","DATABASE","IN",\
          "ID","NAME","VERSION","OWNER","DETAILS","ENTITY","DATA","TYPE","CTIME","DML",\
          "WHERE","SET","LIKE","DISTINCT","ALL","TO","ON",\
          "UNION","INTERSECT","FULLOUTJOIN","LEFT","INJOIN","RIGHT","OUTJOIN","PRODUCT",\
          "NULL","DEBUG",\
          "AND","OR","NOT","BETWEEN","EQUALS","GREATER","SMALLER","NOTEQUAL","ADD","SUB","DIV","MUL","MOD",\
          "AVG","CNT","SUM","XOR","VER",\
          "REFERENCES","CHECK","CONSTRAINT","DROP","ALTER","TRUNCATE","GRANT","REVOKE","COMMIT","ROLLBACK")
    cmd_codes = cmdCodes()
    #constructor: initialize private instance variables
    def __init__(self, io_source,db_list,user):
        self.__io_source = io_source    #select input source: file(script) or console mode
        self.__db_list = db_list        #dictionary of available databases(objects) for current user
        self.__current_user = user      #current user
        self.__debug_mode = 0           #debug mode
        self.__input_file=None       #input script file object
        self.cstack = cStack(200,None)  #command stack

    def get_io_source(self):
        return self.__io_source
    def get_db_list(self):
        return self.__db_list
    def get_current_user(self):
        return self.__current_user
    def get_debug_mode(self):
        return self.__debug_mode
    def get_input_file(self):
        return self.__input_file

    def set_io_source(self, value):
        self.__io_source = value
    def set_db_list(self, value):
        self.__db_list = value
    def set_current_user(self, value):
        self.__current_user = value
    def set_debug_mode(self, value):
        self.__debug_mode = value
    def set_input_file(self,file):
        self.__input_file=file

    #initialize the input source
    #according to the command line arguments
    #arguments in order module_name, file_name,debug_mode
    def py_dbinit(self):
        #get the command line arguments
        cmdargs = sys.argv
        if len(cmdargs)==2:
            try:
                self.__debug_mode=int(cmdargs[1])
            except:
                try:
                    self.__input_file = open(cmdargs[1],'r')
                    self.__io_source= self.cmd_codes.FILE_INPUT
                except:
                    print("Error in arguments")
                    print("Running in Default Mode")
                    return False
        elif len(cmdargs)==3:
            try:
                self.__input_file = os.open(cmdargs[1], 'r')
                self.__debug_mode=int(cmdargs[2])
                self.__io_source = self.cmd_codes.FILE_INPUT
            except:
                print("Error in arguments")
                print("Running in Default Mode")
                return False
        else:
            return False
        print(cmdargs)
        return True


class pyResources(pySQL):
    
    def __init__(self):
        super().__init__(self.cmd_codes.CONSOLE_INPUT,None,None)

    def get_command(self,cstr):
        try:
            return self.cmd_set.index(cstr)
        except:
            return self.cmd_codes.ERR_NOT_FOUND

    def search(self,file,string):
        tmp=""
        c_off=file.tell()
        file.seek(0,SEEK_END)
        f_sz=file.tell()
        file.seek(c_off,SEEK_SET)
        while True:
            ch=file.read(1)
            #print('ch:'+ch)
            if ch == string[0]:
                if file.tell()+len(string)-1>f_sz:
                    print("Not found")
                    break
                tmp=ch+file.read(len(string)-1)
                if tmp==string:
                    c_off=file.tell()-len(string)
                    return c_off
                file.seek(file.tell()-len(string)+1,SEEK_SET)
        file.seek(c_off,SEEK_SET)
        return -1

    def get_tables(self,database_file):
        pass

 
'''
cStack class:
class for providing stack and related operations
pop operation is destructive in nature, i.e., item on the top will be lost after pop operation
'''
class cStack(pyResources):
    def __init__(self,max_size,dlist):
        self.__max_size = max_size      #maximum size of the stack
        self.__top = -1                 #stack top: index of the item at the top
        self.__elements = []            #elements in the stack
        if dlist!=None:
            try:
                if len(dlist)>0:
                    self.__elements+=dlist
            except:
                print("Error in constructor inputs")

    #returns true if stack is empty, else returns false
    def is_empty(self):
        if self.__top==-1:
            return True
        return False

    #returns true if stack reaches its max_size limit, else returns false
    def is_full(self):
        if self.__top==self.__max_size-1:
            return True
        return False

    #pops the element on the top the stack and returns the popped element,else returns the error code
    def pop(self):
        if self.is_empty()==True:
            raise EX_STACK_EMPTY
        self.__top-=1
        return self.__elements.pop()

    #pushes the data into the stack and returns None, else returns error code
    def push(self,data):
        if self.is_full()==True:
            raise EX_STACK_FULL
        self.__top+=1
        self.__elements.append(data)
        return None

    #increment can be positive( to increase he size) or negative(to decrease the size)
    def set_max_size(self,size):
        if size>-1:
            self.__max_size=size

    #increments or decrements the max size of the stack if possible, returns max size or error code if not possible
    def alter_size(self,increment):
        if self.__max_size+increment > self.__top+1:
            self.__max_size+=increment
            return self.__max_size
        raise EX_STACK_SIZE

    #searches for a particular key in the stack elements and returns the index of the element in the stack, else returns -1
    def search(self,key):
        cnt=0
        while cnt<=self.__top:
            if self.__elements[cnt]==key:
                return cnt
            cnt+=1
        return -1

    #returns the list containing all the elements in the stack
    def get_list(self):
        cnt=0
        tmp = []
        while cnt<=self.__top:
            tmp.append(self.__elements[cnt])
        return tmp

    #prints the elements of the stack in the console
    def display(self):
        cnt=self.__top
        while cnt>-1:
            print(self.__elements[cnt])
            cnt-=1

    def get_max_size(self):
        return self.__max_size

    def get_top(self):
        return self.__top

    def clear(self):
        while self.is_empty()==False:
            self.pop()

'''
Linked List class:
class for providing linked list and related operations
linked list is doubly linked
'''
class dLinkedList(pyResources):

    class Node:
        def __init__(self,data):
            self.__data = data
            self.__prev = None
            self.__next = None

    def __init__(self):
        self.__length = 0
        self.__head = None
        self.__tail = None

    def is_empty(self):
        if self.__head==None:
            return True
        return False

    def insert(self,data,after_data):
        if after_data==None:
            return self.append(data)
        
        tmp=self.__head
        tnode=None
        while tmp.__next !=None:
            if tmp.__data==after_data:
                tnode = tmp.__next
                tmp.__next = self.Node(data)
                tmp.__next.__prev = tnode.__prev
                tmp.__next.__next=tnode
                return True
            tmp = tmp.__next
        print("Data could not be inserted!!")
        return False

    def append(self,data):
        n_node=self.Node(data)
        if self.__head==None:
            self.__head=n_node
            self.__tail=n_node
            return True
        n_node.__prev=self.__tail
        self.__tail.__next=n_node
        return True

    def replace(self,data,replace_data):
        if replace_data==None:
            return self.append(data)
        tmp=self.__head
        try:
            while tmp.__next !=None:
                if tmp.__data==replace_data:
                    garbage=tmp.__data
                    tmp.__data=data
                    try:
                        del(garbage)
                    except:
                        pass
                    return True
                tmp = tmp.__next
        except:
            print("Error in Replace!!")
            return False
        print("Data to be replaced not found!!")
        return False

    def delete(self,data):
        c_node=self.__head
        try:
            while c_node.__next!=None:
                if c_node.__data==data:
                    garbage=c_node
                    c_node.__prev.__next=c_node.__next
                    c_node.__next.__prev=c_node.__prev
                    try:
                        del(garbage)
                    except:
                        pass
                    return True
                c_node=c_node.__next
        except:
            print("Error in deletion!!")
        print("Nothing could be deleted!!")
        return False

    def search(self,data):
        c_node=self.__head
        try:
            while c_node.__next!=None:
                if c_node.__data==data:
                    return c_node
                c_node=c_node.__next
        except:
            print("Error in search!!")
        print("Nothing Found!!")
        return None

    def display(self):
        c_node=self.__head
        try:
            while c_node.__next!=None:
                print(c_node.__data)
                c_node=c_node.__next
        except:
            print("Error in traversal!!")

    def get_length(self):
        return self.__length

    def get_head(self):
        return self.__head

    def get_tail(self):
        return self.__tail



