from flask import Blueprint, render_template, request, redirect, url_for, session
from .quiz_engine import generate_quiz_question

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        session['category'] = request.form['category']
        session['continent'] = request.form['continent']
        session['difficulty'] = request.form['difficulty']
        return redirect(url_for('main.quiz'))
    return render_template('settings.html')

@main.route('/quiz')
def quiz():
    question_data = generate_quiz_question(
        session['category'],
        session['continent'],
        session['difficulty']
    )
    session['question'] = question_data
    return render_template('quiz.html', data=question_data)

@main.route('/result', methods=['POST'])
def result():
    selected = request.form.get('selected')
    correct = session['question']['correct']
    is_correct = (selected == correct)
    return render_template('result.html', correct=correct, is_correct=is_correct,
                           details=session['question']['details'])
