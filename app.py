from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_peewee.utils import get_object_or_404
from model import *
import hashlib
from functools import wraps


app = Flask(__name__)
# set the secret key. keep this really secret:
app.secret_key = 'theSecretKey'


# ------------------------------------------------------------------------
# FLASK FUNCTIONS
@app.before_request
def before_request():
	# create db if needed and connect to it
	initialize_db()


@app.teardown_request
def teardown_request(exception):
	close_db()

def login_required(f):
	@wraps(f)
	def inner(*args, **kwargs):
		if not('username' in session) or session['username'] == None:
			return redirect(url_for('index'))
		else:
			return f(*args, **kwargs)
	return inner

def isAuthentic(username, password):
	try:
		user = User.select().where(User.username == username).get()
		if password == user.password:
			return True
		else:
			return False
	except User.DoesNotExist:
		return False

# ------------------------------------------------------------------------
@app.route('/')
def index():
	if 'username' in session and session['username'] != None:
		return redirect(url_for('home'))
	else:
		return(render_template('index.html'))

@app.errorhandler(404)
def pageNotFound(e):
	return render_template('404.html'), 404

@app.route('/home/')
@login_required
def home():
	courses = Course.select()
	return render_template('home.html', courses=courses)

@app.route('/classroom/<course_code>/')
@login_required
def classroom(course_code):
	course = get_object_or_404(Course, Course.code == course_code)
	meetings = Meeting.select().where(Meeting.course_id == course.id)
	resources = Resource.select().where(Resource.course_id == course.id)
	return render_template('classroom.html', course=course, meetings=meetings, resources=resources)

@app.route('/signup/')
def signup():
	return(render_template('signup.html'))

@app.route('/signin/', methods=['POST'])
def signin():

	if isAuthentic(request.form['username'], hashlib.md5(request.form['password'].encode('utf8')).hexdigest()):
		session['username'] = request.form['username']
		return redirect(url_for('home'))
	else:
		session['username'] = None
		return render_template('index.html', message="Username or password incorrect.")


@app.route('/logout/')
def logout():
	session['username'] = None
	return redirect(url_for('index'))

@app.route('/signup_action/', methods=['POST'])
def signup_action():
	try:
		with db.transaction():
			user = User.create(
				username=request.form['username'],
				password=hashlib.md5(request.form['password'].encode('utf8')).hexdigest(),
				fullname=request.form['fullname'],
				email=request.form['email']
			)
		# debugging purpose
		allUsers = User.select()
		for user in allUsers:
			print(user.username)
		# end of debugging purpose 
		return render_template('index.html', message="Sign up success. Please sign in.")
	except IntegrityError:
		return render_template('signup.html', message="Username has already been taken.")
# ------------------------------------------------------------------------
if __name__ == '__main__':
	app.run(debug=True)
# ------------------------------------------------------------------------
