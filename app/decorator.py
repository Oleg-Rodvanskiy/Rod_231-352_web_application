from functools import wraps
from flask import redirect, flash, url_for
from flask_login import current_user


def check_rights(required_role):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Вы должны войти в систему.", "danger")
                return redirect(url_for('login'))

            if current_user.role.name != required_role and current_user.role.name != "Администратор":
                flash("У вас недостаточно прав для доступа к данной странице.", "danger")
                return redirect(url_for('index'))

            return func(*args, **kwargs)

        return wrapped

    return decorator