from . import ModelMixin
from . import db

from .user import User
from utils import log


class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    created_time = db.Column(db.Integer)
    updated_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String(1000))
    title = db.Column(db.String(1000))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = self.dt()
        self.username = form.get('username', '')
        self.comments = ''
        self.title = form.get('title', '')


    def update(self, form):
        self.content = form.get('content', '')
        self.save()

class BlogComment(db.Model, ModelMixin):
    __tablename__ = 'blogcomments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created_time = db.Column(db.Integer, default=0)
    username = db.Column(db.String(1000))
    # 定义关系
    user_id = db.Column(db.Integer)
    blog_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = self.dt()
        self.username = form.get('username', '')
        self.blog_id = form.get('blog_id', '')

    def get_avatar(self):
        a = User.query.filter_by(username=self.username).first()
        if a is None:
            return 'http://p1.qq181.com/cms/1208/2012082315521391704.jpg'
        return a.avatar
