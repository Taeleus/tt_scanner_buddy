from flask import Flask, render_template, request
from resource_identifier import ResourceIdentifier

app = Flask(__name__)
res_identifier = ResourceIdentifier()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    is_string_result = False  # flag to indicate if result is a plain string
    if request.method == "POST":
        rs_signature_str = request.form.get("rs_signature")
        mining_location = request.form.get("mining_location")
        try:
            rs_signature = int(rs_signature_str)
        except ValueError:
            error = "RS signature must be a non-negative integer."
            return render_template("home.html", result=result, error=error, is_string_result=is_string_result)
        result = res_identifier.identify_resource(rs_signature, mining_location)
        is_string_result = isinstance(result, str)
    return render_template("home.html", result=result, error=error, is_string_result=is_string_result)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
