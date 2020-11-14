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
from flask import Flask, render_template, url_for, redirect, request, flash
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
# 在扩展类实例化前加载配置
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'


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

@app.cli.command()
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

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.route('/', methods=['GET', 'POST'])
# def index():
#     movies = Movie.query.all()
#     # 读取用户记录
#     # 读取所有电影记录
#     return render_template('index.html', movies=movies)
def index():
    if request.method == 'POST':
        # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')
        # 传入表单对应输入字段的name值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
            # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    movies = Movie.query.all()
    #user = User.query.first()
    return render_template('index.html', movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
#限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))   # 重定向回主页

@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
    return render_template('404.html'), 404
