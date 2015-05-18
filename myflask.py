from flask import Flask,render_template,session,redirect,url_for,flash
from flask.ext.script import Manager
from flask.ext.script import Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate,MigrateCommand
from flask.ext.mail import Mail
import os
from app.nameform import NameForm
# from app.mail import send_email
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'  #web form
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config["MAIL_SERVER"] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] =  os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
mail = Mail(app)

class Role(db.Model):
    __tablename__ =  'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    # users = db.relationship('user',backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    # role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command("shell",Shell(make_context=make_shell_context))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'),500
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = os.environ.get('FLASKY_MAIL_SENDER')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
from flask.ext.mail import Message

def send_sync_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    msg = Message(app.config["FLASKY_MAIL_SUBJECT_PREFIX"]+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    # mail.send(msg)
    thr = Thread(target=send_sync_email,args=[app,msg])
    thr.start()
    return thr



@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.name.data).first()
            if user is None:
                user = User(username=form.name.data)
                db.session.add(user)
                db.session.commit()
                session['known'] = False
                if app.config['FLASKY_ADMIN']:
                    send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
            else:
                session['known'] = True
        except Exception as e:
            print str(e)

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),current_time = datetime.utcnow(),known= session.get('known',False))

@app.route('/user/<username>')
def user(username):
    # name = 'hellp'
    # return 'Hello World!'
    return render_template('user.html',name=username,current_time = datetime.utcnow())



if __name__ == '__main__':
    print app.url_map
    # app.run()
    manager.run()