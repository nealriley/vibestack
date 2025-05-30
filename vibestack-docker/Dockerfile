FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install packages for VNC and desktop environment + Claude dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        xvfb \
        x11vnc \
        novnc \
        websockify \
        xfce4 \
        xfce4-terminal \
        firefox \
        wget \
        curl \
        supervisor \
        dbus-x11 \
        python3 \
        python3-pip \
        git \
        jq \
        vim \
        nano \
        htop \
        && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN wget https://github.com/tsl0922/ttyd/releases/download/1.6.3/ttyd.x86_64 -O /usr/bin/ttyd && \
    chmod +x /usr/bin/ttyd

# Install Node.js (LTS version)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*

# Install Claude Code
RUN npm install -g @anthropic-ai/claude-code

RUN npm install -g playwright-mcp

RUN npx -y playwright install chrome

# Copy supervisor configuration and Claude config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create required directories
RUN mkdir -p /var/log/supervisor /var/run

RUN claude mcp add --transport sse playwright http://127.0.0.1:7777/sse
# Set the working directory
WORKDIR /workdir

# Environment variables
ENV DISPLAY=:0
ENV NOVNC_PORT=6080
ENV VNC_PORT=5900
ENV RESOLUTION=1280x720

# Expose only the noVNC port
EXPOSE 6080 7681 7777

# Run supervisor directly to manage all services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
