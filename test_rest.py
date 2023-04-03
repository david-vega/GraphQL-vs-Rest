# Consume the REST api written in the app.py folder the user model
import requests


class User():
    url = "http://localhost:5000"

    def __init__(self, id, username=None, email=None):
        self.id = id
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

    @classmethod
    def all(self):
        response = requests.get(f"{self.url}/user/")

        if response.status_code == 200:
            return [User(
                id=user['id'],
                username=user['attributes']['username'],
                email=user['attributes']['email']
            ) for user in response.json()[0]['data']]

    @classmethod
    def create(self, username, email, password):
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        response = requests.post(f"{self.url}/user/", json=data)

        return User(
            id=response.json()[0]['data']['id'],
            username=response.json()[0]['data']['attributes']['username'],
            email=response.json()[0]['data']['attributes']['email']
        )


    def find(self):
        response = requests.get(f"{self.__class__.url}/user/{self.id}")
        if response.status_code == 200:
            self.username = response.json()[0]['data']['attributes']['username']
            self.email = response.json()[0]['data']['attributes']['email']

    def update(self, username=None, email=None, password=None):
        data = {
            "username": username or self.username,
            "email": email or self.email,
        }
        if password:
            data['password'] = password

        response = requests.put(f"{self.__class__.url}/user/{self.id}", json=data)

        self.username = response.json()[0]['data']['attributes']['username']
        self.email = response.json()[0]['data']['attributes']['email']

    def delete(self):
        response = requests.delete(f"{self.__class__.url}/user/{self.id}")
        if response.status_code == 200:
            self.id = None
            self.username = None
            self.email = None



print(User.all())

print()
print()


user = User(id=2)
user.find()
print(user)

print()
print()

user = User.create(username="asdf", email="barbar@test.com", password="Qwerty123")
print(user)
print()
print(User.all())

print()
print()


user.update(email="waka@waka.com")
print(user)
print()
print(User.all())

print()
print()

user.delete()
print(User.all())


# What are the benefits of using REST over GraphQL?

# REST is more widely used and supported by more tools and libraries. It is also easier to implement and understand. GraphQL is more flexible and allows for more complex queries. It is also more secure because it is more difficult to create a query that will return more data than you want. It is also more efficient because it allows you to only request the data you need.
