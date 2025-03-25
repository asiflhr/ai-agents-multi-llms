from pydantic import BaseModel, ValidationError

class User(BaseModel):
    age: int
    name: str
    email: str

a = User(age=10, name="Aditya", email="aditya@gmail.com")
print(a)
print(a.age)
print(a.name)
print(a.email)

# Example showing Pydantic's automatic type validation
try:
    # This will succeed - all types are correct
    valid_user=User(age=10, name="Aditya", email="aditya@gmail.com")
    print("""Valid User created: """,valid_user)

    # This will fail - age should be int, not str
    invalid_user=User(age="10", name="Aditya", email="aditya@gmail.com")
    print("""Invalid User created: """,invalid_user)
except ValidationError as e:
    print("Validation Error:")
    print(e.json())
    # Will show detailed error explaining age must an integer