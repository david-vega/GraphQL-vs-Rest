from ariadne import convert_kwargs_to_snake_case
from models import Post, User, Video


# Post queries
@convert_kwargs_to_snake_case
def list_posts_resolver(obj, info):
    try:
        posts = [post.to_dict() for post in Post.query.all()]
        payload = {
            "success": True,
            "posts": posts
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def get_post_resolver(obj, info, id):
    try:
        post = Post.query.get(id)
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Post item matching {id} not found"]
        }
    return payload


# User queries
@convert_kwargs_to_snake_case
def list_users_resolver(obj, info):
    try:
        users = [user.to_dict(include_videos=True) for user in User.query.all()]
        payload = {
            "success": True,
            "users": users
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def get_user_resolver(obj, info, id):
    try:
        user = User.query.get(id)
        payload = {
            "success": True,
            "user": user.to_dict(include_videos=True, include_posts=True)
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["User item matching {id} not found"]
        }
    return payload


# Video queries
@convert_kwargs_to_snake_case
def list_videos_resolver(obj, info):
    try:
        videos = [video.to_dict(include_user=True) for video in Video.query.all()]
        payload = {
            "success": True,
            "videos": videos
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def get_video_resolver(obj, info, id):
    try:
        video = Video.query.get(id)
        payload = {
            "success": True,
            "video": video.to_dict(include_user=True)
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Video item matching {id} not found"]
        }
    return payload
