import os
import secrets
import random
from app_base import app, db, mail
from flask_mail import Message
from flask import render_template, request, url_for, flash, redirect
from app_base.forms import RegistrationForm, LoginForm, ArticleForm, EmailConfirm, EditForm, RequestPassReset, ConfirmPassReset
from app_base.models import User, Article, check_password_hash
from PIL import Image

from config import basedir


from itsdangerous import URLSafeTimedSerializer, SignatureExpired


# Imports Flask-Login Module/functions
from flask_login import login_user, current_user, logout_user, login_required


class Posts():
    def __init__(self):
        self.id = 0
        self.category = ""
        self.title = ""
        self.author = ""
        self.authorPhoto = ""
        self.article = ""
        self.location = ""
        self.source = ""
        self.date_created =""
        self.photopath = []


class Pages():
    def __init__(self):
        self.first_page = 1
        self.current_page = 1
        self.last_page = 1
        self.next_num = 1
        self.prev_num = 1
        self.has_pref = False
        self.has_next = False




def text_to_list(text):
    a =[]
    if text:
        a = list(text.split("#!$"))
    return a

def list_to_text(list1):
    txt = ""
    for item in list1:
        if txt == "":
            txt = item
        else:
            txt = txt + "#!$" + item
    return txt

# side bars pictures
def sidePictures(basedir,lenOfItems):
    photoList = []
    target = os.path.join(basedir, "app_base/static/artimages/")
    for file in os.listdir(target):
        if file.endswith(".jpg"):
            photoList.append(file)
    left = []
    right = []
    for i in range(lenOfItems+3):
        if i == 0 or i%2 == 0:
            left.append('<img class="side_image_1" src="/static/artimages/{}" alt="">'.format(photoList[random.randint(0, len(photoList)-1)]))
        else:
            left.append('<img class="side_image_2" src="/static/artimages/{}" alt="">'.format(photoList[random.randint(0, len(photoList) - 1)]))
        if i > 0:
            if i % 2 == 0:
                right.append('<img class="side_image_1" src="/static/artimages/{}" alt="">'.format(photoList[random.randint(0, len(photoList) - 1)]))
            else:
                right.append('<img class="side_image_2" src="/static/artimages/{}" alt="">'.format(photoList[random.randint(0, len(photoList) - 1)]))
    return [left, right]


@app.route("/")
def home():
    pages = Pages()
    search = request.args.get('search')
    if search:
        pages.current_page = request.args.get('page', 1, type=int)
        posts2 = Article.query.filter(Article.title.contains(search)| Article.article.contains(search))
        posts1 = posts2.paginate(page = pages.current_page , per_page = 10,)
        pages.last_page = posts1.pages
        pages.next_num = posts1.next_num
        pages.prev_num = posts1.prev_num
        pages.has_next = posts1.has_next
        pages.has_prev = posts1.has_prev
        posts = []
        for post1 in posts1.items:
            user = User.query.filter_by(username=post1.author).one_or_none()
            post = Posts()
            post.id = post1.id
            post.category = post1.category
            post.title = post1.title
            post.author = post1.author
            post.authorPhoto = user.photourl
            post.article = post1.article
            post.location = post1.location
            post.source = post1.source
            post.date_created = post1.date_created.strftime('%B %d, %Y')
            post.photopath = text_to_list(post1.photopath)
            posts.append(post)
    else:
# give all posts to pages
        pages.current_page = request.args.get('page', 1, type=int)
        posts1 = Article.query.paginate(page = pages.current_page , per_page = 10,)
        pages.last_page = posts1.pages
        pages.next_num = posts1.next_num
        pages.prev_num = posts1.prev_num
        pages.has_next = posts1.has_next
        pages.has_prev = posts1.has_prev
        posts = []
        for post1 in posts1.items:
            user = User.query.filter_by(username=post1.author).one_or_none()
            post = Posts()
            post.id = post1.id
            post.category = post1.category
            post.title = post1.title
            post.author = post1.author
            post.authorPhoto = user.photourl
            post.article = post1.article
            post.location = post1.location
            post.source = post1.source
            post.date_created = post1.date_created.strftime('%B %d, %Y')
            post.photopath = text_to_list(post1.photopath)
            posts.append(post)

    return render_template("main.html", posts = posts, pages = pages, leftBar = sidePictures(basedir,len(posts))[0], rightBar = sidePictures(basedir,len(posts))[1])

@app.route("/401")
def err401():
    return render_template("401.html")
@app.route("/post/<int:post_id>")
def post(post_id):
    # posts = Article.query.filter()
    post1 = Article.query.filter_by(id=post_id).first_or_404()
    user = User.query.filter_by(username=post1.author).one_or_none()
    post = Posts()
    post.id = post1.id
    post.category = post1.category
    post.title = post1.title
    post.author = post1.author
    post.authorPhoto = user.photourl
    post.article = post1.article
    post.location = post1.location
    post.source = post1.source
    post.date_created = post1.date_created.strftime('%B %d, %Y')
    post.photopath = text_to_list(post1.photopath)
    return render_template("post.html", post = post)


@app.route("/edit/<int:post_id>", methods =["GET","POST"])
@login_required
def editPost(post_id):
    post1 = Article.query.filter_by(id=post_id).first_or_404()
    post = Posts()
    post.id = post1.id
    post.title = post1.title
    post.photopath = text_to_list(post1.photopath)
    if current_user.username == post1.author:
        form = ArticleForm(formdata=request.form, obj=post1)
        if request.method == "POST" and form.validate():
            print(str(form.photos.data)+"this a photos list")
            form.populate_obj(post)
# delete photo
            if request.form.getlist('deletePhoto'):
                delPhoto = request.form.getlist('deletePhoto')
                target = os.path.join(basedir, "app_base/static/artimages/")
                for photo in delPhoto:
                    print(target+photo)
                    if os.path.isfile(target+photo):
                        os.remove(target+photo)
                    post.photopath.remove(photo)
# end delete photo
#add new photo
            if request.files.getlist('inputFile'):
                for photo in request.files.getlist('inputFile'):
                    if photo:
                        target = os.path.join(basedir, "app_base/static/artimages/")
                        if not os.path.isdir(target):
                            os.mkdir(target)
                        filename = secrets.token_hex(16)+".jpg"
                        destination = "/".join([target,filename])
                        print(destination)
                        photo.save(destination)
                        post.photopath.append(filename)

# end add new photo
            post1.photopath = list_to_text(post.photopath)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash("something went wrong")
    else:
        return redirect(url_for('err401'))
    return render_template("editpost.html", form = form , post = post)


@app.route("/login", methods = ["GET","POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user_email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == user_email).one_or_none()
        if logged_user and check_password_hash(logged_user.password,password):
            login_user(logged_user)
            print(current_user.username)
            return redirect(url_for('home'))
    return render_template('login.html', form = form)
   # return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
@app.route('/email_confirm',methods=['GET', 'POST'])
def email_confirm():
    form = EmailConfirm()
    if request.method == "POST" and form.validate():
        email = form.email.data
        if User.query.filter(User.email.contains(email)).one_or_none():
            flash("user with same email already exist")
            return redirect(url_for("email_confirm"))
        else:
            token = s.dumps(email, salt='email-confirm')
            msg = Message('Confirm Email', sender='admin@chicagotouristinfo.org', recipients=[email])
            link = url_for('register', token=token, _external=True)
            msg.body = "Your link is: {}".format(link)
            mail.send(msg)
        return redirect(url_for('home'))
    return render_template("emailConfirm.html", form = form)

@app.route('/pass_reset', methods=['GET','POST'])
def reqpass_reset():
    if current_user.is_authenticated:
        token = s.dumps(current_user.email, salt='password-reset')
        msg = Message('password reset', sender='admin@chicagotouristinfo.org', recipients=[current_user.email])
        link = url_for('confpass_reset', token=token, _external=True)
        msg.body = "Your link is: {}".format(link)
        mail.send(msg)
        return redirect(url_for('user', user_id = current_user.id))
    form = RequestPassReset()
    if request.method == "POST" and form.validate():
        email = form.email.data
        if not User.query.filter(User.email.contains(email)).one_or_none():
            return redirect(url_for('reqpass_reset'))
        token = s.dumps(email, salt='password-reset')
        msg = Message('password reset', sender='admin@chicagotouristinfo.org', recipients=[email])
        link = url_for('confpass_reset', token=token, _external=True)
        msg.body = "Your link is: {}".format(link)
        mail.send(msg)
        return redirect(url_for('home'))
    return render_template("requestPass.html", form = form)

@app.route('/pass_reset/<token>', methods=['GET','POST'])
def confpass_reset(token):
    if current_user.is_authenticated:
        logout_user()
    email = s.loads(token, salt='password-reset', max_age=3600)
    form = ConfirmPassReset()
    if request.method == "POST" and form.validate():
        user = User.query.filter(User.email == email).first_or_404()
        password = form.password.data
        user.password = user.set_password(password)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('resetPass.html', form = form)


@app.route("/register/<token>", methods=["GET", "POST"])
def register(token):
    # if current_user.username:
    #     return redirect(url_for('logout'))
    email = s.loads(token, salt='email-confirm', max_age=3600)
    form = RegistrationForm()
    if request.method == "POST" and form.validate():

        # Gathering Form Data
        username = form.username.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        password = form.password.data
        print(username, firstname, lastname, email, password)
        # Add Form Data to User Model Class
        user = User(username, firstname, lastname, email, password)
        db.session.add(user) # Start communication with Database
        db.session.commit() # Will save data to Database
        logged_user = User.query.filter(User.email == email).first_or_404()
        if logged_user and check_password_hash(logged_user.password,password):
            login_user(logged_user)
            print(current_user.username)
            return redirect(url_for('home'))

    else:
        flash("Your form is missing some data!")
    return render_template('register.html', form = form, email = email)
    #return render_template('register.html', title='register', form = form)

@app.route("/addPost", methods =["GET","POST"])
@login_required
def post_article():
    print(current_user.username)
    form = ArticleForm()
    if request.method == "POST" and form.validate():
        title = form.title.data
        category = form.category.data
        author = current_user.username
        location = form.location.data
        article = form.article.data
        source = form.source.data
        print(title, category , current_user.username)
        photoList =[]
        for photo in form.photos.data:
            print(photo)

            target = os.path.join(basedir, "app_base/static/artimages/")
            if not os.path.isdir(target):
                os.mkdir(target)
            filename = secrets.token_hex(16)+".jpg"
            destination = "/".join([target,filename])
            print(destination)

            photo.save(destination)
            photoList.append(filename)

        articlePost = Article(title, category, author, article, location, source)
        articlePost.photopath = list_to_text(photoList)
        db.session.add(articlePost)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        flash("something went wrong")
    return render_template("addpost.html", form = form)

@app.route("/delete/<int:post_id>", methods=["GET","POST"])
@login_required
def deleteArticle(post_id):
    post = Article.query.filter_by(id=post_id).first_or_404()
    if current_user.username == post.author:
        target = os.path.join(basedir, "app_base/static/artimages/")
        if post.photopath:
            for photo in text_to_list(post.photopath):
                print(target+photo)
                if os.path.isfile(target+photo):
                    os.remove(target+photo)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('err401'))

    return render_template("main.html")



@app.route("/load")
@login_required
def load():
    return render_template ("upload.html")

@app.route('/upload',methods=["GET","POST"])
@login_required
def upload():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    file = request.files['inputFile']
    if file:
        target = os.path.join(basedir, "app_base/static/userimages/")
        if not os.path.isdir(target):
            os.mkdir(target)
        filename = random_hex = secrets.token_hex(16)+".jpg"
        destination = "/".join([target,filename])
        print(file)
        print(destination)
        size = (700,700)
        file = Image.open(file)
        file.thumbnail(size)
        file.save(destination)
        user.photourl = "../static/userimages/" + filename
        db.session.commit()
    else:
        return redirect(url_for("user",user_id = current_user.id ))

    return redirect(url_for("user",user_id = current_user.id ))

@app.route("/user/<int:user_id>", methods =["GET","POST"])
@login_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    if current_user.username == user.username:
        form = EditForm(formdata=request.form, obj=user)
        if request.method == "POST" and form.validate():
            form.populate_obj(post)
            db.session.commit()
    else:
        return redirect(url_for('err401'))

    return render_template("user.html", user = user, form = form)



@app.errorhandler(401)
def page_not_found(error):
   return render_template('401.html', title = '401'), 401

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

@app.errorhandler(500)
def page_not_found(error):
   return render_template('500.html', title = '500'), 500
