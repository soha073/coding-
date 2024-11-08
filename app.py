from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Problem, Submission
from forms import RegistrationForm, LoginForm
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    problems = Problem.query.all()
    return render_template('index.html', problems=problems)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password_hash=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password_hash == form.password.data:  # For simplicity, do not use plain text
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/submit/<int:problem_id>', methods=['GET', 'POST'])
def submit(problem_id):
    if request.method == 'POST':
        code = request.form['code']
        # Here you would ideally run the code in a safe environment
        result = run_code(code)  # Placeholder for code execution
        submission = Submission(user_id=1, problem_id=problem_id, code=code, result=result)  # User ID hardcoded for demo
        db.session.add(submission)
        db.session.commit()
        flash('Code submitted!', 'success')
        return redirect(url_for('index'))
    problem = Problem.query.get_or_404(problem_id)
    return render_template('problem.html', problem=problem)

def run_code(code):
    # This is a placeholder function; implement code execution in a secure way
    return "Executed successfully"

if __name__ == '__main__':
    app.run(debug=True)


