# Consume the GraphQL api written in the app.py folder consuming the user model
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
        response = requests.post(f"{self.url}/graphql", json={
            "query": """
                query ListUsers {
                    listUsers {
                        users {
                            id
                            username
                            email
                        }
                    }
                }
            """
        })

        if response.status_code == 200:
            return [User(
                id=user['id'],
                username=user['username'],
                email=user['email']
            ) for user in response.json()['data']['listUsers']['users']]

    @classmethod
    def create(self, username, email, password):
        response = requests.post(f"{self.url}/graphql", json={
            "query": """
                mutation CreateUser($username: String!, $email: String!, $password: String!) {
                    createUser(username: $username, email: $email, password: $password) {
                        user {
                            id
                            username
                            email
                        }
                    }
                }
            """,
            "variables": {
                "username": username,
                "email": email,
                "password": password
            }
        })

        return User(
            id=response.json()['data']['createUser']['user']['id'],
            username=response.json()['data']['createUser']['user']['username'],
            email=response.json()['data']['createUser']['user']['email']
        )

    def find(self):
        response = requests.post(f"{self.__class__.url}/graphql", json={
            "query": """
                query GetUser($id: ID!) {
                    getUser(id: $id) {
                        user {
                            id
                            username
                            email
                        }
                    }
                }
            """,
            "variables": {
                "id": self.id
            }
        })

        if response.status_code == 200:
            self.username = response.json()['data']['getUser']['user']['username']
            self.email = response.json()['data']['getUser']['user']['email']

    def update(self, username=None, email=None, password=None):
        data = {
            "username": username or self.username,
            "email": email or self.email,
        }
        if password:
            data['password'] = password

        response = requests.post(f"{self.__class__.url}/graphql", json={
            "query": """
                mutation UpdateUser($id: ID!, $username: String!, $email: String!, $password: String) {
                    updateUser(id: $id, username: $username, email: $email, password: $password) {
                        user {
                            id
                            username
                            email
                        }
                    }
                }
            """,
            "variables": {
                "id": self.id,
                "username": data['username'],
                "email": data['email'],
                "password": data.get('password')
            }
        })

        self.username = response.json()['data']['updateUser']['user']['username']
        self.email = response.json()['data']['updateUser']['user']['email']

    def delete(self):
        response = requests.post(f"{self.__class__.url}/graphql", json={
            "query": """
                mutation DeleteUser($id: ID!) {
                    deleteUser(id: $id) {
                        user {
                            id
                            username
                            email
                        }
                    }
                }
            """,
            "variables": {
                "id": self.id
            }
        })

        if response.status_code == 200:
            self.username = response.json()['data']['deleteUser']['user']['username']
            self.email = response.json()['data']['deleteUser']['user']['email']






print(User.all())

print()
print()

user = User(id=2)
user.find()
print(user)


print()
print()


user = User.create(username="asdf", email="barbar@test.com", password="Qwerty123")
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


# user = User(id=4)
user.delete()
print(User.all())


# What are the benefits of using GraqhQL over REST?
# It's a query language for your API, and it's a single endpoint, so you don't have to worry too much about versioning your API, and it's a lot easier to maintain. Also you can just ask for the data you need, and not have to worry about data that doesn't matter to you.
