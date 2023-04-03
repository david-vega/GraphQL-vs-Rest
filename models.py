from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


category_video = db.Table(
    'category_video',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'), primary_key=True),
)


playlist_video = db.Table(
    'playlist_video',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'), primary_key=True),
)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='address')

    def to_json_api(self):
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'attributes': {
                'street': self.street,
                'city': self.city,
                'state': self.state,
                'zip': self.zip,
                'user_id': self.user_id,
            },
            'relationships': {
                'user': self.user.to_json_api(),
            },
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    videos = db.relationship('Video', secondary=category_video, backref='category')

    def to_json_api(self):
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'attributes': {
                'name': self.name,
            },
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)

    user = db.relationship('User', backref='comment')
    video = db.relationship('Video', backref='comment')

    def to_json_api(self):
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'attributes': {
                'comment': self.comment,
                'user_id': self.user_id,
                'video_id': self.video_id,
            },
            'relationships': {
                'user': self.user.to_json_api(),
                'video': self.video.to_json_api(),
            },
        }


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    kind = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='notification')

    def to_json_api(self):
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'attributes': {
                'kind': self.kind,
                'message': self.message,
                'user_id': self.user_id,
            },
            'relationships': {
                'user': self.user.to_json_api(),
            },
        }


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='playlist')
    videos = db.relationship('Video', secondary=playlist_video, backref='playlist')

    def to_json_api(self):
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'attributes': {
                'name': self.name,
                'user_id': self.user_id,
            },
            'relationships': {
                'user': self.user.to_json_api(),
            },
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_json_api(self):
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'attributes': {
                'title': self.title,
                'description': self.description,
                'created_at': str(self.created_at),
            },
        }

    def to_dict(self, include_user=False):
        data =  {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': str(self.created_at),
        }

        if include_user:
            data['user'] = self.user.to_dict()

        return data



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    posts = db.relationship('Post', backref='user', lazy=True)
    videos = db.relationship('Video', backref='user', lazy=True)

    def to_json_api(self):
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'attributes': {
                'username': self.username,
                'email': self.email,
            },
        }

    def to_dict(
        self,
        include_videos=False,
        include_posts=False,
    ):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
        if include_videos:
            data['videos'] = [video.to_dict() for video in self.videos]

        if include_posts:
            data['posts'] = [post.to_dict() for post in self.posts]

        return data


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    categories = db.relationship('Category', secondary=category_video, backref='video')
    playlists = db.relationship('Playlist', secondary=playlist_video, backref='video')

    def to_json_api(self):
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'attributes': {
                'name': self.name,
                'views': self.views,
                'likes': self.likes,
            },
            'relationships': {
                'user': self.user.to_json_api(),
            },
        }

    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'name': self.name,
            'views': self.views,
            'likes': self.likes,
        }
        if include_user:
            data['user'] = self.user.to_dict()


        return data
