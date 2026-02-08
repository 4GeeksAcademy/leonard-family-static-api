"""Docstring: explains this module starts the API and defines endpoints."""  # Describes the file purpose.
import os  # Accesses environment variables.
from flask import Flask, request, jsonify  # Imports Flask and HTTP utilities.
from flask_cors import CORS  # Imports CORS support.
from datastructures import FamilyStructure  # Imports the family structure.
from utils import APIException, generate_sitemap  # Imports exception and sitemap.

app = Flask(__name__)  # Creates the Flask app.
app.url_map.strict_slashes = False  # Allows routes with or without trailing slash.
CORS(app)  # Enables CORS for the app.

# Initialize the Jackson family with the 3 initial members
jackson_family = FamilyStructure("Jackson", [  # Creates the family with base members.
    {"id": 1, "first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]},  # Member 1.
    {"id": 2, "first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]},  # Member 2.
    {"id": 3, "first_name": "Jimmy", "age": 5, "lucky_numbers": [1]}  # Member 3.
])  # Closes the initial members list.

# Error handler for APIException
@app.errorhandler(APIException)  # Registers the error handler.
def handle_invalid_usage(error):  # Receives the captured error.
    return jsonify(error.to_dict()), error.status_code  # Returns JSON and status.

# Route to generate sitemap
@app.route('/')  # Defines the root route.
def sitemap():  # Endpoint function.
    return generate_sitemap(app)  # Generates and returns the sitemap.

# Route to get all family members
@app.route('/members', methods=['GET'])  # Defines GET /members.
def read_family():  # Endpoint function.
    return jsonify(jackson_family.get_all_members()), 200  # Returns list and 200.

# Route to add a new family member
@app.route("/member", methods=["POST"])  # Defines POST /member.
def create_member():  # Endpoint function.
    try:  # Starts error handling block.
        member = request.json  # Reads the JSON body.

        # Validate required fields
        if not all(key in member for key in ["id", "first_name", "age", "lucky_numbers"]):  # Validates fields.
            return jsonify({"error": "Missing required fields"}), 400  # Returns 400 if missing.

        # Validate data types
        if not isinstance(member["id"], int):  # Validates integer id.
            return jsonify({"error": "id must be an integer"}), 400  # Returns 400.
        if not isinstance(member["first_name"], str):  # Validates string name.
            return jsonify({"error": "first_name must be a string"}), 400  # Returns 400.
        if not isinstance(member["age"], int):  # Validates integer age.
            return jsonify({"error": "age must be an integer"}), 400  # Returns 400.
        if not isinstance(member["lucky_numbers"], list):  # Validates numbers list.
            return jsonify({"error": "lucky_numbers must be a list"}), 400  # Returns 400.

        # Check if member with the same ID already exists
        if jackson_family.get_member(member["id"]):  # Checks if it already exists.
            return jsonify({"error": "Member with the same ID already exists"}), 400  # Returns 400.

        # Add the member to the family
        jackson_family.add_member(member)  # Adds the member.

        # Return success response
        return jsonify(member), 200  # Returns the member and 200.

    except Exception as e:  # Catches unexpected errors.
        # Handle unexpected server errors
        return jsonify({"error": str(e)}), 500  # Returns 500.

# Route to get a specific family member by ID
@app.route("/member/<int:id>", methods=["GET"])  # Defines GET /member/<id>.
def get_member(id: int):  # Endpoint function.
    person = jackson_family.get_member(id)  # Looks up the member.
    if person:  # Checks if it exists.
        return jsonify(person), 200  # Returns member and 200.
    return jsonify({"error": "Member not found"}), 404  # Returns 404.

# Route to delete a family member by ID
@app.route("/member/<int:id>", methods=["DELETE"])  # Defines DELETE /member/<id>.
def delete_member(id: int):  # Endpoint function.
    if jackson_family.get_member(id):  # Checks if it exists.
        jackson_family.delete_member(id)  # Deletes the member.
        return jsonify({"done": True}), 200  # Returns confirmation.
    return jsonify({"error": "Member not found"}), 404  # Returns 404.

# Run the app
if __name__ == '__main__':  # Only runs when executed directly.
    PORT = int(os.environ.get('PORT', 3000))  # Reads port or uses 3000.
    app.run(host='0.0.0.0', port=PORT, debug=True)  # Starts the server.