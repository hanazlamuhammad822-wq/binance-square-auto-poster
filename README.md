# binance-square-auto-poster
# 🚀 Binance Square Auto Poster

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**Automatically post content to Binance Square with text and images**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [API Key](#-api-key-setup) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [API Key Setup](#-api-key-setup)
- [Usage](#-usage)
  - [Web GUI Version](#-web-gui-version)
  - [CLI Version](#-cli-version)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Rules & Limits](#-rules--limits)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

<table>
<tr>
<td>

### 📝 Text Posts
- Post text content to Binance Square
- Support for hashtags and cashtags
- Auto-limit hashtags to 5

</td>
<td>

### 📷 Image Posts
- Upload up to 4 images per post
- Automatic image processing
- Support for PNG, JPG, GIF, WebP

</td>
</tr>
<tr>
<td>

### 🔑 Auto-Save API Key
- Enter API key once
- Saved securely in config
- Auto-load on next use

</td>
<td>

### 🎨 Web GUI
- Beautiful dark theme
- Opens in browser automatically
- Image preview before upload

</td>
</tr>
<tr>
<td>

### 💻 CLI Interface
- Colorful terminal output
- Animated progress bars
- File explorer for images

</td>
<td>

### 🔄 Smart Processing
- Auto-remove emojis
- Auto-limit hashtags
- Error handling & recovery

</td>
</tr>
</table>

---

## 📦 Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.7+ | Required |
| requests | 2.28+ | HTTP library |
| Internet | - | Required for API calls |
| Binance Account | - | Required for API key |

---

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/hanazlamuhammad822-wq/binance-square-auto-poster.git
cd binance-square-poster
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Make Scripts Executable
```bash
chmod +x bsquare_web.py bsquare_cli.py
```

### 4. Verify Installation
```bash
python3 bsquare_cli.py
```

---

## 🔑 API Key Setup

### Step 1: Go to Binance Square Creator Center
Visit: https://www.binance.com/square/creator-center/home

### Step 2: Login to Binance
Use your Binance account credentials

### Step 3: Navigate to API Management
Look for "API" or "OpenAPI" section

### Step 4: Create New API Key
- Click "Create API Key"
- Name it (e.g., "Square Auto Poster")
- Set permissions (Posting access)
- Copy the generated key

### Step 5: Enter in Script
The script will prompt you to enter the API key on first run. It's saved automatically.

---

## 🚀 Usage

### 🌐 Web GUI Version

**Start the server:**
```bash
python3 bsquare_web.py
```

**What happens:**
1. Server starts on port 8888
2. Browser opens automatically
3. Enter your API key (saved for future)
4. Write your post content
5. Select images (optional)
6. Click "POST TO BINANCE SQUARE"

**Access URL:**
```
http://127.0.0.1:8888
```

---

### 💻 CLI Version

**Start the CLI:**
```bash
python3 bsquare_cli.py
```

**Available Options:**
```
1  Change / Set API Key
2  Post Text Only
3  Post Text with Images
4  Exit
```

---

## 📸 Screenshots

### Web GUI Interface
```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│                   BINANCE SQUARE                           │
│                   Auto Poster                              │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  API Key                                                   │
│  ┌──────────────────────────────────────────────────────┐ │
│  │             │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  Post Content                                              │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Hello crypto world!                                  │ │
│  │                                                      │ │
│  │ #Bitcoin #Ethereum #Crypto                           │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  Images (Optional, max 4)                                  │
│  ┌────────────────────────┐  ┌─────────────────────────┐ │
│  │     Choose Images      │  │   2 file(s) selected    │ │
│  └────────────────────────┘  └─────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │            POST TO BINANCE SQUARE                    │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### CLI Main Menu
```
  ╔════════════════════════════════════════════════════════════╗
  ║                                                            ║
  ║   ██╗░░░░░░█████╗░░█████╗░██╗░░░░░░██████╗░░█████╗░░██████╗  ║
  ║   ██║░░░░░██╔══██╗██╔══██╗██║░░░░░██╔════╝░██╔══██╗██╔════╝  ║
  ║   ██║░░░░░██║░░██║██║░░██║██║░░░░░██║░░██╗░██║░░██║╚█████╗░  ║
  ║   ██║░░░░░██║░░██║██║░░██║██║░░░░░██║░░╚██╗██║░░██║░╚═══██╗  ║
  ║   ███████╗╚█████╔╝╚█████╔╝███████╗╚██████╔╝╚█████╔╝██████╔╝  ║
  ║   ╚══════╝░╚════╝░░╚════╝░╚══════╝░╚═════╝░░╚════╝░╚═════╝░  ║
  ║                                                            ║
  ║         S  Q  U  A  R  E   P  O  S  T                      ║
  ║                                                            ║
  ║              Auto Poster for Binance Square                 ║
  ║                                                            ║
  ╚════════════════════════════════════════════════════════════╝

  ┌────────────────────────────────────────────────┐
  │  1  Change / Set API Key                        │
  │  2  Post Text Only                              │
  │  3  Post Text with Images                       │
  │  4  Exit                                        │
  └────────────────────────────────────────────────┘
    For photo posts, use GUI: python3 bsquare_web.py

  Select [1-4]: 
```

### CLI - Text Post Success
```
  ─── TEXT POST ───
  Enter post text: Hello crypto enthusiasts! #Bitcoin #Ethereum

  Note: Limited to 5 hashtags (Binance rule)

  Publishing: ██████████████████████████████ 100%

  ┌──────────────────────────────────────────────┐
  │              ✅  POST SUCCESSFUL  ✅           │
  └──────────────────────────────────────────────┘
  Post ID   :
  Post Link : https://www.binance.com/square/post/123456789
  ───────────────────────────────────────────────

  Press Enter...
```

### CLI - Image Post Success
```
  ─── POST WITH IMAGES 📷 ───
  Enter post text: Check this chart #Bitcoin

  Opening file explorer...

  Selected 2 image(s):
    [1] chart_analysis.png
    [2] market_data.jpg

  Post this? (y/n): y

  [1/2] Uploading: chart_analysis.png
  Uploading: ██████████████████████████████ 100%

  [2/2] Uploading: market_data.jpg
  Uploading: ██████████████████████████████ 100%

  Publishing: ██████████████████████████████ 100%

  ┌──────────────────────────────────────────────┐
  │              ✅  POST SUCCESSFUL  ✅           │
  └──────────────────────────────────────────────┘
  Post ID   : 123456790
  Post Link : https://www.binance.com/square/post/123456790
  ───────────────────────────────────────────────

  Press Enter...
```

---

## 📁 Project Structure

```
binance-square-poster/
│
├── bsquare_web.py          # 🌐 Web GUI version
│                            #    Opens in browser
│                            #    Beautiful dark theme
│                            #    Image preview
│
├── bsquare_cli.py          # 💻 CLI version
│                            #    Terminal interface
│                            #    Colorful output
│                            #    File explorer
│
├── requirements.txt        # 📦 Python dependencies
│
├── README.md               # 📚 This documentation
│
└── .config/                # 🔧 Auto-created config
    └── binance-square/
        └── openapi-key     # 🔑 Saved API key
```

---

## ⚠️ Rules & Limits

| Item | Limit | Action |
|------|-------|--------|
| **Hashtags** | Max 5 per post | Auto-limited |
| **Images** | Max 4 per post | Warned |
| **Emojis** | Not supported | Auto-removed |
| **API Key** | Required | Auto-saved |
| **Post Length** | Binance limit | Server-side check |

---

## 🐛 Troubleshooting

### ❌ "API Key not found"
```bash
# Solution: Set your API key
python3 bsquare_cli.py
# Select option 1 and enter your API key
```

### ❌ "Hashtag count exceeds limit"
```
# You have more than 5 hashtags
# Script auto-limits to 5
# Keep only important hashtags
```

### ❌ "POST UNSUCCESSFUL"
```
# Check:
# ✓ API key is valid
# ✓ Internet connection works
# ✓ Have posting permissions
# ✓ Content follows Binance rules
```

### ❌ Web GUI not opening
```bash
# Check if port is in use
lsof -i :8888

# Try manual access
# Open browser: http://127.0.0.1:8888
```

### ❌ "ModuleNotFoundError: requests"
```bash
# Install dependencies
pip install -r requirements.txt
```

---

## ❓ FAQ

### Q: Is this tool safe to use?
**A:** Yes! This tool uses official Binance Square API endpoints. Your API key is stored locally with secure permissions (600).

### Q: Can I schedule posts?
**A:** Not yet, but this feature is planned for future updates.

### Q: Do I need a Binance account?
**A:** Yes, you need a Binance account to generate an API key from the Creator Center.

### Q: Can I edit/delete posts with this tool?
**A:** No, this tool only creates new posts. Use Binance Square app for editing.

### Q: What image formats are supported?
**A:** PNG, JPG, JPEG, GIF, and WebP formats are supported.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

### 1. Fork Repository
```bash
# Click "Fork" on GitHub
```

### 2. Clone Your Fork
```bash
git clone https://github.com/yourusername/binance-square-poster.git
cd binance-square-poster
```

### 3. Create Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes
```bash
# Edit files
# Test thoroughly
```

### 5. Commit Changes
```bash
git add .
git commit -m "Add: your feature description"
```

### 6. Push to GitHub
```bash
git push origin feature/your-feature-name
```

### 7. Create Pull Request
- Go to your fork on GitHub
- Click "New Pull Request"
- Add description
- Submit PR

---

## 📊 Comparison: Web GUI vs CLI

| Feature | Web GUI | CLI |
|---------|:-------:|:---:|
| Text Posts | ✅ | ✅ |
| Image Posts | ✅ | ✅ |
| API Key Save | ✅ | ✅ |
| Easy to Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Speed | Fast | Fast |
| No Browser Needed | ❌ | ✅ |
| Best for Photos | ✅ | ⚠️ |
| Works Offline | ❌ | ✅ |

---

## 📜 License

```
MIT License

Copyright (c) 2024 Binance Square Auto Poster

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- Binance for the Square API
- Python Community for amazing libraries
- All contributors and users

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/binance-square-poster/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/binance-square-poster/discussions)

---

## ⭐ Star This Repo

If this project helped you, please give it a ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ for the Crypto Community**

[Back to Top](#-binance-square-auto-poster)

</div>
