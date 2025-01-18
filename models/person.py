from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db

class Person(db.Model):
    __tablename__ = 'person'
    
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    activated = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(255), nullable=True)

    def __init__(self, login, email, password, role="user"):
        """
        Initializes a new Person object.
        
        :param login: The login name for the user.
        :param password: The raw password (will be hashed).
        :param role: The role assigned to the user (default is "user").
        """
        self.login = login
        self.email = email
        self.set_password(password)  # Używamy set_password do hashowania hasła
        self.role = role

    def set_confirmation_token(self, token):
        """Zapisuje nowy token do bazy."""
        self.confirmation_token = token
        db.session.commit()

    def __repr__(self):
        return f"<Person {self.login}>"
    
    def has_role(self, role):
        """Checks if the user has a specific role."""
        return self.role == role

    def set_password(self, password):
        """Hashes and sets the password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifies the password against the stored hash."""
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        """Returns a dictionary representation of the Person."""
        return {
            "id": self.id,
            "login": self.login,
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }
    
    
    
