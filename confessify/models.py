from confessify import db


class User(db.Model):
    # schema for user account
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    posts = db.relationship("Post", backref="user", cascade="all, delete", lazy=True)

    def __repr__(self):
        return self.username


class Post(db.Model):
    # schema for posts
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(25), nullable=False)
    post_content = db.Column(db.String(250), nullable=False)
    post_user = db.Column(db.String, db.ForeignKey("user.username", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"#{self.id} - Title: {self.post_title} | Confession: {self.post_content}"