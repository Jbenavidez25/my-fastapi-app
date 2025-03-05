from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/execute", methods=["POST"])
def execute():
    # Simulating a response that might have been in bytes
    byte_data = b"Hello World"  # Example bytes response

    # ✅ FIX: Decode bytes before sending the response
    fixed_data = byte_data.decode("utf-8")  # Convert bytes to string

    # ✅ Ensure the response is always a string
    return jsonify({"message": fixed_data})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
