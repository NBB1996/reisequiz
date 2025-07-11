from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')

@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    return render_template('quiz.html')

@main.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')