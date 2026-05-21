from flask import Flask, render_template, request, jsonify, send_file
from services.srt_parser import parse_srt_blocks
from services.srt_processor import process_blocks
import io

app = Flask(__name__)

progress_state = {"value": 0}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/progress")
def progress():
    return jsonify(progress_state)

@app.route("/translate", methods=["POST"])
def translate():
    progress_state["value"] = 0

    file = request.files.get("srt")
    if not file:
        return "No file uploaded", 400

    lines = file.read().decode("utf-8-sig").splitlines()
    blocks = parse_srt_blocks(lines)

    def update_progress(val):
        progress_state["value"] = val

    result = process_blocks(blocks, update_progress)

    buf = io.BytesIO()
    buf.write(result.encode("utf-8"))
    buf.seek(0)

    return send_file(
        buf,
        as_attachment=True,
        download_name="translated.srt",
        mimetype="application/octet-stream"
    )

if __name__ == "__main__":
    app.run(debug=True)
