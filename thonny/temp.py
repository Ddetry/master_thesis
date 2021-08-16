a = 2
b = 3
c = 4

print(a, b, c)
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







			






