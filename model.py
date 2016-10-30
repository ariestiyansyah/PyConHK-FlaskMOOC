from peewee import *
import datetime


db = SqliteDatabase('minimoocdatabase.db')


class BaseModel(Model):
	class Meta:
		database = db


class User(BaseModel):
	id = PrimaryKeyField()
	username = CharField(unique=True)
	fullname = CharField()
	password = CharField()
	email = CharField()
	join_date = DateTimeField(default=datetime.datetime.now)


class Course(BaseModel):
	id = PrimaryKeyField()
	codex = CharField(unique=True)
	name = CharField()
	instructor = CharField()
	desc = TextField()


class Meeting(BaseModel):
	id = PrimaryKeyField()
	course_id = ForeignKeyField(Course)
	topic = CharField()
	desc = TextField()


class Resource(BaseModel):
	id = PrimaryKeyField()
	course_id = ForeignKeyField(Course)
	meeting_id = ForeignKeyField(Meeting)
	path = CharField()
	filename = CharField()


def initialize_db():
	db.connect()

	db.create_tables([User, Course, Meeting, Resource], safe=True)

	# populate_courses()
	# populate_meeting()
	# populate_resources()


    # Turn this on to rebuild database structures.
	# db.drop_tables([User, Course, Resource, Meeting], safe= False)


def close_db():
	db.close()


def populate_courses():
    Course.create(
    		id=1,
            code="CS50",
            name="Introduction to Computer Science",
            instructor="David J. Malan",
            desc="An introductory course to the foundation of Computer Science by David J. Malan"
    )

    Course.create(
    		id=2,
            code="NLP101",
            name="Introduction to Natural Language Processing",
            instructor="Dan Jurafsky",
            desc="An introductory course to the foundation of NLP."
    )



def populate_meeting():
	Meeting.create(
		id=1,
		course_id=1,
		topic='Introduction to Programming',
		desc='This is the first meeting for CS50'
	)
	Meeting.create(
		id=2,
		course_id=1,
		topic='Introduction to Programming (2)',
		desc='This is the second meeting for CS50'
	)
	Meeting.create(
		id=3,
		course_id=2,
		topic='Introduction to NLP',
		desc='This is the first meeting for CS50'
	)
	Meeting.create(
		id=4,
		course_id=2,
		topic='Introduction to NLP (2)',
		desc='This is the second meeting for CS50'
	)


def populate_resources():
	Resource.create(
		id=2,
		course_id=1,
		meeting_id = 1,
		path='resources/CS50/1/',
		filename='1.pdf'
	)
	Resource.create(
		id=3,
		course_id=1,
		meeting_id = 2,
		path='resources/CS50/2/',
		filename='2.mp4'
	)
	Resource.create(
		id=4,
		course_id=2,
		meeting_id = 3,
		path='resources/NLP101/1/',
		filename='1.mp4'
	)
	Resource.create(
		id=5,
		course_id=2,
		meeting_id = 3,
		path='resources/NLP101/1/',
		filename='1.pdf'
	)
	Resource.create(
		id=6,
		course_id=2,
		meeting_id = 4,
		path='resources/NLP101/2/',
		filename='2.mp4'
	)