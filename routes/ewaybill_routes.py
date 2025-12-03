from flask import Blueprint, request, jsonify

eway_bp = Blueprint("ewaybill", __name__, url_prefix="/ewaybill")


# -----------------------------------------------------
# TEST ROUTE – confirm API is working
# -----------------------------------------------------
@eway_bp.route("/test", methods=["GET"])
def test_ewaybill():
    return jsonify({"status": "E-Waybill API Working"})


# -----------------------------------------------------
# GENERATE E-WAYBILL (dummy for now)
# -----------------------------------------------------
@eway_bp.route("/generate", methods=["POST"])
def generate_ewaybill():
    data = request.get_json()

    # Later: integrate with NIC EWB API
    return jsonify({
        "message": "E-Waybill generation endpoint working",
        "input": data
    })


# -----------------------------------------------------
# CANCEL E-WAYBILL (dummy for now)
# -----------------------------------------------------
@eway_bp.route("/cancel", methods=["POST"])
def cancel_ewaybill():
    data = request.get_json()

    return jsonify({
        "message": "E-Waybill cancellation endpoint working",
        "input": data
    })
