from app import db, app  # Importing app
from models import User, Resource, Assignment, Submission, Note
from datetime import datetime, timedelta  # Importing timedelta

def seed():
    with app.app_context():  # Correcting the app context
        # Create users
        user1 = User(
            username='anis_abdi',
            email='anis170@gmail.com',  # Correcting the comma here
            password='password123',
            role='student',
            is_active=True
        )
        user2 = User(
            username='Ikran_Ali',
            email='ikran@example.com',
            password='password456',
            role='teacher',
            is_active=True
        )
        user3 = User(
            username='mikail_hassan',
            email='mikailismail260@gmail.com',
            password='mikail',
            role='admin',
            is_active=True
        )

        # Add users to the session
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)

        # Commit the user objects to the database
        db.session.commit()

        # Fetch the created users
        users = User.query.all()

        # Create resources
        resource1 = Resource(
            title='Sample Resource 1',
            description='This is a sample resource uploaded by Mikail Hassan.',
            uploaded_by=users[0].id,
            uploaded_at=datetime.utcnow()
        )
        resource2 = Resource(
            title='Sample Resource 2',
            description='This is a sample resource uploaded by ikran Ali.',
            uploaded_by=users[1].id,
            uploaded_at=datetime.utcnow()
        )

        # Add resources to the session
        db.session.add(resource1)
        db.session.add(resource2)

        # Commit changes to the database
        db.session.commit()

        # Create assignments
        assignment1 = Assignment(
            title='Sample Assignment 1',
            description='This is a sample assignment for students.',
            deadline=datetime.utcnow() + timedelta(days=7),  # Using timedelta to set deadline
            teacher_id=users[1].id,
            created_at=datetime.utcnow()
        )
        assignment2 = Assignment(
            title='Sample Assignment 2',
            description='This is another sample assignment for students.',
            deadline=datetime.utcnow() + timedelta(days=14),  # Using timedelta to set deadline
            teacher_id=users[1].id,
            created_at=datetime.utcnow()
        )

        # Add assignments to the session
        db.session.add(assignment1)
        db.session.add(assignment2)

        # Commit changes to the database
        db.session.commit()

        # Create notes
        note1 = Note(
            title='Introduction to the Command Line Interface',
            content='''\
            Introduction to the Command Line Interface
            ...
            ''',
            user_id=users[0].id,
            created_at=datetime.utcnow()
        )
        note2 = Note(
            title='Navigating Files and Directories in Bash',
            content='''\
            Navigating Files and Directories in Bash
            ...
            ''',
            user_id=users[1].id,
            created_at=datetime.utcnow()
        )

        # Add notes to the session
        db.session.add(note1)
        db.session.add(note2)

        # Commit changes to the database
        db.session.commit()

if __name__ == '__main__':
    seed()
