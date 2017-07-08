from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Blog, User
import random


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method is 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and password is user.password:
            session['user'] = username
            flash('Welcome back, ' + username + '!')
            return redirect('/blog')
        elif not user:
            flash('That user name does not yet exist.', 'error')
        else:
            flash('That password is incorrect.', 'error')

    return render_template('login.html', 
                           username=username,)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if request.method is 'POST':
        username, password, verify = (
            request.form['username'], 
            request.form['password'], 
            request.form['verify'],
        )
        user = User.query.filter_by(username=username).first()

        if not any()
            flash('Please enter a username and password')



@app.route('/blog')
def bloglist():
    blog_id = request.args.get('id')
    blogs = Blog.query.order_by(Blog.pubdate.desc()).all()

    if blog_id:
        blog = Blog.query.get(blog_id)
        pubmonth = blog.pubdate.strftime('%b')
        pubdate = blog.pubdate.strftime('%d')
        pubtime = blog.pubdate.strftime('%I:%M %p')
        return render_template('blog.html',
                               title=blog.title,
                               pubmonth=pubmonth,
                               pubdate=pubdate,
                               pubtime=pubtime,
                               blog_title=blog.title,
                               blog_body=blog.body,
                               pub_date=blog.pubdate,
                               blogs=blogs,)
    else:
        return render_template('bloglist.html',
                               title='Bloglist',
                               blogs=blogs,)


@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    blogs = Blog.query.order_by(Blog.pubdate.desc()).all()

    placeholder = random.choice([
        "What's on your mind?",
        "How're you doing today?",
        "This message is randomly generated! Neat!",
        "I'm running out of random messages to display...",
    ])

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        title_error = body_error = ''

        if not blog_title:
            title_error = "Your blog needs a title."

        if not blog_body:
            body_error = "Please add some content to your blog post."

        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id
            return redirect('/blog?id={0}'.format(blog_id))
        else:
            return render_template('newpost.html',
                                   title='New Blog Post',
                                   blog_body=blog_body,
                                   blog_title=blog_title,
                                   title_error=title_error,
                                   body_error=body_error,
                                   placeholder=placeholder,
                                   blogs=blogs,)

    return render_template('newpost.html',
                           title='New Blog Post',
                           placeholder=placeholder,
                           blogs=blogs,)


if __name__ == '__main__':
    app.run()
