#!/bin/bash
set -e

# Vibestack Combined Container Entrypoint
# Currently runs Claude Code, with NoVNC infrastructure ready for future use

# Set up the environment
export HOME=/root
cd /workdir

# Check if Claude Code is properly installed
if ! command -v claude &> /dev/null; then
    echo "Error: Claude Code is not installed or not in PATH"
    exit 1
fi

# Display system info for debugging
echo "=== Vibestack Combined Container ==="
echo "Claude Code version: $(claude --version 2>/dev/null || echo 'unknown')"
echo "Working directory: $(pwd)"
echo "Node.js version: $(node --version)"
echo "jq version: $(jq --version)"
echo "VNC infrastructure: Available (not started)"
echo "NoVNC port: $NOVNC_PORT (not active)"
echo "===================================="

# For now, just run Claude Code
# TODO: Add logic to optionally start NoVNC services via supervisor
exec claude "$@"