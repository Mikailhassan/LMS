from flask import Blueprint, request, jsonify
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from models import User, Resource, Assignment, Submission, Note, db
from datetime import datetime, timedelta

# Initialize Flask-Mail
mail = Mail()


# Initialize Flask-JWT-Extended
jwt = JWTManager()

# Blueprint for resources
resources_bp = Blueprint('resources', __name__)

# Example of sending email
def send_registration_email(email):
    msg = Message('Registration Confirmation', recipients=[email])
    msg.body = 'Thank you for registering with us!'
    # Send email
    mail.send(msg)

# Registration endpoint
@resources_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    if not all([username, email, password, role]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_user = User(username=username, email=email, password=password, role=role, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    send_registration_email(email)
    
    return jsonify({'message': 'User registered successfully'}), 201

# Login endpoint
@resources_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Endpoint to fetch resources
@resources_bp.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    resource_data = [{'title': resource.title, 'description': resource.description} for resource in resources]
    return jsonify(resource_data), 200

# Endpoint to handle assignments
@resources_bp.route('/assignments', methods=['POST'])
def handle_assignment():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    deadline = data.get('deadline')
    teacher_id = data.get('teacher_id')
    
    if not all([title, description, deadline, teacher_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_assignment = Assignment(title=title, description=description, deadline=deadline, teacher_id=teacher_id)
    new_assignment.save()  # Assuming there's a save method in the Assignment model to save to the database
    
    return jsonify({'message': 'Assignment created successfully'}), 201

# Endpoint to grade assignments
@resources_bp.route('/assignments/<int:assignment_id>/grade', methods=['PUT'])
def grade_assignment(assignment_id):
    data = request.json
    submission_id = data.get('submission_id')
    grade = data.get('grade')
    
    if not all([submission_id, grade]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    submission = Submission.query.get(submission_id)
    if submission:
        submission.grade = grade
        submission.save()  # Assuming there's a save method in the Submission model to save to the database
        return jsonify({'message': 'Assignment graded successfully'}), 200
    else:
        return jsonify({'error': 'Submission not found'}), 404

# CRUD operations for administrators
# These endpoints should be protected with authentication middleware

# Endpoint to create a new resource
@resources_bp.route('/admin/resources', methods=['POST'])
@jwt_required()
def create_resource():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    
    if not all([title, description]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Get the current user who uploaded the resource
    current_user = get_jwt_identity()
    
    new_resource = Resource(title=title, description=description, uploaded_by=current_user)
    db.session.add(new_resource)
    db.session.commit()
    
    return jsonify({'message': 'Resource created successfully'}), 201

# Endpoint to update an existing resource
@resources_bp.route('/admin/resources/<int:resource_id>', methods=['PUT'])
@jwt_required()
def update_resource(resource_id):
    data = request.json
    title = data.get('title')
    description = data.get('description')
    
    if not all([title, description]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    resource = Resource.query.get(resource_id)
    if resource:
        resource.title = title
        resource.description = description
        resource.save()  # Assuming there's a save method in the Resource model to save to the database
        return jsonify({'message': 'Resource updated successfully'}), 200
    else:
        return jsonify({'error': 'Resource not found'}), 404

# Endpoint to delete a resource
@resources_bp.route('/admin/resources/<int:resource_id>', methods=['DELETE'])
@jwt_required()
def delete_resource(resource_id):
    resource = Resource.query.get(resource_id)
    if resource:
        resource.delete()  # Assuming there's a delete method in the Resource model to delete from the database
        return jsonify({'message': 'Resource deleted successfully'}), 200
    else:
        return jsonify({'error': 'Resource not found'}), 404
# Define auth resource
@resources_bp.route('/auth', methods=['GET'])
@jwt_required()
def auth_resource():
    return jsonify({'message': 'Authentication successful'}), 200
    
