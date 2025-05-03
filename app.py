from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send_data", methods=["POST"])
def get_data():
    try:
        data = request.get_json()
        if not data or "username" not in data or "password" not in data:
            return jsonify({"status": "error", "message": "Invalid input"}), 400

        hashed_password = generate_password_hash(data["password"])
        new_user = User(username=data["username"], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success"})

    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 500
    

    
@app.route("/get_data", methods=["GET"])
def fetch_data():
    try:
        users = User.query.all()
        user_list = [{"id": user.id, "username": user.username} for user in users]
        return jsonify({"status": "success", "data": user_list})
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)