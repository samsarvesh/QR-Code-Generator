from flask import Flask, render_template, request, send_file
import qrcode
import os
from datetime import datetime

app = Flask(__name__)
QR_FOLDER = os.path.join("static", "qr_codes")

if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_filename = None
    if request.method == "POST":
        data = request.form.get("data")
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=12,
                border=4
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#0f172a", back_color="white")

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            qr_filename = f"qr_{timestamp}.png"
            img.save(os.path.join(QR_FOLDER, qr_filename))

    return render_template("index.html", qr_filename=qr_filename)

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(QR_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
