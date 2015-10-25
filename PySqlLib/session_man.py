'''
Created on Oct 18, 2015

@author: rahul.bhartari
'''
from PySqlLib.resources import *
from PySqlLib.constdata import *
import os

class Session(pyResources):
    '''
    Session Manager Class
    Provide login functionality and define accessibility for each user.
    Store authorized databases list in form of dictionary-{db_path/name:db_file_object}
    '''
    __default_keystore = "./pyddkst.ks"
    def __init__(self, keystore):
        self.__user = None                      #string
        self.__authorized_databases_d = dict()  #dictionary{string:file_object}
        self.__current_database = None          #string
        self.__keystore_file_path=self.__default_keystore#string
        self.__keystore_file=None               #file object
        if keystore != None:
            self.__keystore_file_path=keystore
        try:
            if os.access(self.__keystore_file_path, os.F_OK)==True:
                self.__keystore_file = open(self.__keystore_file_path,'r+')
            else:
                self.__keystore_file = open(self.__keystore_file_path,'w+')
        except:
            raise EX_INTERNAL_FILE

    def get_user(self):
        return self.__user

    def __check_user(self,username,password):
        '''
        find position of user_name in key_store file
        check the password, if matches then return the list of authorized databases
        key_store format: $user_name:password:adb1,adb2,adb3
        '''
        alpl = "qwertyuiopasdfghjklzxcvbnm@_#:0123456789"
        #print("searching")
        cur_pos=self.search(self.__keystore_file, '$'+username)
        self.__keystore_file.seek(cur_pos+len(username)+2)
        #print("found")
        if cur_pos<0:
            raise EX_NOT_FOUND
        tmp=""
        while True:
            ch=self.__keystore_file.read(1)
            if ch not in alpl:
                #print(ch,"break")
                break
            tmp+=ch
            #print(ch)
        tmp=tmp.split(':')
        if tmp[0]==password:
            try:
                dbl=tmp[1].split(',')
                return dbl
            except IndexError:
                print("__check_user: No Databases")
            except:
                print("__check_user: Exception Here!!")
            return None
        raise EX_NOT_FOUND

    def __set_authorized_databases(self,dbfile_list):
        '''
        check the availability of authorized databases list
        if available, then open the database file and populate the authorized databases dictionary in Session
        Update attributes in pySQL class
        '''
        if dbfile_list != None:
            for db in dbfile_list:
                if os.access(db,os.F_OK|os.R_OK|os.W_OK)==True:
                    self.__authorized_databases_d[db]=open(db,'r+b')
        self.set_db_list(self.__authorized_databases_d)
        return

    def login(self,cstk):
        '''
        input: cstk: user_name PASS password
        > validate command
        > check user_name-password
        > set the list of authorized databases
        '''
        try:
            if self.get_command(cstk.pop())!=self.cmd_codes.USER:
                return self.cmd_codes.ERR_UNKNOWN_COMMAND
            username = cstk.pop()
            if self.get_command(cstk.pop())!=self.cmd_codes.PASS:
                return self.cmd_codes.ERR_UNKNOWN_COMMAND
            password = cstk.pop()
            if password==';':
                return self.cmd_codes.ERR_UNKNOWN_APPLICATION
            self.__set_authorized_databases(self.__check_user(username,password))
            self.__user = username
            self.set_current_user(username)
        except Exception as msg:
            print("Error: Invalid Login!!")
            #print(msg)
            return self.cmd_codes.ERR_UNAUTHORIZED
        print("Logged in User:",self.get_current_user())
        return self.cmd_codes.NULL






