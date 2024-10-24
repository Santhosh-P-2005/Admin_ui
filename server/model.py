# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the Supersuperadmin model
class Supersuperadmin(db.Model):
    __tablename__ = 'supersuperadmin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    organizations = db.relationship('Organization', backref='supersuperadmin', lazy=True)


# Define the Organization model
class Organization(db.Model):
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_super_admin_id = db.Column(db.Integer, db.ForeignKey('supersuperadmin.id'))

    branches = db.relationship('Branch', backref='organization', lazy=True)


# Define the Branch model
class Branch(db.Model):
    __tablename__ = 'branch'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))

    admins = db.relationship('Admin', backref='branch', lazy=True)


# Define the Admin model
class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

    departments = db.relationship('Department', backref='admin', lazy=True)


# Define the Department model
class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    coordinators = db.relationship('Coordinator', backref='department', lazy=True)


# Define the Coordinator model
class Coordinator(db.Model):
    __tablename__ = 'coordinator'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    members = db.relationship('Member', backref='coordinator', lazy=True)


# Define the Member model
class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    coordinator_id = db.Column(db.Integer, db.ForeignKey('coordinator.id'))