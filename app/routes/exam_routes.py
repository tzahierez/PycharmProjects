from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from app import db
from app.clients import openai_client
from app.clients.openai_client import OpenAiClient
from app.models.exam import ExamTemplate, QuestionTemplate, Exam, GradingCriteria, \
    StudentAnswer  # Make sure these are imported correctly
from openai import OpenAI
import os

exam_routes = Blueprint('exam', __name__)
openai_client = OpenAiClient()


# @exam_routes.route('/create_exam_template', methods=['GET', 'POST'])
# def create_exam_template():
#     if request.method == 'POST':
#         # Real database interaction
#         course = request.form.get('course')
#         subject = request.form.get('subject')
#         chapter = request.form.get('chapter')
#         question_count = int(request.form.get('question_count'))
#
#         new_exam_template = ExamTemplate(course=course, subject=subject, chapter=chapter, question_count=question_count)
#         db.session.add(new_exam_template)
#         db.session.commit()  # In reality, you should handle exceptions and rollback if necessary
#         return redirect(url_for('exam.view_exam', exam_id=new_exam_template.id))
#     return render_template('create_exam_template.html')

# this is the enrty point - http://127.0.0.1:5000/exam/create_exam_template
@exam_routes.route('/create_exam_template', methods=['GET', 'POST'])
def create_exam_template():
    if request.method == 'POST':
        # Extract the basic information from the form
        course = request.form.get('course')
        subject = request.form.get('subject')
        chapter = request.form.get('chapter')
        question_count = int(request.form.get('question_count'))

        # Create placeholders for each question
        questions = [{'question_text': '', 'suggested_answer': '', 'evaluation_criteria': ''} for _ in
                     range(question_count)]

        return render_template('create_exam_template.html', course=course, subject=subject, chapter=chapter,
                               questions=questions, step=2)

    # Initial rendering of the page
    return render_template('create_exam_template.html', step=1)


@exam_routes.route('/exams_list', methods=['GET'])
def exams_list():
    exam_templates = ExamTemplate.query.all()
    exams_data = []
    for exam_template in exam_templates:
        questions = QuestionTemplate.query.filter_by(exam_template_id=exam_template.id).all()
        exam_data = {
            'id': exam_template.id,
            'title': exam_template.course,
            'subject': exam_template.subject,
            'questions': questions
        }
        exams_data.append(exam_data)
    return render_template('exams_list.html', exams_data=exams_data)


@exam_routes.route('/generate_questions', methods=['POST'])
def generate_questions():
    # Extract data from the form submission
    course = request.form['course']
    subject = request.form['subject']
    chapter = request.form['context']
    number_of_questions = int(request.form['number_of_questions'])

    questions_to_answer_pairs = openai_client.generate_question_to_answer_pairs(course, subject, chapter, number_of_questions)
    print(questions_to_answer_pairs)

    # Generate dummy questions and answers
    questions_and_answers = [
        {
            'question': f"Dummy question {i+1}",
            'answer': f"Dummy answer {i+1}"
        } for i in range(number_of_questions)
    ]

    # questions_to_answer_pairs = [{'answer': 'dummy ans1', 'question': 'dummy question1?'},
    #  {'answer': 'dummy ans2.', 'question': 'dummy question2?'},
    #  {'answer': 'dummy ans3.', 'question': 'dummy question2?'}]
    # Return the questions and answers as JSON
    return jsonify(questions_to_answer_pairs)

@exam_routes.route('/save_exam', methods=['POST'])
def save_exam():
    # Assuming you pass the exam ID in some way, e.g., hidden field in form
    exam_id = request.form.get('exam_id')
    exam = ExamTemplate.query.get_or_404(exam_id)

    # Loop through the form keys to find ones that start with 'answer'
    for key in request.form.keys():
        if key.startswith('answer'):
            # Extract the number from the key
            _, number = key.split('answer')
            try:
                question_number = int(number)  # Convert the number part to an integer
            except ValueError:
                # Handle the case where the conversion fails
                continue

            # Fetch the question using the number
            question = QuestionTemplate.query.get(question_number)
            if question:
                # Get the answer from the form
                question.answer = request.form.get(key)
                # Get the evaluation criteria if needed
                question.evaluation_criteria = request.form.get(f'evaluation_criteria{question_number}')

                db.session.add(question)

    # Commit the changes to the database
    db.session.commit()

    return redirect(url_for('exam.exams_list'))  # Redirect to the desired endpoint


@exam_routes.route('/save_exam_template', methods=['POST'])
def save_exam_template():
    # Extract data from request
    course = request.form.get('course')
    subject = request.form.get('subject')
    chapter = request.form.get('chapter')
    number_of_questions = request.form.get('number_of_questions')
    questions = request.form.getlist('questions[]')
    # ... other data ...

    # Create and save the exam template
    new_exam_template = ExamTemplate(course=course, subject=subject, chapter=chapter, question_count=number_of_questions)
    db.session.add(new_exam_template)
    db.session.flush()
    # Add questions here as well

    # Add questions here as well
    for i in range(int(number_of_questions)):
        question_data = {
            'question': request.form.get(f'questions[{i}][question]'),
            'answer': request.form.get(f'questions[{i}][answer]'),
            'evaluation_criteria': request.form.get(f'questions[{i}][evaluation_criteria]')
        }
        question = QuestionTemplate(
            exam_template_id=new_exam_template.id,
            question_text=question_data['question'],
            perfect_answer=question_data['answer'],
            evaluation_criteria=question_data['evaluation_criteria']
        )
        db.session.add(question)

    db.session.commit()

    # Return a success message with the new exam template ID
    return jsonify({
        'status': 'success',
        'course': course,
        'subject': subject,
        'exam_template_id': new_exam_template.id
    })


@exam_routes.route('/exam/<int:exam_id>', methods=['GET'])
def view_exam(exam_id):
    # Real fetching exam data
    exam = ExamTemplate.query.get_or_404(exam_id)
    questions = QuestionTemplate.query.filter_by(exam_template_id=exam_id).all()
    return render_template('view_exam.html', exam=exam, questions=questions)


@exam_routes.route('/view_test/<int:exam_template_id>', methods=['GET'])
def view_test(exam_template_id):
    # Fetch the exam template
    exam_template = ExamTemplate.query.get_or_404(exam_template_id)

    # Fetch the questions associated with the exam template
    questions = QuestionTemplate.query.filter_by(exam_template_id=exam_template_id).all()

    # Render a template to display the exam and its questions
    return render_template('view_exam.html', exam_template=exam_template, questions=questions)


@exam_routes.route('/submit_test/<int:exam_template_id>', methods=['POST'])
def submit_test(exam_template_id):
    # Fetch the student's email from the form
    student_email = request.form.get('student_email')

    # Create a new Exam instance
    new_exam = Exam(exam_template_id=exam_template_id, student_email=student_email)
    db.session.add(new_exam)
    db.session.flush()  # Flush to assign an ID to new_exam

    # Loop through the submitted answers
    for question_id, answer_text in request.form.items():
        if question_id.startswith('question_'):
            # Extract question ID and save the answer
            question_id_num = int(question_id.split('_')[1])
            student_answer = StudentAnswer(
                exam_template_id = exam_template_id,
                exam_id = new_exam.id,
                question_template_id=question_id_num,
                student_answer=answer_text
            )
            db.session.add(student_answer)

    # Commit the answers and the new exam to the database
    db.session.commit()

    # Redirect to a confirmation page
    return redirect(url_for('exam.confirmation_page', exam_id=new_exam.id))


@exam_routes.route('/confirmation_page/<int:exam_id>', methods=['GET'])
def confirmation_page(exam_id):
    return render_template('confirmation_page.html', exam_id=exam_id)

@exam_routes.route('/submit_answers', methods=['POST'])
def submit_answers():
    # Real submission of student answers
    # Process the form data and save the answers to the database
    # ...
    return jsonify({'status': 'success', 'message': 'Answers submitted successfully'})


@exam_routes.route('/review_exam/<int:exam_id>', methods=['GET'])
def review_exam(exam_id):
    # Real review data
    exam = ExamTemplate.query.get_or_404(exam_id)
    # Fetch submissions and any associated data
    # ...
    return render_template('review_exam.html', exam=exam)


@exam_routes.route('/grade_exam/<int:exam_id>', methods=['GET'])
def grade_exam(exam_id):
    # Real grading data
    # Fetch the exam, questions, and student answers, then grade them according to the criteria
    # ...
    return jsonify({'status': 'success', 'message': 'Grades submitted successfully'})


# run with:   curl -X POST http://localhost:5000/exam/chat -H "Content-Type: application/json" -d '{"text": "Hello, how are you?"}'
@exam_routes.route('/chat', methods=['POST'])
def chat():
    try:
    # Extract text from the incoming JSON request
        data = request.json
        user_input = data.get('text')
        user_id = data.get('user_id', 'default_user')  # You should pass a unique user_id with each request

        # Retrieve the existing conversation context if it exists
        conversation_history = '' #session_contexts.get(user_id, [])

        # OPENAI_API_KEY=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   ( replaced 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)
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        print('sending req to gpt ', conversation_history)
        # Call OpenAI GPT-3.5-turbo API using the updated API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the GPT-3.5-turbo model
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_input}]
        )
        print('got response from gpt')
        # Extract the response text
        response_text = response.choices[0].message.content  # Accessing the 'content' attribute directly

        # Return the response text as JSON
        return jsonify({'response': response_text})
    except Exception as e:
        print("Error during API call:", e)
        return str(e)  # or handle the error appropriately


@exam_routes.route('/validate_exam', methods=['GET', 'POST'])
def validate_exam():
    if request.method == 'POST':
        exam_id = request.form.get('exam_id')
        exam = Exam.query.get_or_404(exam_id)
        exam_template_id = exam.exam_template_id
        exam_template = ExamTemplate.query.get_or_404(exam_template_id)

        questions = QuestionTemplate.query.filter_by(exam_template_id=exam_template_id).all()
        student_answers = StudentAnswer.query.filter_by(exam_id=exam_id).all()

        if len(questions) != len(student_answers):
            return "Mismatch in the number of questions and student answers."

        evaluations = []
        for question, answer in zip(questions, student_answers):
            evaluation = evaluate_student_answers_with_gpt(
                course_name=exam_template.course,
                question=question.question_text,
                perfect_answer=question.perfect_answer,
                evaluation_criteria=question.evaluation_criteria,
                student_answer=answer.student_answer
            )
            evaluations.append({
                'question_text': question.question_text,
                'student_answer': answer.student_answer,
                'evaluation': evaluation
            })

        # Pass the evaluations to the template for rendering
        return render_template('exam_evaluation_results.html', evaluations=evaluations, exam_id=exam_id)

    # GET request - render the validation form
    return render_template('validate_exam.html')


def evaluate_student_answers_with_gpt(course_name, question, perfect_answer, evaluation_criteria, student_answer):
    prompt = (
        f"Course: {course_name}\n"
        f"Question: {question}\n"
        f"Perfect Answer: {perfect_answer}\n"
        f"Evaluation Criteria: {evaluation_criteria}\n"
        f"Student Answer: {student_answer}\n\n"
        f"Based on the criteria, evaluate the student's answer. Provide a grade on a scale of 0 to 100 and feedback:"
    )

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


@exam_routes.route('/test')
def test_route():
    return 'Test route is working'
