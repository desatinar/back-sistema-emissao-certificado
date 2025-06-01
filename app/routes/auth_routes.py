from flask import Blueprint, request, jsonify, session
from app.models.user import User
from app import db

auth_bp = Blueprint("auth_api", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Usuário e senha são obrigatórios"}), 400
    
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session.clear()
        session["admin_id"] = user.id
        session["email"] = user.email

        return jsonify({"message": "Sucesso!", "user": user.to_dict()}), 200
    
    else:
        return jsonify({"message": "Credenciais inválidas"}), 401
    
@auth_bp.route("/logout", methods=["POST"])
def logout():
    admin_id_logged_out = session.pop("admin_id", None)
    session.pop("email", None)
    
    if admin_id_logged_out:
        return jsonify({"message": "Logout"}), 200
    else:
        return jsonify({"message": "Nenhum usuário logado para deslogar"}), 400
    
@auth_bp.route("/status", methods=["GET"])
def status():
    if "admin_id" in session:
        return jsonify({
            "logged_in": True,
            "admin_id": session["admin_id"],
            "email": session.get("email")
        }), 200
    else:
        return jsonify({"logged_in": False}), 200