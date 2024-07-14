from app import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), nullable=False)
    is_human = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Vote {self.session_id} - {"Human" if self.is_human else "AI"}>'
