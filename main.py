from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Blog, User
from hashutils import check_pw_hash
import random

@app.before_request
def require_login():
    whitelist = ['login', 'signup', 'bloglist', 'index']
    if all([request.endpoint not in whitelist, 'user' not in session, '/static/' not in request.path]):
        return redirect('/login')

def get_user():
    user = User.query.filter_by(username=session.get('user')).first()
    current_user = ''
    if user:
        current_user = user

    return current_user

def get_blogs():
    blogs = Blog.query.order_by(Blog.pubdate.desc()).all()
    return blogs

def get_posts():
    posts_dict = {}
    users =  User.query.all()
    for user in users:
        posts_dict[user] = len(Blog.query.filter_by(owner_id=user.id).all())
    return posts_dict

@app.route('/')
def index():
    users = User.query.all()
    blogs = get_blogs()
    return render_template('index.html',
                           title="Home",
                           users=users,
                           blogs=blogs,
                           user=get_user(),
                           posts=get_posts())


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['user'] = username
            flash('Welcome back, ' + username + '!', 'confirmation')
            return redirect('/blog')

        # TODO - Implement Input Validation

        elif not user:
            flash('That username does not yet exist.', 'error')

        else:
            flash('That password is incorrect.', 'error')

    return render_template('login.html',
                           title='Login',
                           user=get_user())


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username, password, verify = (
            request.form['username'],
            request.form['password'],
            request.form['verify'],
        )

        user = User.query.filter_by(username=username).first()

        # TODO - Implement input validation

        if not user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username
            return redirect('/blog')

    return render_template('signup.html',
                           title='Signup',
                           user=get_user())

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/blog')


@app.route('/blog')
def bloglist():
    blog_id = request.args.get('id')
    blogs = Blog.query.order_by(Blog.pubdate.desc()).all()

    if not blog_id:
        return render_template('bloglist.html',
                               title='Bloglist',
                               blogs=blogs,
                               user=get_user(),)

    blog = Blog.query.get(blog_id)
    pubmonth = blog.pubdate.strftime('%b')
    pubdate = blog.pubdate.strftime('%d')
    pubtime = blog.pubdate.strftime('%I:%M %p')
    return render_template('blog.html',
                            title=blog.title,
                            pubmonth=pubmonth,
                            pubdate=pubdate,
                            pubtime=pubtime,
                            author=blog.owner.username,
                            blog_title=blog.title,
                            blog_body=blog.body,
                            blogs=blogs,
                            user=get_user(),)


@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    blogs = Blog.query.order_by(Blog.pubdate.desc()).all()
    user = get_user()

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
            new_blog = Blog(blog_title, blog_body, user)
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
                                   blogs=blogs,
                                   user=user,)

    return render_template('newpost.html',
                           title='New Blog Post',
                           placeholder=placeholder,
                           blogs=blogs,
                           user=user,)


if __name__ == '__main__':
    app.run(debug=True)
