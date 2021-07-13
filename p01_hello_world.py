print('hello world')

a = 'Hi!'
b = a * 3
print(b)
for char in a:
    print(char)

name = "Joe"
if len(name) > 3:
    print("Nice name,")
    print(name)
else:
    print("That's a short name,")
    print(name)

n = 0
for i in range(5):
    n += i
print("The sum of the numbers 1 to 4 is: %d" % n)

dict_test = {i: i ** 3 for i in range(5)}
print(dict_test)