from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

    def __repr__(self):
        return f'<Category: {self.name_category}>'


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)

    def __repr__(self):
        return f'<Resource: {self.name_resourse}>'
