import hashlib
import os

from . import ModelMixin
from . import db

from .user import User
from utils import log

import json


class Weibo(db.Model, ModelMixin):
    __tablename__ = 'weibos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created_time = db.Column(db.Integer, default=0)
    # 定义关系
    username = db.Column(db.String(1000))
    user_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = self.dt()
        self.username = form.get('username', '')
        self.comments = []

    def load_comments(self):
        cs = Comment.query.filter_by(weibo_id=self.id).all()
        return cs

    def valid_add(self):
        return len(self.content) > 0 and len(self.content) < 140

    def get_avatar(self):
        a = User.query.filter_by(username=self.username).first()
        if a is None:
            return 'http://p1.qq181.com/cms/1208/2012082315521391704.jpg'
        return a.avatar


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created_time = db.Column(db.Integer, default=0)
    username = db.Column(db.String(1000))
    # 定义关系
    user_id = db.Column(db.Integer)
    weibo_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = self.dt()
        self.username = form.get('username', '')
        self.weibo_id = form.get('weibo_id', '')

    def valid_add(self):
        return len(self.content) > 0 and self.user_id is not None

    def get_avatar(self):
        a = User.query.filter_by(username=self.username).first()
        if a is None:
            return 'http://p1.qq181.com/cms/1208/2012082315521391704.jpg'
        return a.avatar

    def json(self):
        d = {
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
            'weibo_id': self.weibo_id,
            'user_id': self.user_id,
            'avatar': self.get_avatar(),
        }
        return json.dumps(d, ensure_ascii=False)
