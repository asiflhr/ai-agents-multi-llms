'''
Understanding dataclasses in python

Advantages of dataclasses over normal classes:

1.Automatically adds __init__ method
2.It makes the class attributes clear at a glance
'''

from dataclasses import dataclass

@dataclass
class User:
    age: int
    name: str
    email: str

a = User(age=10, name="Aditya", email="aditya@gmail.com")
print(a)
print(a.age)
print(a.name)
print(a.email)

# Without dataclasses
class User:
    def __init__(self, age, name, email):
        self.age = age
        self.name = name
        self.email = email

b = User(age=10, name="Aditya", email="aditya@gmail.com")

print(b)
print(b.age)
print(b.name)
print(b.email)
