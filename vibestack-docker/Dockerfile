FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for both Claude and NoVNC functionality
RUN apt-get update && apt-get install -y \
    # Claude dependencies
    curl \
    wget \
    python3 \
    python3-pip \
    git \
    jq \
    vim \
    nano \
    htop \
    # NoVNC dependencies
    xvfb \
    x11vnc \
    novnc \
    websockify \
    xfce4 \
    xfce4-terminal \
    firefox \
    supervisor \
    dbus-x11 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (LTS version)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*

# Install Claude Code
RUN npm install -g @anthropic-ai/claude-code

# Copy configuration files
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN chmod +x /usr/local/bin/entrypoint.sh

# Create required directories
RUN mkdir -p /var/log/supervisor /var/run

# Set the working directory
WORKDIR /workdir

# Environment variables
ENV DISPLAY=:0
ENV NOVNC_PORT=6080
ENV VNC_PORT=5900
ENV RESOLUTION=1280x720

# Expose NoVNC port (for future use)
EXPOSE 6080

# Start with Claude for now
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]