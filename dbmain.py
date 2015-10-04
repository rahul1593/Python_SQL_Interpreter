#   Main File for Database startup
#   Contains code for database shell
#
#   Author: Rahul Bhartari
#

# Function to get input from the console
# Returns a command string
def py_get_input():
  cmd = input("$>")
  if cmd[len(cmd)-1]!=';':
    cmd+=' '+py_get_input()
  return cmd

# function which will process the command string (not list)
def process_cmd(cmd):
  cmdstk = []         # empty list to store commands in a stack
  




# SELECT * FROM F3,F1 WHERE F1.name==F3.name
