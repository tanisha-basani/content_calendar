from flask import Flask, request, jsonify
from notion import get_database_entries, add_item

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Notion Content Tracker API 🚀"})

# Get all items from Notion database
@app.route("/items", methods=["GET"])
def get_items():
    data = get_database_entries()
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Could not fetch items"}), 500

# Add a new item to Notion
@app.route("/items", methods=["POST"])
def create_item():
    content = request.json
    title = content.get("title")
    status = content.get("status", "Idea")
    tags = content.get("tags", [])

    if not title:
        return jsonify({"error": "Title is required"}), 400

    result = add_item(title, status, tags)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to create item"}), 500

if __name__ == "__main__":
    app.run(debug=True)
