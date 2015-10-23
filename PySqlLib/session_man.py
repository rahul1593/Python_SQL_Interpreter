'''
Created on Oct 18, 2015

@author: rahul.bhartari
'''
from PySqlLib.resources import pySQL

class Session(pySQL):
    '''
    Session Manager Class
    Provide login functionality and define accessibility for each user.
    Store the user-names and passwords in the form of integer hash values
    '''
    def __init__(self, keystore):
        self.keystore_file_obj=keystore
        self.current_user=None
        self.available_databases=None
        self.current_database=None
    
    def __check_user(self,username):
        #returns the hash value for the password of the user if available else raises an exception
        pass


    def __set_authorized_databases(self,username):
        pass

    def login(self,username,password):
        '''
        > check user-name
        > check password
        > set the list of authorized databases
        '''
        try:
            userpasshash=self.__check_user(username)
            if userpasshash == hash(password):
                self.__set_authorized_databases(username)
        except:
            return None
        return 1






