FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install packages for VNC and desktop environment
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
        && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create required directories
RUN mkdir -p /var/log/supervisor /var/run

# Environment variables
ENV DISPLAY=:0
ENV NOVNC_PORT=6080
ENV VNC_PORT=5900
ENV RESOLUTION=1280x720

# Expose only the noVNC port
EXPOSE 6080

# Run supervisor directly to manage all services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
