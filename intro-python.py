#this is how you decalre a variable
#and input something to it
name = input('What\'s ypur name?')
# YOu can concatenate strings
print('Hello world!' + name + '!')
#but it is nicer to use string interpolation
print(f'Hello {name}!')

# If...elif...else
if name == 'Python':
    print ('You are the best language')
elif name == 'Java':
    print ('You are a very structured lanuguage!')
else:
    print(f'{name} is a nice name')

#Ternary operator
# different from java and most other languages
# in java: condition ? [value if true] : [value if false]
# in python [value if true] if condition else [value if false]
print ('You are the great' if name == 'Python' else 'you are ok!')

    # There are not traditional for loop
    # but here is the equivalent of for(i = 1; i <= 10; i++)
for i in range(1, 11): 
    # optional: print(i, end=' ') # with spaces instead of line feed
    print(i)
   

counter = 1
while counter <= 10:
    print(counter)
    counter += 1