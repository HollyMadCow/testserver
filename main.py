#!/usr/bin/python
#coding: utf-8

from flask import Flask, abort, request, jsonify, g, url_for
from pymongo import MongoClient
from datetime import datetime, time
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
import random
import string
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


app = Flask(__name__)
client = MongoClient()
app.config['SECRET_KEY'] = '$%NY5tNH%^%56mn^%&^bv%YBGF$%$%BTR$%$%^EB54^%$##$#Y$^V$#YGEg43$#GRG@##@V'
app.config['AUTH_SALT'] = '@#F$T$H%H3t53$%Y45y$%Y65hgv$%'
auth = HTTPBasicAuth()


"""
随机字符串
"""


def random_str(randomlength=16):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

"""
添加类
"""


class User(object):
    username = ''
    passwordhash = ''

    def __init__(self, username,passwordhash):
        self.username = username
        self.password_hash = passwordhash
    # __tablename__ = 'users'
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(32), index=True)
    # password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True



tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


# @app.route('/v1/add', methods=['GET'])
# def get_tasks0():
#
#         db = client.testdb
#         post = {"author": "Mike1",
#                 "text": "My first blog post!",
#                 "tags": ["mongodb", "python", "pymongo"]}
#         posts = db.col2
#         posts.insert(post)
#         return jsonify({'tasks': tasks})

# @app.route('/api/v1/tasks', methods=['GET'])


# @app.route('/v1/add1w', methods=['GET'])
# def get_add1w():
#     db = client.testdb
#     posts = db.col2
#     for x in range(1000):
#         new_post = {"UserName": random_str(), 'date': datetime.now()}
#         posts.insert(new_post)
#     return 'ok'

# 授权连接
@app.route('/v1/auth', methods=['POST', 'GET'])
def get_token():
    return jsonify({'date:':  datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    # pass


# 奖励api
@app.route('/v1/reward', methods=['POST'])
def get_reward():
    pass


# 添加收货地址
@app.route('/v1/addaddress', methods=['POST'])
def add_address():
    pass


# 更新用户资料
@app.route('/v1/updateuserinfo', methods=['POST'])
def update_userinfo():
    pass


# 用户注册
@app.route('/v1/register', methods=['POST'])
def reg_user():
    test = request.headers['token']
    return jsonify(test)


# 忘记密码
@app.route('/v1/forget', methods=['POST'])
def forget_user():
    pass


# 客户端获取用户信息
@app.route('/v1/user/<userid>', methods=['GET'])
def get_userinfo(userid):

    return userid


#列表
@app.route('/v1/itemlist', methods=['GET'])
def get_itemlist():

    pass


# 获取物品信息
@app.route('/v1/item/<itemid>', methods=['GET'])
def get_item(itemid):

    return itemid


@app.route('/v1/additem/<itemid>', methods=['POST'])
def add_item():

    pass


#添加购物车
@app.route('/v1/addcart/', methods=['POST'])
def add_cart():

    pass


#下单
@app.route('/v1/placedorder/', methods=['POST'])
def place_order():

    pass


# 登录
@app.route('/v1/login', methods=['POST'])
def user_login():
    pass


# 测试API
@app.route('/api/v1/tasks')
def get_tasks():

    pa = request.args.get('do')
    pa1 = request.values.get('test')
    #header=request.headers
    return pa + pa1
    # return jsonify({'tasks': tasks})


# 测试API
@app.route('/api/v1/test')
def get_tasks1():

	#
    # client = MongoClient()
    # db = client.testdb
    # post = {"author": "Mike",
    #         "text": "My first blog post!",
    #         "tags": ["mongodb", "python", "pymongo"]}
    # posts = db.test1
    # posts.insert(post)
    pa = request.args.get('do')
    pa1 = request.values.get('test')

    return pa + pa1
    # return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run()
