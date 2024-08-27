from flask import Flask, render_template, flash, redirect, url_for, jsonify
from forms import RegistrationForm, LoginForm, TaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task-manager.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # `tasks = db.relationship('Task', backref='owner', lazy=True)` creates a link to all tasks of a person,
    # labels each task with the owner, and only fetches tasks when needed.
    tasks = db.relationship('Task', backref='owner', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.String(50), nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Ensure the User Loader is Defined
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# MAIN HOME ROUTE
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


# REGISTRATION ROUTE
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(password=form.password.data, method='pbkdf2:sha256:600000')

        new_user = User(username=form.username.data, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('success'))

    return render_template('register.html', title='Register', form=form)

@app.route('/success')
def success():
    return render_template('success.html')


# LOGIN ROUTE
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            priority=form.priority.data,
            deadline=form.deadline.data,
            owner=current_user
        )
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('dashboard'))

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks, form=form)


@app.route('/edit_task/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm()

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.category = form.category.data
        task.priority = form.priority.data
        task.deadline = form.deadline.data
        db.session.commit()
        return redirect(url_for('dashboard'))

    return redirect(url_for('dashboard'))


@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Ensure that the task belongs to the current user
    if task.owner != current_user:
        flash('You are not authorized to delete this task.', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted!', 'success')
    return redirect(url_for('dashboard'))



@app.route('/task-details/<int:task_id>', methods=['GET'])
@login_required
def task_details(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify({
            'title': task.title,
            'description': task.description,
            'category': task.category,
            'priority': task.priority,
            'deadline': task.deadline
        })
    else:
        return jsonify({'error': 'Task not found'}), 404


@app.route('/toggle-task-completion/<int:task_id>', methods=['POST'])
@login_required
def toggle_task_completion(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Ensure that the task belongs to the current user
    if task.owner != current_user:
        return jsonify({'success': False, 'message': 'Not authorized'})

    task.is_completed = not task.is_completed
    db.session.commit()
    
    return jsonify({'success': True})



@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
