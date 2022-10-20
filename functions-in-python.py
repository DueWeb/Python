# A definition of a function with on argument, namethat has a default value 'jane doe'
# that will be used if someone calls the function without the argument
def say_hello(name='jane doe'):
    return f'Hello {name}!'

    print(say_hello('Anna'))
    print(say_hello('Beata'))
    print(say_hello()) # Prints 'jane doe'
    