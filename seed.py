from models import db, User, Category, Expense
from app import app

def seeding():
    # Create sample users
    user1 = User(username='user1', email='user1@example.com', password='password1')
    user2 = User(username='user2', email='user2@example.com', password='password2')

    # Create sample categories
    category1 = Category(name='Food')
    category2 = Category(name='Transportation')
    category3 = Category(name='Entertainment')

    # Create sample expenses
    expense1 = Expense(name='Lunch', amount=15.99, user=user1, category=category1)
    expense2 = Expense(name='Gas', amount=35.75, user=user1, category=category2)
    expense3 = Expense(name='Movie', amount=12.50, user=user2, category=category3)

    # Add users, categories, and expenses to the database
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.add(expense1)
    db.session.add(expense2)
    db.session.add(expense3)

    # Commit the changes to the database
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seeding()

print('Sample data added to the database.')
