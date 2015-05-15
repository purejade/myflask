from flask import Flask,render_template,session,redirect,url_for,flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from app.nameform import NameForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Look like you have changed your name')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),current_time = datetime.utcnow())

@app.route('/user/<username>')
def user(username):
    # name = 'hellp'
    # return 'Hello World!'
    return render_template('user.html',name=username,current_time = datetime.utcnow())



if __name__ == '__main__':
    print app.url_map
    app.run()
    # manager.run()