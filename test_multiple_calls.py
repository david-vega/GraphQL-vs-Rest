import requests






class GraphQLActivity():
    url = "http://localhost:5000"

    def __init__(self, id, username=None, engagement=0):
        self.id = id
        self.username = username
        self.engagement = engagement


    def __repr__(self):
        return f"User(id={self.id} username={self.username} engagement={self.engagement})"


    def find(self):
        response = requests.post(f"{self.__class__.url}/graphql", json={
            "query": """
                query GetUser($id: ID!) {
                    getUser(id: $id) {
                        user {
                            username
                            videos {
                                id
                            }
                            posts {
                                id
                            }
                        }
                    }
                }
            """,
            "variables": {
                "id": self.id
            }
        })

        print(response.json())

        if response.status_code == 200:
            self.username = response.json()['data']['getUser']['user']['username']
            videos = response.json()['data']['getUser']['user']['videos']
            posts = response.json()['data']['getUser']['user']['posts']

            if videos:
                self.engagement += len(videos)
            if posts:
                self.engagement += len(posts)

class RESTActivity():
    url = "http://localhost:5000"

    def __init__(self, id, username=None, engagement=None):
        self.id = id
        self.username = username
        self.engagement = engagement

    def __repr__(self):
        return f"User(id={self.id} username={self.username} engagement={self.engagement})"

    def find(self):
        user_response = requests.get(f"{self.__class__.url}/user/{self.id}")
        video_response = requests.get(f"{self.__class__.url}/video/?user_id={self.id}")
        post_response = requests.get(f"{self.__class__.url}/post/?user_id={self.id}")

        print(user_response.json())
        print(video_response.json())
        print(post_response.json())

        if user_response.status_code == 200:
            self.username = user_response.json()[0]['data']['attributes']['username']

        if video_response.status_code == 200:
            self.engagement = len(video_response.json()[0]['data'])

        if post_response.status_code == 200:
            self.engagement += len(post_response.json()[0]['data'])

graph = GraphQLActivity(2)
graph.find()
print(graph)

print()
print()

rest = RESTActivity(2)
rest.find()
print(rest)
