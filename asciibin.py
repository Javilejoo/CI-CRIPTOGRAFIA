alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
lista = []

def string_to_ascii(s):
    for char in s:
        lista.append(ord(char))

string_to_ascii("hello")
print(lista)
