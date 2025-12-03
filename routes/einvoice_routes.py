from flask import Blueprint, request, jsonify

einv_bp = Blueprint("einvoice", __name__, url_prefix="/einvoice")

# -----------------------------------------------------
# TEST ROUTE – Check API is working
# -----------------------------------------------------
@einv_bp.route("/test", methods=["GET"])
def test_einvoice():
    return jsonify({"status": "E-Invoice API Working"})


# -----------------------------------------------------
# GENERATE E-INVOICE (dummy for now)
# -----------------------------------------------------
@einv_bp.route("/generate", methods=["POST"])
def generate_einvoice():
    data = request.get_json()

    # Here you will later add NIC API integration
    return jsonify({
        "message": "E-Invoice generation endpoint working",
        "input": data
    })


# -----------------------------------------------------
# CANCEL E-INVOICE (dummy)
# -----------------------------------------------------
@einv_bp.route("/cancel", methods=["POST"])
def cancel_einvoice():
    data = request.get_json()

    return jsonify({
        "message": "E-Invoice cancellation endpoint working",
        "input": data
    })
