import hashlib
import os

from . import ModelMixin
from . import db

from utils import log


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    avatar = db.Column(db.String())

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar = form.get('avatar', 'http://p1.qq181.com/cms/1208/2012082315521391704.jpg')
        self.created_time = self.dt()


    # 验证注册用户的合法性的
    def valid_register(self):
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_username_len = len(self.username) >= 3
        valid_password_len = len(self.password) >= 3
        # valid_captcha = self.captcha == '3'
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度必须大于等于 3'
            msgs.append(message)
        elif not valid_password_len:
            message = '密码长度必须大于等于 3'
            msgs.append(message)
        # elif not valid_captcha:
        #     message = '验证码必须输入 3'
        #     msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs

    # def error_message(self):
    #     if len(self.username) <= 2:
    #         return '用户名长度必须大于等于 3'
    #     elif len(self.password) <= 2:
    #         return '密码长度必须大于等于 3'
    #     elif User.query.filter_by(username=self.username).first() != None:
    #         return '用户名已存在'

    def valid_login(self, u):
        if u is not None:
            username_equals = u.username == self.username
            password_equals = u.password == self.password
            return username_equals and password_equals
        else:
            return False

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False

    def change_avatar(self, avatar):
        if len(avatar) > 2:
            self.avatar = avatar
            self.save()
            return True
        else:
            return False

    def json(self):
        d = dict(
            id=self.id,
            username=self.username,
            created_time=self.created_time,
            avatar=self.get_avatar(),
            password=self.password,
        )
        return d
