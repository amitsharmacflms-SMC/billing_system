@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return {"error": "Invalid Email or Password"}, 401

    from flask_jwt_extended import create_access_token

    token = create_access_token(
        identity=user.id,
        additional_claims={
            "role": user.role,
            "state": user.state,
            "supplier_id": user.supplier_id
        }
    )

    # THIS MUST RETURN EXACT FIELDS ↓↓↓
    return {
        "access_token": token,
        "role": user.role,
        "state": user.state,
        "supplier_id": user.supplier_id
    }, 200
