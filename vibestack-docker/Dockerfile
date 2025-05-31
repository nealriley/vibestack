FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install packages for VNC and desktop environment + Claude dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
        xvfb \
        x11vnc \
        novnc \
        websockify \
        wmaker \
        xterm \
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
        figlet \
        ruby \
        nginx \
        whiptail

# Install lolcat via gem
RUN gem install lolcat
RUN wget https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 -O /usr/bin/ttyd && \
    chmod +x /usr/bin/ttyd

# Install Node.js (LTS version)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*

# Install Claude Code
RUN npm install -g @anthropic-ai/claude-code

RUN npm install -g playwright-mcp

RUN npx -y playwright install chrome

# RUN curl -LsSf https://astral.sh/uv/install.sh | bash - 

RUN pip install llm

# Copy supervisor configuration, nginx config, Claude config, and autostart
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY .bashrc /root/.bashrc
COPY terminal-autostart.desktop /root/.config/autostart/terminal-autostart.desktop
COPY vibestack-kickstart.sh /root/vibestack-kickstart.sh
# Create required directories
RUN mkdir -p /var/log/supervisor /var/run /root/.config/autostart

# MCP server configuration moved to interactive startup menu
# Set the working directory
WORKDIR /workdir

# Environment variables
ENV DISPLAY=:0
ENV NOVNC_PORT=6080
ENV VNC_PORT=5900
ENV RESOLUTION=1280x720

# Expose only the nginx port (80)
EXPOSE 80

# Run supervisor directly to manage all services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
