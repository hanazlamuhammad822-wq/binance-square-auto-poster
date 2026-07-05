#!/usr/bin/env python3
"""
Binance Square Auto Poster - CLI Version
Supports multi-line text paste
"""

import os
import sys
import time
import re
import requests
import mimetypes
import tkinter as tk
from tkinter import filedialog

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

# ============ COLORS ============
G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
C = "\033[96m"
B = "\033[1m"
D = "\033[90m"
X = "\033[0m"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print()
    print(f"  {C}{B}╔══════════════════════════════════════════════════╗{X}")
    print(f"  {C}{B}║{X}                                                    {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {R}{B}██╗  ██╗ █████╗ ███╗   ██╗ █████╗ ███████╗{X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {R}{B}██║  ██║██╔══██╗████╗  ██║██╔══██╗╚══███╔╝{X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {R}{B}███████║███████║██╔██╗ ██║███████║  ███╔╝ {X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {R}{B}██╔══██║██╔══██║██║╚██╗██║██╔══██║ ███╔╝  {X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {R}{B}██║  ██║██║  ██║██║ ╚████║██║  ██║███████╗{X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {R}{B}╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝{X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {Y}{B}██╗      █████╗                             {X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {Y}{B}██║     ██╔══██╗                            {X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {Y}{B}██║     ███████║                            {X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {Y}{B}██║     ██╔══██║                            {X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {Y}{B}███████╗██║  ██║                            {X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}   {Y}{B}╚══════╝╚═╝  ╚═╝                            {X}       {C}{B}║{X}")
    print(f"  {C}{B}║{X}                                                    {C}{B}║{X}")
    print(f"  {C}{B}╠══════════════════════════════════════════════════╣{X}")
    print(f"  {C}{B}║{X}          {G}{B}BINANCE SQUARE AUTO POSTER{X}                {C}{B}║{X}")
    print(f"  {C}{B}║{X}          {D}CLI Version — by Hanazla{X}                  {C}{B}║{X}")
    print(f"  {C}{B}╚══════════════════════════════════════════════════╝{X}")
    print()

def loading(label, duration=2.5):
    for i in range(int(duration * 20)):
        p = (i % (duration * 20)) / (duration * 20)
        filled = int(30 * p)
        bar = f"{G}{'#' * filled}{D}{'-' * (30 - filled)}{X}"
        sys.stdout.write(f"\r  {D}{label}:{X} {bar} {G}{int(p*100):>3}%{X}")
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write(f"\r  {D}{label}:{X} {G}{'#' * 30}{X} {G}100%{X}\n")
    sys.stdout.flush()

def success(post_id, post_link):
    print()
    print(f"  {G}========================================{X}")
    print(f"  {G}{B}     POST SUCCESSFUL{X}")
    print(f"  {G}========================================{X}")
    print(f"  {C}  ID  :{X} {B}{post_id}{X}")
    print(f"  {C}  Link:{X} {B}{post_link}{X}")
    print(f"  {G}========================================{X}")
    print()

def fail(msg):
    print()
    print(f"  {R}========================================{X}")
    print(f"  {R}{B}     POST FAILED{X}")
    print(f"  {R}========================================{X}")
    print(f"  {Y}  Reason:{X} {msg}")
    print(f"  {R}========================================{X}")
    print()

def menu():
    print(f"  {C}----------------------------------------{X}")
    print(f"  {C}|{X}  {B}1{X}  Set API Key                      {C}|{X}")
    print(f"  {C}|{X}  {B}2{X}  Post Text                        {C}|{X}")
    print(f"  {C}|{X}  {B}3{X}  Post Text + Images               {C}|{X}")
    print(f"  {C}|{X}  {B}4{X}  Exit                             {C}|{X}")
    print(f"  {C}----------------------------------------{X}")
    return input(f"\n  {B}Select [1-4]: {X}").strip()

# ============ MULTI-LINE ============
def get_text():
    """Read multi-line text. Use Ctrl+D or Ctrl+Z to finish."""
    print(f"  {Y}Paste your text below (Ctrl+D to finish):{X}")
    text = ""
    try:
        for line in sys.stdin:
            text += line
        return text.strip()
    except KeyboardInterrupt:
        return ""

# ============ FILE BROWSER ============
def pick_files():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        files = filedialog.askopenfilenames(
            title="Select Images (Max 4)",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.webp")]
        )
        root.destroy()
        return list(files) if files else []
    except:
        return []

# ============ API ============
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

def upload_image(api_key, path, idx, total):
    name = os.path.basename(path)
    mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    sys.stdout.write(f"\r  {C}[{idx}/{total}]{X} {name}...  ")
    sys.stdout.flush()

    res = requests.post(ENDPOINTS["PRESIGNED_IMAGE_URL"], headers=get_headers(api_key),
                        json={"imageName": name})
    data = res.json()
    if data.get("code") != "000000":
        return None, data.get("message")

    presigned = data["data"]["presignedUrl"]
    ticket = data["data"]["fileTicket"]

    with open(path, "rb") as f:
        up = requests.put(presigned, headers={"Content-Type": mime}, data=f)
    if up.status_code != 200:
        return None, f"Upload failed: {up.status_code}"

    for _ in range(15):
        st = requests.post(ENDPOINTS["IMAGE_STATUS"], headers=get_headers(api_key),
                           json={"fileTicket": ticket})
        d = st.json().get("data", {})
        if d.get("status") == 1:
            print(f"\r  {C}[{idx}/{total}]{X} {G}Done{X} {name}")
            return d.get("imageUrl"), None
        elif d.get("status") == 2:
            return None, d.get("failedReason")
        time.sleep(2)
    return None, "Timeout"

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

# ============ MAIN ============
def main():
    api_key = load_api_key()

    while True:
        clear()
        banner()
        choice = menu()

        if choice == '1':
            if api_key:
                print(f"\n  {C}Current:{X} {api_key[:5]}...{api_key[-4:]}")
            else:
                print(f"\n  {Y}No key saved{X}")
            k = input(f"  {C}New API Key: {X}").strip()
            if k:
                save_api_key(k)
                api_key = k
                print(f"  {G}Saved!{X}")
            input(f"  {B}Press Enter...{X}")

        elif choice == '2':
            print(f"\n  {C}--- TEXT POST ---{X}")
            if not api_key:
                print(f"  {R}Set API Key first (option 1){X}")
                input(f"  {B}Press Enter...{X}")
                continue

            text = get_text()
            if not text:
                print(f"  {R}No text entered!{X}")
                input(f"  {B}Press Enter...{X}")
                continue

            loading("Publishing")
            result, err = post_to_binance(api_key, text)
            if err:
                fail(err)
            else:
                success(result.get("id", "N/A"), result.get("shareLink", "N/A"))
            input(f"  {B}Press Enter...{X}")

        elif choice == '3':
            print(f"\n  {C}--- POST WITH IMAGES ---{X}")
            if not api_key:
                print(f"  {R}Set API Key first (option 1){X}")
                input(f"  {B}Press Enter...{X}")
                continue

            text = get_text()
            if not text:
                print(f"  {R}No text entered!{X}")
                input(f"  {B}Press Enter...{X}")
                continue

            print(f"  {Y}Opening file browser...{X}")
            paths = pick_files()

            if not paths:
                print(f"  {Y}No files{X}")
                m = input(f"  {C}Manual paths? (y/n): {X}").strip().lower()
                if m == 'y':
                    r = input(f"  {C}Paths (comma): {X}").strip()
                    paths = [p.strip() for p in r.split(",") if p.strip()]
                else:
                    input(f"  {B}Press Enter...{X}")
                    continue

            if len(paths) > 4:
                paths = paths[:4]

            print(f"\n  {G}Selected:{X}")
            for i, p in enumerate(paths, 1):
                print(f"    {C}[{i}]{X} {os.path.basename(p)}")

            c = input(f"\n  {C}Post? (y/n): {X}").strip().lower()
            if c != 'y':
                print(f"  {Y}Cancelled{X}")
                input(f"  {B}Press Enter...{X}")
                continue

            urls = []
            failed = False
            for i, p in enumerate(paths, 1):
                url, err = upload_image(api_key, p, i, len(paths))
                if err:
                    fail(f"Upload: {err}")
                    failed = True
                    break
                urls.append(url)

            if failed:
                input(f"  {B}Press Enter...{X}")
                continue

            print()
            loading("Publishing")
            result, err = post_to_binance(api_key, text, urls)
            if err:
                fail(err)
            else:
                success(result.get("id", "N/A"), result.get("shareLink", "N/A"))

            input(f"  {B}Press Enter...{X}")

        elif choice == '4':
            print(f"\n  {G}Bye!{X}\n")
            break
        else:
            print(f"  {R}Invalid!{X}")
            input(f"  {B}Press Enter...{X}")

if __name__ == "__main__":
    main()
