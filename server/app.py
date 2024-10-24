from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Create the Flask application
app = Flask(__name__)

# Configuration
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:ragu 16-10-2004@localhost/admin_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Load configuration into the app
app.config.from_object(Config)

# Initialize the database
db = SQLAlchemy(app)

# Define the unified User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Hashed password
    role = db.Column(db.String(50), nullable=False)  # Role: supersuperadmin, superadmin, admin, coordinator, member

# Define models for specific roles
class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_super_admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Link to User table

class Branch(db.Model):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Link to User table

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Link to User table

class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Hashed password
    coordinator_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Link to User table

# Utility function to add user to `user` table
def add_user_to_user_table(name, password, role):
    """Utility function to add a new user to the user table."""
    hashed_password = generate_password_hash(password)
    new_user = User(name=name, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

# CRUD for SuperSuperAdmin (Organizations)
@app.route('/supersuperadmins/<int:supersuperadmin_id>/organizations', methods=['GET'])
def get_organizations(supersuperadmin_id):
    organizations = Organization.query.filter_by(super_super_admin_id=supersuperadmin_id).all()
    return jsonify([{'id': org.id, 'name': org.name} for org in organizations]), 200

@app.route('/supersuperadmins/<int:supersuperadmin_id>/organizations', methods=['POST'])
def create_organization(supersuperadmin_id):
    data = request.json
    new_org = Organization(name=data['name'], super_super_admin_id=supersuperadmin_id)
    db.session.add(new_org)
    db.session.commit()
    return jsonify({'id': new_org.id, 'name': new_org.name}), 201

@app.route('/organizations/<int:org_id>', methods=['PUT'])
def update_organization(org_id):
    organization = Organization.query.get_or_404(org_id)
    data = request.json
    organization.name = data.get('name', organization.name)
    db.session.commit()
    return jsonify({'id': organization.id, 'name': organization.name}), 200

@app.route('/organizations/<int:org_id>', methods=['DELETE'])
def delete_organization(org_id):
    organization = Organization.query.get_or_404(org_id)
    db.session.delete(organization)
    db.session.commit()
    return jsonify({'message': 'Organization deleted'}), 204


# CRUD for SuperAdmin (Branches)
@app.route('/superadmins/<int:superadmin_id>/branches', methods=['GET'])
def get_branches(superadmin_id):
    branches = Branch.query.filter_by(super_admin_id=superadmin_id).all()
    return jsonify([{'id': branch.id, 'name': branch.name} for branch in branches]), 200

@app.route('/superadmins/<int:superadmin_id>/branches', methods=['POST'])
def create_branch(superadmin_id):
    data = request.json
    new_branch = Branch(name=data['name'], super_admin_id=superadmin_id)
    db.session.add(new_branch)
    db.session.commit()
    return jsonify({'id': new_branch.id, 'name': new_branch.name}), 201

@app.route('/branches/<int:branch_id>', methods=['PUT'])
def update_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    data = request.json
    branch.name = data.get('name', branch.name)
    db.session.commit()
    return jsonify({'id': branch.id, 'name': branch.name}), 200

@app.route('/branches/<int:branch_id>', methods=['DELETE'])
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    return jsonify({'message': 'Branch deleted'}), 204


# CRUD for Admin (Departments)
@app.route('/admins/<int:admin_id>/departments', methods=['GET'])
def get_departments(admin_id):
    departments = Department.query.filter_by(admin_id=admin_id).all()
    return jsonify([{'id': department.id, 'name': department.name} for department in departments]), 200

@app.route('/admins/<int:admin_id>/departments', methods=['POST'])
def create_department(admin_id):
    data = request.json
    new_department = Department(name=data['name'], admin_id=admin_id)
    db.session.add(new_department)
    db.session.commit()
    return jsonify({'id': new_department.id, 'name': new_department.name}), 201

@app.route('/departments/<int:department_id>', methods=['PUT'])
def update_department(department_id):
    department = Department.query.get_or_404(department_id)
    data = request.json
    department.name = data.get('name', department.name)
    db.session.commit()
    return jsonify({'id': department.id, 'name': department.name}), 200

@app.route('/departments/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    return jsonify({'message': 'Department deleted'}), 204


# CRUD for Coordinator (Members)
@app.route('/coordinators/<int:coordinator_id>/members', methods=['GET'])
def get_members(coordinator_id):
    members = Member.query.filter_by(coordinator_id=coordinator_id).all()
    return jsonify([{'id': member.id, 'name': member.name} for member in members]), 200

@app.route('/coordinators/<int:coordinator_id>/members', methods=['POST'])
def create_member(coordinator_id):
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    new_member = Member(
        name=data['name'],
        password=hashed_password,
        coordinator_id=coordinator_id
    )
    db.session.add(new_member)
    db.session.commit()

    # Add to User table
    add_user_to_user_table(new_member.name, data['password'], 'Member')

    return jsonify({'id': new_member.id, 'name': new_member.name}), 201

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    member = Member.query.get_or_404(member_id)
    data = request.json
    member.name = data.get('name', member.name)
    if 'password' in data:
        member.password = generate_password_hash(data['password'])  # Hashing password
    db.session.commit()
    return jsonify({'id': member.id, 'name': member.name}), 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted'}), 204


# Main entry point for running the app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)












# from flask import Flask, jsonify, request, abort
# from flask_sqlalchemy import SQLAlchemy

# # Create the Flask application
# app = Flask(__name__)

# # Configuration
# class Config:
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:ragu 16-10-2004@localhost/admin_db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# # Load configuration into the app
# app.config.from_object(Config)

# # Initialize the database
# db = SQLAlchemy(app)

# # Define your models
# class Organization(db.Model):
#     __tablename__ = 'organization'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     super_super_admin_id = db.Column(db.Integer, db.ForeignKey('supersuperadmin.id'))

# class SuperSuperAdmin(db.Model):
#     __tablename__ = 'supersuperadmin'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)

# class Branch(db.Model):
#     __tablename__ = 'branch'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     super_admin_id = db.Column(db.Integer, db.ForeignKey('superadmin.id'))

# class SuperAdmin(db.Model):
#     __tablename__ = 'superadmin'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)

# class Department(db.Model):
#     __tablename__ = 'department'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

# class Admin(db.Model):
#     __tablename__ = 'admin'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)

# class Coordinator(db.Model):
#     __tablename__ = 'coordinator'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)

# class Member(db.Model):
#     __tablename__ = 'member'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     coordinator_id = db.Column(db.Integer, db.ForeignKey('coordinator.id'))


# # CRUD for Organizations
# @app.route('/supersuperadmins/<int:supersuperadmin_id>/organizations', methods=['GET'])
# def get_organizations(supersuperadmin_id):
#     organizations = Organization.query.filter_by(super_super_admin_id=supersuperadmin_id).all()
#     return jsonify([{'id': org.id, 'name': org.name} for org in organizations]), 200

# @app.route('/supersuperadmins/<int:supersuperadmin_id>/organizations', methods=['POST'])
# def create_organization(supersuperadmin_id):
#     data = request.json
#     new_org = Organization(name=data['name'], super_super_admin_id=supersuperadmin_id)
#     db.session.add(new_org)
#     db.session.commit()
#     return jsonify({'id': new_org.id, 'name': new_org.name}), 201

# @app.route('/organizations/<int:org_id>', methods=['PUT'])
# def update_organization(org_id):
#     organization = Organization.query.get_or_404(org_id)
#     data = request.json
#     organization.name = data.get('name', organization.name)
#     db.session.commit()
#     return jsonify({'id': organization.id, 'name': organization.name}), 200

# @app.route('/organizations/<int:org_id>', methods=['DELETE'])
# def delete_organization(org_id):
#     organization = Organization.query.get_or_404(org_id)
#     db.session.delete(organization)
#     db.session.commit()
#     return jsonify({'message': 'Organization deleted'}), 204


# # CRUD for Branches
# @app.route('/superadmins/<int:superadmin_id>/branches', methods=['GET'])
# def get_branches(superadmin_id):
#     branches = Branch.query.filter_by(super_admin_id=superadmin_id).all()
#     return jsonify([{'id': branch.id, 'name': branch.name} for branch in branches]), 200

# @app.route('/superadmins/<int:superadmin_id>/branches', methods=['POST'])
# def create_branch(superadmin_id):
#     data = request.json
#     new_branch = Branch(name=data['name'], super_admin_id=superadmin_id)
#     db.session.add(new_branch)
#     db.session.commit()
#     return jsonify({'id': new_branch.id, 'name': new_branch.name}), 201

# @app.route('/branches/<int:branch_id>', methods=['PUT'])
# def update_branch(branch_id):
#     branch = Branch.query.get_or_404(branch_id)
#     data = request.json
#     branch.name = data.get('name', branch.name)
#     db.session.commit()
#     return jsonify({'id': branch.id, 'name': branch.name}), 200

# @app.route('/branches/<int:branch_id>', methods=['DELETE'])
# def delete_branch(branch_id):
#     branch = Branch.query.get_or_404(branch_id)
#     db.session.delete(branch)
#     db.session.commit()
#     return jsonify({'message': 'Branch deleted'}), 204


# # CRUD for Departments
# @app.route('/admins/<int:admin_id>/departments', methods=['GET'])
# def get_departments(admin_id):
#     departments = Department.query.filter_by(admin_id=admin_id).all()
#     return jsonify([{'id': department.id, 'name': department.name} for department in departments]), 200

# @app.route('/admins/<int:admin_id>/departments', methods=['POST'])
# def create_department(admin_id):
#     data = request.json
#     new_department = Department(name=data['name'], admin_id=admin_id)
#     db.session.add(new_department)
#     db.session.commit()
#     return jsonify({'id': new_department.id, 'name': new_department.name}), 201

# @app.route('/departments/<int:department_id>', methods=['PUT'])
# def update_department(department_id):
#     department = Department.query.get_or_404(department_id)
#     data = request.json
#     department.name = data.get('name', department.name)
#     db.session.commit()
#     return jsonify({'id': department.id, 'name': department.name}), 200

# @app.route('/departments/<int:department_id>', methods=['DELETE'])
# def delete_department(department_id):
#     department = Department.query.get_or_404(department_id)
#     db.session.delete(department)
#     db.session.commit()
#     return jsonify({'message': 'Department deleted'}), 204


# # CRUD for Members
# @app.route('/coordinators/<int:coordinator_id>/members', methods=['GET'])
# def get_members(coordinator_id):
#     members = Member.query.filter_by(coordinator_id=coordinator_id).all()
#     return jsonify([{'id': member.id, 'name': member.name} for member in members]), 200

# @app.route('/coordinators/<int:coordinator_id>/members', methods=['POST'])
# def create_member(coordinator_id):
#     data = request.json
#     new_member = Member(name=data['name'], coordinator_id=coordinator_id)
#     db.session.add(new_member)
#     db.session.commit()
#     return jsonify({'id': new_member.id, 'name': new_member.name}), 201

# @app.route('/members/<int:member_id>', methods=['PUT'])
# def update_member(member_id):
#     member = Member.query.get_or_404(member_id)
#     data = request.json
#     member.name = data.get('name', member.name)
#     db.session.commit()
#     return jsonify({'id': member.id, 'name': member.name}), 200

# @app.route('/members/<int:member_id>', methods=['DELETE'])
# def delete_member(member_id):
#     member = Member.query.get_or_404(member_id)
#     db.session.delete(member)
#     db.session.commit()
#     return jsonify({'message': 'Member deleted'}), 204


# # Main entry point for running the app
# if __name__ == '__main__':
#     db.create_all() 
#     app.run(debug=True)
