from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from netaddr import IPAddress, IPRange, IPNetwork
import os
import re

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.jinja_env.cache = {}
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_ip_list(content):
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    result = []
    for line in lines:
        parts = re.split(r'[\s,]+', line)
        for part in parts:
            part = part.strip()
            try:
                if '-' in part:
                    start_ip, end_ip = part.split('-')
                    iprange = IPRange(start_ip.strip(), end_ip.strip())
                    result.extend(str(ip) for ip in iprange)
                elif '/' in part:
                    ipnet = IPNetwork(part)
                    result.extend(str(ip) for ip in ipnet)
                else:
                    ip = IPAddress(part)
                    result.append(str(ip))
            except Exception as e:
                raise ValueError(f"Invalid input detected: {part}. Error: {str(e)}")
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    parsed_ips = []
    error = None
    count = 0
    if request.method == 'POST':
        text_input = request.form.get('ip_textarea')
        file = request.files.get('ip_file')
        try:
            if text_input:
                parsed_ips = parse_ip_list(text_input)
            elif file and allowed_file(file.filename):
                content = file.read().decode('utf-8')
                parsed_ips = parse_ip_list(content)
            else:
                raise ValueError("Tidak ada input valid ditemukan.")

            if not parsed_ips:
                raise ValueError("Tidak ada IP Address valid yang berhasil diparse.")

            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.txt')
            with open(output_path, 'w') as f:
                f.write('\n'.join(parsed_ips))
            count = len(parsed_ips)
        except Exception as e:
            error = str(e)

    return render_template('index.html', parsed_ips=parsed_ips, error=error, count=count)

@app.route('/download')
def download():
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.txt')
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=8087)

