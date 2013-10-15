__author__ = 'Bolero'

from functools import wraps
from flask import Flask, request, url_for, redirect, g, session, render_template, flash
from app import db, app
from forms import AddTask, RegisterForm, LoginForm
from models import Ftasks, User
from sqlalchemy.exc import IntegrityError


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in %s field - %s" %(getattr(form, field).label.text, error), 'error')


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to be logged in.')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You are logged out.')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = User.query.filter_by(name=request.form['name'], password=request.form['password']).first()
        if u is None:
            error = 'Invalid credentials. Please try again'
        else:
            session['logged_in'] = True
            session['user_id'] = u.id
            return redirect(url_for('tasks'))
    return render_template('login.html', form=LoginForm(request.form), error=error)

@app.route('/tasks/')
@login_required
def tasks():
    open_tasks = db.session.query(Ftasks).filter_by(status='1').order_by(Ftasks.due_date.asc())
    closed_tasks = db.session.query(Ftasks).filter_by(status='0').order_by(Ftasks.due_date.asc())
    return render_template('tasks.html', form=AddTask(request.form), open_tasks=open_tasks, closed_tasks=closed_tasks)

#add new tasks
@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
    print 'new task'
    form = AddTask(request.form, csrf_enabled=False)
    print form.errors
    print form.is_submitted()
    print form.errors
    if request.method == 'POST' and form.validate():
        print 'here'
        new_task = Ftasks(form.name.data, form.due_date.data, form.priority.data, form.posted_date.data, '1',
                          session['user_id'])
        db.session.add(new_task)
        db.session.commit()
        flash('New entry was successful!')
    else:
        flash_errors(form)
    return redirect(url_for('tasks'))


#mark task as complete
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(Ftasks).filter_by(task_id=new_id).update({"status": "0"})
    db.session.commit()
    flash('The task was marked complete')
    return redirect(url_for('tasks'))

#delete task
@app.route('/delete/<int:task_id>',)
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(Ftasks).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash('The task is deleted')
    return redirect(url_for('tasks'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form, csrf_enabled = False)
    if form.validate_on_submit():
        new_user = User(form.name.data, form.email.data, form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for joining!')
            return redirect(url_for('login'))
        except IntegrityError:
            error = "The username and/or email already exists. Please try again"
    else:
        flash_errors(form)
    return render_template('register.html', form=form, error=error)


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(404)
def internal_error(error):
    db.session.rollback()
    return render_template('404.html'), 404