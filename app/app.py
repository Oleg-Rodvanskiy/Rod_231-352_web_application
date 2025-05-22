from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.modules.models import db, User, Role, VisitLog
from app.modules.forms import UserForm, ChangePasswordForm
# from decorators import check_rights
import csv
from io import StringIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

def get_app():
    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def log_visit():
    log_entry = VisitLog(path=request.path, user_id=current_user.id if current_user.is_authenticated else None)
    db.session.add(log_entry)
    db.session.commit()


@app.route('/')
@login_required
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(login=login).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Вы успешно вошли в систему.")
            return redirect(url_for('index'))
        flash("Неверный логин или пароль.")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы.")
    return redirect(url_for('login'))


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]  # Значения для выбора ролей
    if form.validate_on_submit():
        user = User(login=form.login.data,
                    last_name=form.last_name.data,
                    first_name=form.first_name.data,
                    patronymic=form.patronymic.data,
                    role_id=form.role_id.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Пользователь успешно создан!")
        return redirect(url_for('index'))
    return render_template('create_user.html', form=form)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = UserForm(obj=user)
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]

    if form.validate_on_submit():
        user.login = form.login.data
        user.last_name = form.last_name.data
        user.first_name = form.first_name.data
        user.patronymic = form.patronymic.data
        if form.password.data:
            user.set_password(form.password.data)
        user.role_id = form.role_id.data
        db.session.commit()
        flash("Пользователь успешно обновлён!")
        return redirect(url_for('index'))

    return render_template('edit_user.html', form=form, user=user)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Пользователь удален.")
    return redirect(url_for('index'))


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash("Пароль успешно изменен.")
            return redirect(url_for('index'))
        else:
            flash("Старый пароль неверен.")
    return render_template('change_password.html', form=form)


@app.route('/visit_log')
@login_required
def visit_log():
    logs = VisitLog.query.order_by(VisitLog.created_at.desc()).paginate(per_page=10)
    return render_template('visit_log.html', logs=logs)


@app.route('/report/pages')
@login_required
def report_pages():
    page_stats = db.session.query(VisitLog.path, db.func.count(VisitLog.id).label('count')) \
        .group_by(VisitLog.path) \
        .order_by(db.desc('count')).all()
    return render_template('report_pages.html', page_stats=page_stats)


@app.route('/report/users')
@login_required
def report_users():
    user_stats = db.session.query(User, db.func.count(VisitLog.id).label('count')) \
        .outerjoin(VisitLog) \
        .group_by(User.id) \
        .order_by(db.desc('count')).all()
    return render_template('report_users.html', user_stats=user_stats)


@app.route('/export/pages')
@login_required
def export_pages():
    page_stats = db.session.query(VisitLog.path, db.func.count(VisitLog.id).label('count')) \
        .group_by(VisitLog.path) \
        .order_by(db.desc('count')).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Страница', 'Количество посещений'])
    for record in page_stats:
        writer.writerow(record)

    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename="report_pages.csv"'
    }


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создать таблицы
    app.run(debug=True)