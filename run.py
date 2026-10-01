import os
import sys
import webbrowser
import threading
import time

def open_browser():
    time.sleep(1.2)
    print("Opening Campus-AI in default browser: http://localhost:5000")
    webbrowser.open("http://localhost:5000")

if __name__ == "__main__":
    from app import app
    print("=" * 70)
    print("🚀 Campus-AI: Intelligent Student Support System (ABESEC)")
    print("   Status: Autonomous since 2025 | Knowledge Corpus v5.0")
    print("   Serving on: http://localhost:5000")
    print("=" * 70)
    
    # Launch browser automatically
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=False)
