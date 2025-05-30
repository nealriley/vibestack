#!/bin/bash
set -e

# Vibestack Claude Container Entrypoint
# Ensures Claude Code is available and starts in interactive mode

# Set up the environment
export HOME=/root
cd /workdir

# Check if Claude Code is properly installed
if ! command -v claude &> /dev/null; then
    echo "Error: Claude Code is not installed or not in PATH"
    exit 1
fi

# Display system info for debugging
echo "=== Vibestack Claude Container ==="
echo "Claude Code version: $(claude --version 2>/dev/null || echo 'unknown')"
echo "Working directory: $(pwd)"
echo "Node.js version: $(node --version)"
echo "jq version: $(jq --version)"
echo "================================="

# Execute Claude with any passed arguments, defaulting to interactive mode
exec claude "$@"