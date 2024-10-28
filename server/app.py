from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_cors import CORS
import uuid  # Add this import to generate UUIDs

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='santhosh090405@',
        database='admindb'
    )

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    user_id = str(uuid.uuid4())  # Generate a UUID
    username = data['username']
    password = data['password']
    role = data['role']
    access_id = data['access_id']

    connection = create_connection()
    cursor = connection.cursor()
    hashed_password = generate_password_hash(password)  # Hash the password for security
    try:
        cursor.execute("INSERT INTO user (id, username, password, role, access_id) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, username, hashed_password, role, access_id))
        connection.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password'], password):
        # Return both role and access_id in the response
        return jsonify({
            'role': user['role'],
            'access_id': user['access_id']
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Organization Routes

@app.route('/organizations', methods=['POST'])
def create_organization():
    data = request.get_json()
    id = str(uuid.uuid4())
    name = data.get('name')
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO organization (id, name) VALUES (%s, %s)", (id,name,))
        connection.commit()
        return jsonify({"message": "Organization created", "organizationId": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/organizations', methods=['GET'])
def get_organizations():
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM organization")
        organizations = cursor.fetchall()
        return jsonify(organizations)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/organizations/<int:id>', methods=['GET'])
def get_organization(id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM organization WHERE id = %s", (id,))
        organization = cursor.fetchone()
        if organization:
            return jsonify(organization)
        else:
            return jsonify({"message": "Organization not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/organizations/<int:id>', methods=['PUT'])
def update_organization(id):
    data = request.get_json()
    name = data.get('name')
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE organization SET name = %s WHERE id = %s", (name, id))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "Organization updated"})
        else:
            return jsonify({"message": "Organization not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/organizations/<int:id>', methods=['DELETE'])
def delete_organization(id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM organization WHERE id = %s", (id,))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "Organization deleted"})
        else:
            return jsonify({"message": "Organization not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Get branches for a specific organization
@app.route('/organizations/<int:id>/branches', methods=['GET'])
def get_branches(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM branch WHERE organization_id = %s", (id,))
    branches = cursor.fetchall()
    connection.close()
    return jsonify(branches)

# Add a branch to an organization
@app.route('/organizations/<int:id>/branches', methods=['POST'])
def add_branch(id):
    data = request.json
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO branch (name, organization_id) VALUES (%s, %s)", (data['name'], id))
    connection.commit()
    branch_id = cursor.lastrowid
    connection.close()
    return jsonify({'id': branch_id, 'name': data['name']})

@app.route('/branches/<int:id>', methods=['GET'])
def get_branch(id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM branch WHERE id = %s", (id,))
        branch = cursor.fetchone()
        if branch:
            return jsonify(branch)
        else:
            return jsonify({"message": "Branch not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/branches/<int:id>', methods=['PUT'])
def update_branch(id):
    data = request.get_json()
    name = data.get('name')
    organization_id = data.get('organization_id')
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE branch SET name = %s, organization_id = %s WHERE id = %s", (name, organization_id, id))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "Branch updated"})
        else:
            return jsonify({"message": "Branch not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/branches/<int:id>', methods=['DELETE'])
def delete_branch(id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM branch WHERE id = %s", (id,))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "Branch deleted"})
        else:
            return jsonify({"message": "Branch not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Get departments for a specific branch
@app.route('/branches/<int:branch_id>/departments', methods=['GET'])
def get_departments(branch_id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM department WHERE branch_id = %s", (branch_id,))
        departments = cursor.fetchall()
        return jsonify(departments)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Add a department to a branch
@app.route('/branches/<int:branch_id>/departments', methods=['POST'])
def add_department(branch_id):
    data = request.json
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO department (name, branch_id) VALUES (%s, %s)", (data['name'], branch_id))
        connection.commit()
        department_id = cursor.lastrowid
        return jsonify({'id': department_id, 'name': data['name']})
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/departments/<int:id>', methods=['GET'])
def get_department(id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM department WHERE id = %s", (id,))
        department = cursor.fetchone()
        if department:
            return jsonify(department)
        else:
            return jsonify({"message": "Department not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/departments/<int:id>', methods=['PUT'])
def update_department(id):
    data = request.get_json()
    name = data.get('name')
    branch_id = data.get('branch_id')
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE department SET name = %s, branch_id = %s WHERE id = %s", (name, branch_id, id))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "Department updated"})
        else:
            return jsonify({"message": "Department not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/departments/<int:id>', methods=['DELETE'])
def delete_department(id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM department WHERE id = %s", (id,))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "Department deleted"})
        else:
            return jsonify({"message": "Department not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# User Routes

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    id = str(uuid.uuid4())
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    access_id = data.get('access_id')

    if not username or not password or not role or not access_id:
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = generate_password_hash(password)
    
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user (id,username, password, role, access_id) VALUES (%s, %s, %s, %s, %s)",
                       (id, username, hashed_password, role, access_id))
        connection.commit()
        return jsonify({"message": "User created", "userId": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/users', methods=['GET'])
def get_users():
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        return jsonify(users)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE id = %s", (id,))
        user = cursor.fetchone()
        if user:
            return jsonify(user)
        else:
            return jsonify({"message": "User not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    access_id = data.get('access_id')
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE user SET username = %s, password = %s, role = %s, access_id = %s WHERE id = %s",
                       (username, password, role, access_id, id))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "User updated"})
        else:
            return jsonify({"message": "User not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM user WHERE id = %s", (id,))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "User deleted"})
        else:
            return jsonify({"message": "User not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/departments/<string:department_id>/members', methods=['GET'])
def get_members_by_department(department_id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE role = %s AND access_id = %s", ('member', department_id))
        members = cursor.fetchall()
        return jsonify(members)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/branches/<string:branch_id>/members', methods=['GET'])
def get_members_by_branch(branch_id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE role = %s AND access_id = %s", ('branchadmin', branch_id))
        members = cursor.fetchall()
        return jsonify(members)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/organizations/<string:organization_id>/members', methods=['GET'])
def get_members_by_organization(organization_id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE role = %s AND access_id = %s", ('orgadmin', organization_id))
        members = cursor.fetchall()
        return jsonify(members)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/departments/<string:department_id>/admins', methods=['GET'])
def get_admins_by_department(department_id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE role = %s AND access_id = %s", ('dprtadmin', department_id))
        members = cursor.fetchall()
        return jsonify(members)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
