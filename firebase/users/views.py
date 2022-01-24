from flask import render_template, url_for, flash, redirect, request, Blueprint, session, jsonify
from firebase.users.forms import LoginForm, RegistrationForm, UpdateUserForm, BlogPostsForm
from firebase.users.picture_handler import add_profile_pic, add_post_pic
from datetime import datetime
import pyrebase
from firebase import db, auth, storage
from firebase.users.functions import checker, blogcheck


users = Blueprint('users', __name__)

# register view
@users.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = {
            'username' : form.username.data,
            'email' : form.email.data,
            'password' : form.password.data,
            'is_active' : True,
            'picture' :  "jaggu.jpg",
            'blogposts' : list(tuple({''}))
        }
        name = db.child("users").child(user['username']).get().val()
        if name != None:
            return jsonify({"error" : "Username Taken Try With Another Name"}), 400 

        email = form.email.data
        password = form.password.data
        users = auth.create_user_with_email_and_password(email,password)
        db.child("users").child(user['username']).set(user) 
        return redirect(url_for('users.login')) 
        
    return render_template('register.html', form = form)


#   login view
@users.route('/login', methods=['POST','GET'])
def login():

    form = LoginForm()
    check = False
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        login = auth.sign_in_with_email_and_password(email, password)
        users = db.child("users").get().val().values()
        username = checker(users, email)
        user =  db.child("users").child(username).get().val()
        session['username'] = user['username']
        session['login'] = True 
        check = True 
        form.email.data = "" 
        form.password.data = "" 
        return redirect(url_for('users.home')) 
        
    return render_template('login.html', form = form, check=check)


#   logout view 
@users.route('/logout')
def logout():
    session.clear()
    session['login'] = False
    return redirect(url_for("users.home"))


# profile view for particular user using dynamic routing (update userform)
@users.route('/profile/<username>', methods=['POST','GET'])
def profile(username):
    if session['login']:
        form = UpdateUserForm()
        user = db.child("users").child(username).get().val()
        profile = user['picture']
        blogposts = user['blogposts']
        length = len(blogposts)
        if form.validate_on_submit():
            if form.picture.data:
                pic = add_profile_pic(form.picture.data, user['username'])
                profile = pic
                db.child("users").child(session['username']).update({'picture':pic})
                return redirect(url_for('users.home'))

        profile_image = url_for('static', filename='profile_pics/'+profile)
        return render_template('profile.html', profile=profile, user=user, form=form, blogposts=blogposts, length=length)

    else:
        return redirect(url_for('users.home'))

        
@users.route('/home', methods=['POST','GET'])
def home():
    if session['login']:
        form = BlogPostsForm()
        user = db.child("users").child(session['username']).get().val()
        blog_data = db.child("blogposts").get().val()
        count = blogcheck(blog_data)

        if form.validate_on_submit():
            now = datetime.now()
            post_author = session['username']
            post_date = str(now.strftime("%d-%m-%Y"))
            post_text = form.text.data
            if form.picture.data:
                pic = add_post_pic(form.picture.data, user['username'], count)
                profile = url_for('static', filename='post_pics/'+pic)
                db.child("blogposts").child(count).set({'id':count, 'author':post_author, 'text':post_text, 'date':post_date, 'picture':profile})
                user['blogposts'].append({'id':count, 'author':post_author, 'text':post_text, 'date':post_date, 'picture':profile})
            else:
                user['blogposts'].append({'id':count, 'author':post_author, 'text':post_text, 'date':post_date})
                db.child("blogposts").child(count).set({'id':count, 'author':post_author, 'text':post_text, 'date':post_date})
            db.child("users").child(post_author).update({'blogposts':user['blogposts']})
            return redirect(url_for('users.home'))
        return render_template('home.html', form=form, user=user, blog_data = blog_data)

    return render_template('index.html')


@users.route('/about', methods=['POST','GET'])
def about():
    if session['login']:
        user = db.child("users").child(session['username']).get().val()
        blogposts = []
        if user['blogposts']:
            blogposts = user['blogposts']

        return render_template('about.html', user=user, blogposts =blogposts , length=len(blogposts )-1)

    else:
        return redirect(url_for('users.home'))

@users.route('/')
def index():
    session['start'] = True
    return render_template('index.html')