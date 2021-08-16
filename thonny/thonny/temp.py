c = [1,2,3]
n = [4,5]
c.append(n)

def play_with_list():
    c.append(7)
    c.append([3,5])
    c.pop(1)

play_with_list()
    
def exchange_in_list(mylist, i, j):
    a = mylist[i]
    mylist[i] = mylist[j]
    mylist[j] = a

exchange_in_list(c, 0, 3)
    
class Node:
    def __init__(self, dataval):
        self.next = None
        self.dataval = dataval

x = 2
n1 = Node([1,2,3])
n2 = Node(x)
n1.next = n2
n3 = Node(3)
n2.next = n3


al = [n1,n2,n3]

mylist = [n1, n2, n3]
mydict = {'x':n1, 'b':n2, 'y':n3}

ls = ["salut", "bonjour"]

d = 1
e = 2
f = 3
g = {"first", "second", "third"}
h = (1,[1,2],3)

first = Node(0)

def create_linked_list(n):
    cur = first
    for i in range(1,n):
        newNode = Node(i)
        cur.next = newNode
        cur = cur.next

create_linked_list(3)
        

        
        
        
import types

def is_personal_object(item, myvalue):
        if(item != list and item != int and item != tuple and item != float and item != str and item != bool and item != dict and item != set ):
            #if(isinstance(myvalue, types.FunctionType) != True and isinstance(myvalue, types.ModuleType) != True):
            return True
            
        else:
            return False


all_vars = []
all_variables = dir()

def myloop():
    for name in all_variables:
        # Print the item if it doesn't start with '__'
        if not name.startswith('__'):
            myvalue = eval(name)
            if(is_personal_object(type(myvalue), myvalue)):
            	if(isinstance(myvalue, types.FunctionType) or isinstance(myvalue, types.ModuleType)):
            		continue
            	else:
            		all_vars.append((name, myvalue, vars(myvalue)))	

            else:
            	all_vars.append((name, myvalue))







			






