# 第二章节
# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/home')
# def hello():
#     return '<h1>s112a</h1>'
# @app.route('/user/<name>')
# def user_page(name):
#   return 'User:%s' % name

# 第三章节
# from flask import Flask, render_template
# app = Flask(__name__)
# name = 'Movee'
# movies = [
# {'title': 'My Neighbor Totoro', 'year': '1988'},
# {'title': 'Dead Poets Society', 'year': '1989'},
# {'title': 'A Perfect World', 'year': '1993'},
# {'title': 'Leon', 'year': '1994'},
# {'title': 'Mahjong', 'year': '1996'},
# {'title': 'Swallowtail Butterfly', 'year': '1996'},
# {'title': 'King of Comedy', 'year': '1999'},
# {'title': 'Devils on the Doorstep', 'year': '1999'},
# {'title': 'WALL-E', 'year': '2008'},
# {'title': 'The Pork of Music', 'year': '2012'},
# ]
#
# @app.route('/')
# def index():
#     return render_template('index.html', name=name, movies=movies)

# 第四章节 第五章节
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import os
import sys
import click

# 导入扩展类
WIN = sys.platform.startswith('win')

# 如果是windows返回True，否则返回false
if WIN:
    # 如果是 Windows 系统,使用三个斜线
    prefix = 'sqlite:///'
else:
    # 否则使用四个斜线
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

@app.cli.command()
# 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:
        # 判断是否输入了选项
        db.drop_all()
        db.create_all()
        click.echo('Initialized database.')
        # 输出提示信息
def forge():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

class User(db.Model):  # 表名将会是 user(自动生成,小写处理)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):
    # 主键
    # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    # 读取用户记录
    # 读取所有电影记录
    return render_template('index.html', user=user, movies=movies)
