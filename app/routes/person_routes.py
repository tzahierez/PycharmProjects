# person_routes.py

from flask import Blueprint, request, render_template, redirect, url_for
from app import db
from app.models.exam import Student
from app.models.exam import Teacher

person_routes = Blueprint('person', __name__)


@person_routes.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Extract data from form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        # Other fields...

        # Create new Student object
        new_student = Student(first_name=first_name, last_name=last_name, email=email)
        # Add other fields as necessary

        # Add to database
        db.session.add(new_student)
        db.session.commit()

        # Redirect to a different page, or back to the form
        return redirect(url_for('person.add_student'))

    return render_template('add_student.html')


# In person_routes.py or similar file

@person_routes.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        # Extract data from form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        # Other fields...

        # Create new Teacher object
        new_teacher = Teacher(first_name=first_name, last_name=last_name, email=email)
        # Add other fields as necessary

        # Add to database
        db.session.add(new_teacher)
        db.session.commit()

        # Redirect or provide feedback
        return redirect(url_for('person.add_teacher'))

    return render_template('add_teacher.html')
