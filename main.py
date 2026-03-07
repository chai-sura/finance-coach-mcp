"""
Main entry point for Finance Coach MCP.
Runs the MCP server and Streamlit dashboard.

Usage:
    # Run MCP server only
    python main.py --mode mcp

    # Run Streamlit dashboard only
    python main.py --mode dashboard

    # Run both together (default)
    python main.py
"""

import argparse
import subprocess
import sys
import os
from dotenv import load_dotenv

load_dotenv()


def run_mcp_server():
    """Start the MCP server."""
    print("🤖 Starting Finance Coach MCP Server...")
    from mcp_server.server import mcp
    mcp.run()


def run_dashboard():
    """Start the Streamlit dashboard."""
    print("🌐 Starting Finance Coach Dashboard...")
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard", "app.py")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", dashboard_path,
        "--server.port", "8501",
        "--server.headless", "false"
    ])


def run_both():
    """Run MCP server and Streamlit dashboard together."""
    import threading

    print("🚀 Starting Finance Coach MCP...")
    print("─" * 40)
    print("🤖 MCP Server    → connecting to AI tools")
    print("🌐 Dashboard     → http://localhost:8501")
    print("─" * 40)

    # Run MCP server in background thread
    mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
    mcp_thread.start()

    # Run dashboard in main thread
    run_dashboard()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finance Coach MCP")
    parser.add_argument(
        "--mode",
        choices=["mcp", "dashboard", "both"],
        default="both",
        help="What to run: mcp, dashboard, or both (default: both)"
    )

    args = parser.parse_args()

    if args.mode == "mcp":
        run_mcp_server()
    elif args.mode == "dashboard":
        run_dashboard()
    else:
        run_both()