from flask import Flask, render_template, request
from resource_identifier import ResourceIdentifier

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace_with_a_secure_key'

res_identifier = ResourceIdentifier()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    is_string_result = False
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

if __name__ == "__main__":
    # Run the app on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
