from app import app
from app.modules.models import db, User, Role, VisitLog

with app.get_app().app_context():
    db.create_all()