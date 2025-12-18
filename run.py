import os
import sys
import subprocess
import webbrowser
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.join(ROOT, "backend")
FRONTEND = os.path.join(ROOT, "frontend", "index.html")

def run(cmd, cwd=None):
    subprocess.check_call(cmd, cwd=cwd, shell=(os.name == "nt"))

def main():
    print("🥗 Starting MealMind...")

    venv = os.path.join(BACKEND, ".venv")
    python = sys.executable

    # Create venv if missing
    if not os.path.exists(venv):
        print("🔧 Creating virtual environment...")
        run([python, "-m", "venv", ".venv"], cwd=BACKEND)

    # Activate paths
    pip = os.path.join(venv, "Scripts" if os.name == "nt" else "bin", "pip")
    uvicorn = os.path.join(venv, "Scripts" if os.name == "nt" else "bin", "uvicorn")

    # Install deps
    print("📦 Installing dependencies...")
    run([pip, "install", "-r", "requirements.txt"], cwd=BACKEND)

    # Start backend
    print("🚀 Launching backend...")
    subprocess.Popen(
        [uvicorn, "main:app", "--reload"],
        cwd=BACKEND,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait a sec for server
    time.sleep(2)

    # Open frontend
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:8000/health")
    webbrowser.open(f"file://{FRONTEND}")

    print("✅ MealMind is running. Close this window to stop.")

    # Keep process alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
