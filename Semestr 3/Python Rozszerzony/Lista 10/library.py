import json
import argparse
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, validates

# SQLAlchemy base model
Base = declarative_base()

# Models
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    specimens = relationship('Specimen', back_populates='book')

    @validates('author')
    def validate_author(self, key, author):
        if len(author) < 3:
            raise ValueError('Author name is too short')
        return author

class Specimen(Base):
    __tablename__ = 'specimens'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    condition = Column(String, nullable=False, default='New')

    book = relationship('Book', back_populates='specimens')
    borrowings = relationship('Borrowing', back_populates='specimen')

    @validates('condition')
    def validate_condition(self, key, condition):
        if condition not in ['New', 'Good', 'Fair', 'Poor']:
            raise ValueError("Condition must be one of: 'New', 'Good', 'Fair', 'Poor'")
        return condition

class Reader(Base):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    borrowings = relationship('Borrowing', back_populates='reader')

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")
        return email

class Borrowing(Base):
    __tablename__ = 'borrowings'

    id = Column(Integer, primary_key=True)
    specimen_id = Column(Integer, ForeignKey('specimens.id'), nullable=False)
    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=False)

    specimen = relationship('Specimen', back_populates='borrowings')
    reader = relationship('Reader', back_populates='borrowings')

# Database setup
def init_db(engine):
    Base.metadata.create_all(engine)

# Load initial data from JSON
def load_data(session, file_path='data.json'):
    with open(file_path, 'r') as f:
        data = json.load(f)

    for book in data.get('books', []):
        session.add(Book(**book))

    for reader in data.get('readers', []):
        session.add(Reader(**reader))

    for specimen in data.get('specimens', []):
        session.add(Specimen(**specimen))

    for borrowing in data.get('borrowings', []):
        session.add(Borrowing(**borrowing))

    session.commit()

# Command handlers
def add_book(session, title, author, year):
    book = Book(title=title, author=author, year=year)
    session.add(book)
    session.commit()
    print(f'Added book: {title}')

def add_reader(session, name, email):
    reader = Reader(name=name, email=email)
    session.add(reader)
    session.commit()
    print(f'Added new reader: {name}')

def add_specimen(session, book_id, condition):
    specimen = Specimen(book_id=book_id, condition=condition)
    session.add(specimen)
    session.commit()
    print(f'Added specimen for book ID {book_id} with condition {condition}')

def borrow_specimen(session, specimen_id, reader_id):
    specimen = session.query(Specimen).filter_by(id=specimen_id).first()
    reader = session.query(Reader).filter_by(id=reader_id).first()
    borrowing = session.query(Borrowing).filter_by(specimen_id=specimen_id).first()

    if not specimen or not reader:
        print("Invalid specimen or reader ID.")
        return
    
    if borrowing:
        print(f"This specimen {specimen_id} can't be borrowed")
        return

    borrowing = Borrowing(specimen_id=specimen_id, reader_id=reader_id)
    session.add(borrowing)
    session.commit()
    print(f"Specimen {specimen_id} borrowed by reader {reader.name}")

def return_specimen(session, specimen_id):
    borrowing = session.query(Borrowing).filter_by(specimen_id=specimen_id).first()

    if not borrowing:
        print("This specimen wasn't borrowed")
        return
    
    session.delete(borrowing)
    session.commit()
    print(f"Specimen: {specimen_id} was successfuly returned")

def list_books(session):
    books = session.query(Book).all()
    for book in books:
        print(f"{book.id}: {book.title} by {book.author} ({book.year})")

def list_readers(session):
    readers = session.query(Reader).all()
    for reader in readers:
        print(f"{reader.id}: {reader.name} ({reader.email})")

def list_specimens(session):
    specimens = session.query(Specimen).all()
    for specimen in specimens:
        status = "Borrowed" if specimen.borrowings else "Available"
        print(f"Specimen ID: {specimen.id}, Book ID: {specimen.book_id}, Condition: {specimen.condition}, Status: {status}")

def list_borrowings(session):
    borrowings = session.query(Borrowing).all()
    for borrowing in borrowings:
        specimen = session.query(Specimen).filter_by(id=borrowing.specimen_id).first()
        reader = session.query(Reader).filter_by(id=borrowing.reader_id).first()
        print(f"Borrowing ID: {borrowing.id}, Specimen ID: {borrowing.specimen_id} (Book ID: {specimen.book_id}), Borrowed by Reader: {reader.name} (Email: {reader.email})")

# Argument parser setup
def main():
    parser = argparse.ArgumentParser(description="Library Management System")

    parser.add_argument('entity', choices=['books', 'readers', 'specimens', 'borrowings'], help="Entity to manage")
    parser.add_argument('--add', action='store_true', help="Add a new entity")
    parser.add_argument('--list', action='store_true', help="List entities")
    parser.add_argument('--back', type=int, help="Return a speciment to library (requires specimen ID)")
    parser.add_argument('--borrow', type=int, help="Borrow a specimen (requires specimen ID and reader ID)")
    parser.add_argument('--title', type=str, help="Title of the book")
    parser.add_argument('--author', type=str, help="Author of the book")
    parser.add_argument('--year', type=int, help="Year of publication")
    parser.add_argument('--name', type=str, help="Name of the reader")
    parser.add_argument('--email', type=str, help="Email of the reader")
    parser.add_argument('--book-id', type=int, help="Book ID for specimen")
    parser.add_argument('--condition', type=str, help="Condition of the specimen")
    parser.add_argument('--reader-id', type=int, help="Reader ID for borrowing")

    args = parser.parse_args()

    # Database connection
    engine = create_engine('sqlite:///library.db')
    Session = sessionmaker(bind=engine)
    with Session() as session:
        init_db(engine)
        # load_data(session)

        if args.entity == 'books':
            if args.add:
                add_book(session, args.title, args.author, args.year)
            elif args.list:
                list_books(session)

        elif args.entity == 'readers':
            if args.add:
                add_reader(session, args.name, args.email)
            elif args.list:
                list_readers(session)

        elif args.entity == 'specimens':
            if args.add:
                add_specimen(session, args.book_id, args.condition)
            elif args.list:
                list_specimens(session)

        elif args.entity == 'borrowings':
            if args.borrow and args.reader_id:
                borrow_specimen(session, args.borrow, args.reader_id)
            elif args.list:
                list_borrowings(session)
            elif args.back:
                return_specimen(session, args.back)

if __name__ == '__main__':
    main()
