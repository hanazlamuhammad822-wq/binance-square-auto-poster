#!/usr/bin/env python3
"""
Binance Square Auto Poster - Web GUI
Opens in your browser automatically
"""

import os
import sys
import json
import time
import re
import io
import mimetypes
import cgi
import tempfile
import requests
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# ============ API CONFIG ============
BASE_URL_V2 = "https://www.binance.com/bapi/composite/v2/public/pgc/openApi"
BASE_URL_V1 = "https://www.binance.com/bapi/composite/v1/public/pgc/openApi"
ENDPOINTS = {
    "PRESIGNED_IMAGE_URL": f"{BASE_URL_V2}/image/presignedUrl",
    "IMAGE_STATUS": f"{BASE_URL_V2}/image/imageStatus",
    "ADD_CONTENT": f"{BASE_URL_V1}/content/add"
}
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "binance-square")
KEY_FILE = os.path.join(CONFIG_DIR, "openapi-key")

# ============ API FUNCTIONS ============
def save_api_key(key):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(KEY_FILE, "w") as f:
        f.write(key)
    os.chmod(KEY_FILE, 0o600)

def load_api_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    return ""

def get_headers(api_key):
    return {
        "X-Square-OpenAPI-Key": api_key,
        "Content-Type": "application/json",
        "clienttype": "binanceSkill"
    }

def upload_image(api_key, image_path):
    file_name = os.path.basename(image_path)
    mime_type = mimetypes.guess_type(image_path)[0] or 'application/octet-stream'

    res = requests.post(ENDPOINTS["PRESIGNED_IMAGE_URL"], headers=get_headers(api_key),
                        json={"imageName": file_name})
    data = res.json()
    if data.get("code") != "000000":
        return None, data.get("message", "Presigned URL error")

    presigned_url = data["data"]["presignedUrl"]
    file_ticket = data["data"]["fileTicket"]

    with open(image_path, "rb") as f:
        upload_res = requests.put(presigned_url, headers={"Content-Type": mime_type}, data=f)

    if upload_res.status_code != 200:
        return None, f"S3 upload failed: {upload_res.status_code}"

    for _ in range(15):
        status_res = requests.post(ENDPOINTS["IMAGE_STATUS"], headers=get_headers(api_key),
                                   json={"fileTicket": file_ticket})
        sd = status_res.json().get("data", {})
        if sd.get("status") == 1:
            return sd.get("imageUrl"), None
        elif sd.get("status") == 2:
            return None, sd.get("failedReason")
        time.sleep(2)

    return None, "Processing timeout"

def post_to_binance(api_key, text, image_urls=None):
    # Only limit hashtags to 5 (remove by exact position, not by string.replace,
    # to avoid accidentally stripping matching substrings out of other words)
    matches = list(re.finditer(r'#\w+', text))
    if len(matches) > 5:
        for m in reversed(matches[5:]):
            text = text[:m.start()] + text[m.end():]
        text = re.sub(r'\s+', ' ', text).strip()

    payload = {"contentType": 1, "bodyTextOnly": text}
    if image_urls:
        payload["imageList"] = image_urls

    res = requests.post(ENDPOINTS["ADD_CONTENT"], headers=get_headers(api_key), json=payload)
    if res.status_code == 504:
        return {"id": "unavailable", "shareLink": "unavailable"}, None

    data = res.json()
    if data.get("code") == "000000":
        return data.get("data"), None
    return None, data.get("message", "Unknown error")

# ============ HTML PAGE ============
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Binance Square Auto Poster</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 {
            color: #f7931a;
            font-size: 28px;
            letter-spacing: 3px;
            text-shadow: 0 0 20px rgba(247,147,26,0.5);
        }
        .header p { color: #aaa; font-size: 14px; margin-top: 5px; }
        .form-group { margin-bottom: 20px; }
        .form-group label {
            display: block;
            color: #f7931a;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 14px;
        }
        .form-group input[type="text"],
        .form-group textarea {
            width: 100%;
            padding: 12px 15px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 10px;
            color: white;
            font-size: 14px;
            transition: all 0.3s;
        }
        .form-group input:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #f7931a;
            box-shadow: 0 0 15px rgba(247,147,26,0.3);
        }
        .form-group textarea { height: 150px; resize: vertical; }
        .file-upload {
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .file-upload input[type="file"] {
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }
        .file-upload .btn-browse {
            background: #302b63;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.2);
            cursor: pointer;
            white-space: nowrap;
        }
        .file-upload .file-name { color: #aaa; font-size: 13px; }
        .image-preview {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }
        .image-preview img {
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 8px;
            border: 2px solid rgba(247,147,26,0.5);
        }
        .post-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #f7931a, #e67e22);
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            letter-spacing: 2px;
            transition: all 0.3s;
            margin-top: 10px;
        }
        .post-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(247,147,26,0.4);
        }
        .post-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        .status {
            text-align: center;
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            display: none;
        }
        .status.success {
            display: block;
            background: rgba(83,215,105,0.15);
            border: 1px solid #53d769;
            color: #53d769;
        }
        .status.error {
            display: block;
            background: rgba(233,69,96,0.15);
            border: 1px solid #e94560;
            color: #e94560;
        }
        .status.info {
            display: block;
            background: rgba(247,147,26,0.15);
            border: 1px solid #f7931a;
            color: #f7931a;
        }
        .progress-bar {
            width: 100%;
            height: 6px;
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
            margin-top: 10px;
            overflow: hidden;
            display: none;
        }
        .progress-bar .fill {
            height: 100%;
            background: linear-gradient(90deg, #f7931a, #53d769);
            border-radius: 3px;
            width: 0%;
            transition: width 0.3s;
        }
        .api-note {
            text-align: center;
            color: #666;
            font-size: 11px;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>BINANCE SQUARE</h1>
            <p>Auto Poster</p>
        </div>

        <form id="postForm">
            <div class="form-group">
                <label>API Key</label>
                <input type="text" id="apiKey" placeholder="Enter your Binance Square API Key" />
            </div>

            <div class="form-group">
                <label>Post Text</label>
                <textarea id="postText" placeholder="Write your post here..."></textarea>
            </div>

            <div class="form-group">
                <label>Images (Optional, max 4)</label>
                <div class="file-upload">
                    <span class="btn-browse">Choose Images</span>
                    <input type="file" id="imageInput" accept="image/*" multiple />
                    <span class="file-name" id="fileName">No files selected</span>
                </div>
                <div class="image-preview" id="imagePreview"></div>
            </div>

            <button type="submit" class="post-btn" id="postBtn">POST TO BINANCE SQUARE</button>
        </form>

        <div class="progress-bar" id="progressBar">
            <div class="fill" id="progressFill"></div>
        </div>

        <div class="status" id="statusBox"></div>

        <p class="api-note">Max 5 hashtags allowed. API Key is saved automatically.</p>
    </div>

    <script>
        const imageInput = document.getElementById('imageInput');
        const imagePreview = document.getElementById('imagePreview');
        const fileName = document.getElementById('fileName');
        const form = document.getElementById('postForm');
        const statusBox = document.getElementById('statusBox');
        const postBtn = document.getElementById('postBtn');
        const progressBar = document.getElementById('progressBar');
        const progressFill = document.getElementById('progressFill');

        let selectedFiles = [];

        fetch('/get-key').then(r => r.json()).then(data => {
            if (data.key) {
                document.getElementById('apiKey').value = data.key;
            }
        }).catch(() => {});

        imageInput.addEventListener('change', (e) => {
            selectedFiles = Array.from(e.target.files).slice(0, 4);
            fileName.textContent = selectedFiles.length > 0
                ? selectedFiles.length + ' file(s) selected'
                : 'No files selected';
            imagePreview.innerHTML = '';
            selectedFiles.forEach(file => {
                const reader = new FileReader();
                reader.onload = (ev) => {
                    const img = document.createElement('img');
                    img.src = ev.target.result;
                    imagePreview.appendChild(img);
                };
                reader.readAsDataURL(file);
            });
        });

        function showStatus(msg, type) {
            statusBox.className = 'status ' + type;
            statusBox.textContent = msg;
        }

        function setProgress(pct) {
            progressFill.style.width = pct + '%';
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const apiKey = document.getElementById('apiKey').value.trim();
            let text = document.getElementById('postText').value;

            if (!apiKey) { showStatus('Please enter API Key!', 'error'); return; }
            if (!text) { showStatus('Please enter post text!', 'error'); return; }

            postBtn.disabled = true;
            postBtn.textContent = 'POSTING...';
            progressBar.style.display = 'block';
            setProgress(10);
            showStatus('Uploading images...', 'info');

            let imageUrls = [];

            if (selectedFiles.length > 0) {
                for (let i = 0; i < selectedFiles.length; i++) {
                    setProgress(10 + (i / selectedFiles.length) * 40);
                    showStatus('Uploading image ' + (i+1) + '/' + selectedFiles.length + '...', 'info');

                    const formData = new FormData();
                    formData.append('apiKey', apiKey);
                    formData.append('image', selectedFiles[i]);

                    try {
                        const res = await fetch('/upload', { method: 'POST', body: formData });
                        const data = await res.json();
                        if (data.url) {
                            imageUrls.push(data.url);
                        } else {
                            showStatus('Upload failed: ' + (data.error || 'Unknown'), 'error');
                            postBtn.disabled = false;
                            postBtn.textContent = 'POST TO BINANCE SQUARE';
                            progressBar.style.display = 'none';
                            return;
                        }
                    } catch (err) {
                        showStatus('Upload error: ' + err.message, 'error');
                        postBtn.disabled = false;
                        postBtn.textContent = 'POST TO BINANCE SQUARE';
                        progressBar.style.display = 'none';
                        return;
                    }
                }
            }

            setProgress(60);
            showStatus('Publishing...', 'info');

            try {
                const res = await fetch('/post', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ apiKey: apiKey, text: text, images: imageUrls })
                });
                const data = await res.json();
                setProgress(100);

                if (data.success) {
                    showStatus('POST SUCCESSFUL! ID: ' + (data.id || 'N/A') + ' | Link: ' + (data.link || 'N/A'), 'success');
                } else {
                    showStatus('POST FAILED: ' + (data.error || 'Unknown error'), 'error');
                }
            } catch (err) {
                showStatus('Error: ' + err.message, 'error');
            }

            postBtn.disabled = false;
            postBtn.textContent = 'POST TO BINANCE SQUARE';
            setTimeout(() => { progressBar.style.display = 'none'; setProgress(0); }, 2000);
        });
    </script>
</body>
</html>"""

# ============ HTTP SERVER ============
class PostHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get-key':
            key = load_api_key()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"key": key}).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        if self.path == '/upload':
            self.handle_upload(content_length)
        elif self.path == '/post':
            self.handle_post(content_length)
        else:
            self.send_response(404)
            self.end_headers()

    def handle_upload(self, content_length):
        try:
            content_type = self.headers['Content-Type']
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': content_type,
                }
            )

            api_key = form_data.getvalue('apiKey')
            file_item = form_data['image']

            if not file_item.filename:
                self.send_json({"error": "No file selected"})
                return

            tmp_dir = tempfile.mkdtemp()
            tmp_path = os.path.join(tmp_dir, file_item.filename)
            with open(tmp_path, 'wb') as f:
                f.write(file_item.file.read())

            url, err = upload_image(api_key, tmp_path)

            try:
                os.remove(tmp_path)
                os.rmdir(tmp_dir)
            except:
                pass

            if url:
                self.send_json({"url": url})
            else:
                self.send_json({"error": err})

        except Exception as e:
            self.send_json({"error": str(e)})

    def handle_post(self, content_length):
        try:
            body = self.rfile.read(content_length)
            data = json.loads(body)

            api_key = data.get('apiKey')
            text = data.get('text')
            images = data.get('images', [])

            if not api_key or not text:
                self.send_json({"success": False, "error": "Missing API key or text"})
                return

            save_api_key(api_key)

            result, err = post_to_binance(api_key, text, images if images else None)

            if err:
                self.send_json({"success": False, "error": err})
            else:
                self.send_json({
                    "success": True,
                    "id": result.get("id"),
                    "link": result.get("shareLink")
                })

        except Exception as e:
            self.send_json({"success": False, "error": str(e)})

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass

# ============ MAIN ============
def main():
    port = 8888
    server = HTTPServer(('127.0.0.1', port), PostHandler)

    print()
    print("  ========================================")
    print("     BINANCE SQUARE AUTO POSTER")
    print("     Web GUI Version")
    print("  ========================================")
    print()
    print("  Server: http://127.0.0.1:" + str(port))
    print("  Opening in browser...")
    print()

    threading.Timer(1.0, lambda: webbrowser.open('http://127.0.0.1:' + str(port))).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("  Server stopped.")
        server.server_close()

if __name__ == "__main__":
    main()
