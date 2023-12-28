# app/models/exam.py
from datetime import datetime
import uuid  # Import UUID library
from app import db


class ExamTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(128), nullable=False)
    chapter = db.Column(db.String(128), nullable=True)
    question_count = db.Column(db.Integer, nullable=False)


class QuestionTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_template_id = db.Column(db.Integer, db.ForeignKey('exam_template.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    perfect_answer = db.Column(db.Text, nullable=False)
    evaluation_criteria = db.Column(db.Text, nullable=True)


class GradingCriteria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_template_id = db.Column(db.Integer, db.ForeignKey('question_template.id'), nullable=False)
    criteria = db.Column(db.Text, nullable=False)


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    externalId = db.Column(db.String(36), nullable=False, default=lambda: str(uuid.uuid4()))
    exam_template_id = db.Column(db.Integer, db.ForeignKey('exam_template.id'), nullable=False)
    student_email = db.Column(db.String(100), nullable=False)
    total_grade = db.Column(db.Integer, nullable=True)
    # Other metadata like timestamps can be added here


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    externalId = db.Column(db.String(36), nullable=False, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(15))
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Add creation time

    # ... [rest of the Student model] ...


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    externalId = db.Column(db.String(36), nullable=False, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(15))
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Add creation time


class StudentAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_template_id = db.Column(db.Integer, db.ForeignKey('exam_template.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    question_template_id = db.Column(db.Integer, db.ForeignKey('question_template.id'), nullable=False)
    student_answer = db.Column(db.Text, nullable=True)  # Text of student's answer
    ai_grade = db.Column(db.Float, nullable=True)  # AI's grade for the answer
    ai_grade_reason = db.Column(db.Text, nullable=True)  # AI's reason for the given grade
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#
#     def __init__(self, first_name, last_name, email, phone_number):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.phone_number = phone_number

# def __repr__(self):
#     return f'<Student {self.first_name} {self.last_name}>'
