from datetime import datetime
from flask_restful import Resource, reqparse, abort
from models import (
    Address,
    Category,
    Comment,
    Notification,
    Playlist,
    Post,
    User,
    Video,
    db,
)


# Post endpoints
class PostsApi(Resource):
    post_post_args = reqparse.RequestParser()
    post_post_args.add_argument("title", type=str, help="Title of the post is required", required=True)
    post_post_args.add_argument("description", type=str, help="Description of the post is required", required=True)
    post_post_args.add_argument("user_id", type=int, help="User id is required", required=True)

    def get(self, user_id=None):
        posts = None
        if user_id:
            posts = Post.query.filter_by(user_id=user_id).all()
        else:
            posts = Post.query.all()

        data = [post.to_json_api() for post in posts]
        return {
            'data': data,
            'meta': {'count': len(data)},
            'message': 'Posts fetched successfully'
        },
        200

    def post(self):
        args = self.__class__.post_post_args.parse_args()
        user = User.query.filter_by(id=args['user_id']).first()
        if not user:
            abort(404, message="Could not find user with that id")

        post = Post(
            title=args['title'],
            description=args['description'],
            created_at=datetime.now(),
            user=user
        )
        db.session.add(post)
        db.session.commit()

        return {
            'data': post.to_json_api(),
            'message': 'Post created successfully'
        },
        201


class PostApi(Resource):
    post_update_args = reqparse.RequestParser()
    post_update_args.add_argument("title", type=str, help="Title of the post is required")
    post_update_args.add_argument("description", type=str, help="Body of the post is required")
    post_update_args.add_argument("user_id", type=int, help="User id is required")

    def get(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            abort(404, message="Could not find post with that id")

        return {
            'data': post.to_json_api(),
            'message': 'Post fetched successfully'
        },
        200

    def put(self, post_id):
        args = self.__class__.post_update_args.parse_args()
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            abort(404, message="Could not find post with that id")

        user = User.query.filter_by(id=args['user_id']).first()
        if not user:
            abort(404, message="Could not find user with that id")

        post.title = args['title']
        post.description = args['description']
        post.user_id = user.id
        db.session.commit()

        return {
            'data': post.to_json_api(),
            'message': 'Post updated successfully'
        },
        200

    def delete(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            abort(404, message="Could not find post with that id")

        db.session.delete(post)
        db.session.commit()

        return {
            'message': 'Post deleted successfully'
        },
        200


# User endpoints
class UsersApi(Resource):
    user_post_args = reqparse.RequestParser()
    user_post_args.add_argument("username", type=str, help="Username of the user is required", required=True)
    user_post_args.add_argument("email", type=str, help="Email of the user is required", required=True)
    user_post_args.add_argument("password", type=str, help="Password of the user is required", required=True)

    def get(self):
        users = User.query.all()
        data = [user.to_json_api() for user in users]
        return {
            'data': data,
            'meta': {'count': len(data)},
            'message': 'Users fetched successfully'
        },
        200

    def post(self):
        args = self.__class__.user_post_args.parse_args()
        user = User(
            username=args['username'],
            email=args['email'],
            password=args['password'],
        )
        db.session.add(user)
        db.session.commit()

        return {
            'data': user.to_json_api(),
            'message': 'User created successfully'
        },
        201


class UserApi(Resource):
    user_update_args = reqparse.RequestParser()
    user_update_args.add_argument("username", type=str, help="Username of the user is required")
    user_update_args.add_argument("email", type=str, help="Email of the user is required")
    user_update_args.add_argument("password", type=str, help="Password of the user is required")

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="Could not find user with that id")

        return {
            'data': user.to_json_api(),
            'message': 'User fetched successfully'
        },
        200


    def put(self, user_id):
        args = self.__class__.user_update_args.parse_args()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User doesn't exist, cannot update")

        if args['username']:
            user.username = args['username']
        if args['email']:
            user.email = args['email']
        if args['password']:
            user.password = args['password']

        db.session.commit()

        return {
            'data': user.to_json_api(),
            'message': 'User updated successfully'
        },
        200

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="Could not find user with that id")

        db.session.delete(user)
        db.session.commit()

        return {
            'message': 'User deleted successfully'
        },
        200


# Video endpoints
class VideosApi(Resource):
    video_post_args = reqparse.RequestParser()
    video_post_args.add_argument("name", type=str, help="Name of the video is required", required=True)
    video_post_args.add_argument("views", type=int, help="Views of the video is required", required=True)
    video_post_args.add_argument("likes", type=int, help="Likes of the video is required", required=True)
    video_post_args.add_argument("user_id", type=int, help="User id of the video is required", required=True)

    def get(self, user_id=None):
        videos = None
        if user_id:
            videos = Video.query.filter_by(user_id=user_id).all()
        else:
            videos = Video.query.all()


        data = [video.to_json_api() for video in videos]
        return {
            'data': data,
            'meta': {'count': len(data)},
            'message': 'Videos fetched successfully'
        },
        200

    def post(self):
        args = self.__class__.video_post_args.parse_args()
        user = User.query.filter_by(id=args['user_id']).first()
        if not user:
            abort(404, message="User doesn't exist")

        video = Video(
            name=args['name'],
            views=args['views'],
            likes=args['likes'],
            user_id=user.id,
        )
        db.session.add(video)
        db.session.commit()

        return {
            'data': video.to_json_api(),
            'message': 'Video created successfully'
        },
        201


class VideoApi(Resource):
    video_update_args = reqparse.RequestParser()
    video_update_args.add_argument("name", type=str, help="Name of the video is required")
    video_update_args.add_argument("views", type=int, help="Views of the video is required")
    video_update_args.add_argument("likes", type=int, help="Likes of the video is required")
    video_update_args.add_argument("user_id", type=int, help="User id of the video is required")


    def get(self, video_id):
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Could not find video with that id")

        return {
            'data': video.to_json_api(),
            'message': 'Video fetched successfully'
        },
        200


    def put(self, video_id):
        args = self.__class__.video_update_args.parse_args()
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video doesn't exist, cannot update")

        if args['name']:
            video.name = args['name']
        if args['views']:
            video.views = args['views']
        if args['likes']:
            video.likes = args['likes']
        if args['user_id']:
            user = User.query.filter_by(id=args['user_id']).first()
            if not user:
                abort(404, message="User doesn't exist, cannot update video")

            video.user_id = user.id

        db.session.commit()

        return {
            'data': video.to_json_api(),
            'message': 'Video updated successfully'
        },
        200
