from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"
    # Add validations and constraints

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"

    # Validate  name
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required for an Author")
        if Author.query.filter_by(name=name).first() is not None:
            raise ValueError("Author with this name already exists.")
        return name

    # Validate phone_number
    @validates("phone_number")
    def validate_phone_number(self, key, value):
        # Check if the phone number has exactly 10 digits
        if value and not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return value


class Post(db.Model):
    __tablename__ = "posts"
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(), nullable=False)
    summary = db.Column(db.String(length=250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})"

    # Validate  category
    @validates("category")
    def validate_category(self, key, value):
        valid_categories = ["Fiction", "Non-Fiction"]
        if value not in valid_categories:
            raise ValueError(f"Categories must be one of: {'. '.join(valid_categories)}")

        return value

    # Custom validate title
    @validates("title")
    def validate_title(self, key, value):
        valid_titles = ["Won't Believe", "Secret", "Top", "Guess"]
        if value not in valid_titles:
            raise ValueError(f"Title must be sufficiently clickbait-y with: {'. '.join(valid_titles)}")
