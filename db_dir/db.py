import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# Модель пользователя
class User(Base):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(50))
    last_name = db.Column('last_name', db.String(80), nullable=False)
    email = db.Column(
        'email', db.String(100),
        db.CheckConstraint("email LIKE '%@%'"), nullable=False
    )
    phone_number = db.Column('phone_number', db.String(12), nullable=False)
    birth_day = db.Column('birth_day', db.Date, nullable=False)
    status = db.Column('status', db.String(25))
    db.UniqueConstraint('email', 'phone_number')

    def __str__(self):
        return f'Имя {self.first_name} - Фамилия{self.last_name}'
    query: db.sql.select
