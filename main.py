import random
from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Blog, User
from hashutils import check_pw_hash
import verifyutils
from config import POSTS_PER_PAGE
import time

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
    blogs = Blog.query.order_by(Blog.pubdate.desc())
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
    return render_template('index.html',
                           title="Home",
                           users=users,
                           blogs=get_blogs(),
                           user=get_user(),
                           posts=get_posts(),)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        usererror = passerror = ""

        if not user:
            usererror = "That user doesn't exist yet."
            return render_template('login.html',
                                   title='Login',
                                   user=get_user(),
                                   username=username,
                                   usererror=usererror,
                                   blogs=get_blogs(),)

        if not check_pw_hash(password, user.pw_hash):
            passerror = "That password is incorrect."

        if any([usererror, passerror]):
            return render_template('login.html',
                                   title='Login',
                                   user=get_user(),
                                   username=username,
                                   usererror=usererror,
                                   passerror=passerror,
                                   blogs=get_blogs(),)

        session['user'] = username
        flash('Welcome back, ' + username + '!', 'confirmation')
        return redirect('/blog')

    return render_template('login.html',
                           title='Login',
                           user=get_user(),
                           blogs=get_blogs(),)


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username, password, verify = (
            request.form['username'],
            request.form['password'],
            request.form['verify'],
        )

        user = User.query.filter_by(username=username).first()

        usererrors = verifyutils.check_username_signup(username, user)
        passerrors = verifyutils.check_password_signup(password)
        verifyerrors = verifyutils.check_verify_signup(verify, password)

        if any([usererrors, passerrors, verifyerrors]):
            return render_template('signup.html',
                                   title='Signup',
                                   user=get_user(),
                                   username=username,
                                   usererrors=usererrors,
                                   passerrors=passerrors,
                                   verifyerrors=verifyerrors,
                                   blogs=get_blogs(),)

        if not user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username
            return redirect('/blog')

    return render_template('signup.html',
                           title='Signup',
                           user=get_user(),
                           blogs=get_blogs(),)


@app.route('/logout')
def logout():
    del session['user']
    return redirect('/login')


@app.route('/blog')
@app.route('/blog/<int:page>')
def bloglist(user=None, page=1):
    blog_id = request.args.get('id')
    user = request.args.get('user')
    user_filter = User.query.filter_by(username=user).first()

    if user_filter:
        blogs = Blog.query.filter_by(owner_id=user_filter.id).order_by(Blog.pubdate.desc())
        return render_template('bloglist.html',
                               title='Bloglist',
                               blogs=get_blogs(),
                               page_blogs=blogs.paginate(page, POSTS_PER_PAGE, False),
                               user=get_user(),)

    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('blog.html',
                               title=blog.title,
                               blog=blog,
                               blogs=get_blogs(),
                               user=get_user(),)

    return render_template('bloglist.html',
                           title='Bloglist',
                           blogs=get_blogs(),
                           page_blogs=get_blogs().paginate(page, POSTS_PER_PAGE, False),
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

### FOR TESTING PURPOSES ONLY ###
@app.route('/build-blogs')
def genBlogs():
    user = get_user()
    for i in range(20):
        db.session.add(Blog('TestBlog ' + str(i), 'THIS IS JUST A TEST DONT WORRY ABOUT IT', user))
        time.sleep(0.2)
        db.session.commit()
    return redirect('/blog') 
### END TESTING ### 


if __name__ == '__main__':
    app.run(debug=True)
