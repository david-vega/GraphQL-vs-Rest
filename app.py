from flask import Flask, jsonify, request
from flask_restful import Api
from ariadne import (
	load_schema_from_path,
	make_executable_schema,
	graphql_sync,
	snake_case_fallback_resolvers,
	ObjectType,
)

from models import db
from rest_apis import (
	PostApi,
	PostsApi,
	UserApi,
	UsersApi,
	VideoApi,
	VideosApi,
)

from queries import (
   get_post_resolver,
   get_user_resolver,
   get_video_resolver,
   list_posts_resolver,
   list_users_resolver,
   list_videos_resolver,
)

from mutations import (
	create_post_resolver,
	create_user_resolver,
	create_video_resolver,
	delete_post_resolver,
	delete_user_resolver,
	delete_video_resolver,
	update_post_resolver,
	update_user_resolver,
	update_video_resolver,
)



app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


with app.app_context():
    db.create_all()


###### REST APIs ######

api.add_resource(PostsApi, "/post/")
api.add_resource(PostApi, "/post/<int:post_id>")

api.add_resource(UsersApi, "/user/")
api.add_resource(UserApi, "/user/<int:user_id>")

api.add_resource(VideosApi, "/video/")
api.add_resource(VideoApi, "/video/<int:video_id>")

# api.add_resource(NotificationsApi, "/notification/")
# api.add_resource(NotificationApi, "/notification/<int:notification_id>")

# api.add_resource(CommentsApi, "/comment/")
# api.add_resource(CommentApi, "/comment/<int:comment_id>")

# api.add_resource(CategoriesApi, "/category/")
# api.add_resource(CategoryApi, "/category/<int:category_id>")

# api.add_resource(PlaylistsApi, "/playlist/")
# api.add_resource(PlaylistApi, "/playlist/<int:playlist_id>")

# api.add_resource(AddressesApi, "/address/")
# api.add_resource(AddressApi, "/address/<int:address_id>")


###### GraphQL APIs ######

query = ObjectType("Query")
mutation = ObjectType("Mutation")


query.set_field("getPost", get_post_resolver)
query.set_field("getUser", get_user_resolver)
query.set_field("getVideo", get_video_resolver)
query.set_field("listPosts", list_posts_resolver)
query.set_field("listUsers", list_users_resolver)
query.set_field("listVideos", list_videos_resolver)

mutation.set_field("createPost", create_post_resolver)
mutation.set_field("createUser", create_user_resolver)
mutation.set_field("createVideo", create_video_resolver)
mutation.set_field("deletePost", delete_post_resolver)
mutation.set_field("deleteUser", delete_user_resolver)
mutation.set_field("deleteVideo", delete_video_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("updateUser", update_user_resolver)
mutation.set_field("updateVideo", update_video_resolver)



type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs,
	query,
	mutation,
	snake_case_fallback_resolvers,
)

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400

    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)
