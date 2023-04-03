from datetime import datetime
from ariadne import convert_kwargs_to_snake_case
from models import Post, User, Video, db


# Post mutations
@convert_kwargs_to_snake_case
def create_post_resolver(obj, info, title, description, user_id):
    try:
        post = Post(
            title=title,
            description=description,
            created_at=datetime.now(),
            user_id=user_id,
        )

        db.session.add(post)
        db.session.commit()
        payload = {
            "success": True,
            "post": post.to_dict(include_user=True),
        }
    except ValueError:
        payload = {
            "success": False,
            "errors": [
                f"Incorrect date format provided. Date should be in "
                f"the format dd-mm-yyyy",
            ]
        }
    return payload


@convert_kwargs_to_snake_case
def update_post_resolver(obj, info, id, title, description, user_id):
    try:
        post = Post.query.get(id)
        if post:
            post.title = title
            post.description = description
            post.user_id = user_id
        db.session.add(post)
        db.session.commit()
        payload = {
            "success": True,
            "post": post.to_dict(include_user=True)
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload


@convert_kwargs_to_snake_case
def delete_post_resolver(obj, info, id):
    try:
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        payload = {"success": True, "post": post.to_dict(include_user=True)}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload


# User mutations
@convert_kwargs_to_snake_case
def create_user_resolver(obj, info, username, email, password):
    try:
        user = User(
            username=username,
            email=email,
            password=password,
        )

        db.session.add(user)
        db.session.commit()
        payload = {
            "success": True,
            "user": user.to_dict(include_videos=True),
        }
    except ValueError:
        payload = {
            "success": False,
            "errors": [
                f"Incorrect date format provided. Date should be in "
                f"the format dd-mm-yyyy",
            ]
        }
    return payload


@convert_kwargs_to_snake_case
def update_user_resolver(obj, info, id, username, email, password):
    try:
        user = User.query.get(id)
        if user:
            user.username = username
            user.email = email
            if password:
                user.password = password
        db.session.add(user)
        db.session.commit()
        payload = {
            "success": True,
            "user": user.to_dict(include_videos=True)
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload


@convert_kwargs_to_snake_case
def delete_user_resolver(obj, info, id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        payload = {"success": True, "user": user.to_dict(include_videos=True)}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload


# Video mutations

@convert_kwargs_to_snake_case
def create_video_resolver(obj, info, name, likes, views, user_id):
    try:
        video = Video(
            name=name,
            likes=likes,
            views=views,
            user_id=user_id,
        )

        db.session.add(video)
        db.session.commit()
        payload = {
            "success": True,
            "video": video.to_dict(include_user=True),
        }
    except ValueError:
        payload = {
            "success": False,
            "errors": [
                f"Incorrect date format provided. Date should be in "
                f"the format dd-mm-yyyy",
            ]
        }
    return payload


@convert_kwargs_to_snake_case
def update_video_resolver(obj, info, id, name, likes, views, user_id):
    try:
        video = Video.query.get(id)
        if video:
            video.name = name
            video.likes = likes
            video.views = views
            video.user_id = user_id
        db.session.add(video)
        db.session.commit()
        payload = {
            "success": True,
            "video": video.to_dict(include_user=True)
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload


@convert_kwargs_to_snake_case
def delete_video_resolver(obj, info, id):
    try:
        video = Video.query.get(id)
        db.session.delete(video)
        db.session.commit()
        payload = {"success": True, "video": video.to_dict(include_user=True)}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload
