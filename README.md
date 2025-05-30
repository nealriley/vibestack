# Vibestack

A Docker-based development environment featuring Claude Code, NoVNC remote desktop, and essential development tools.

## Components

### claude-docker
- **Base**: Ubuntu 22.04
- **Tools**: Claude Code, Node.js, Python3, Git, jq, vim, nano, htop
- **Purpose**: Interactive Claude Code environment with development tools

### novnc-docker  
- **Base**: Ubuntu 22.04
- **Desktop**: XFCE4 with Firefox
- **Access**: NoVNC web interface on port 6080
- **Purpose**: Remote desktop environment accessible via web browser

## Quick Start

1. **Start all services**:
   ```bash
   docker-compose up -d
   ```

2. **Access NoVNC**: Open http://localhost:6080 in your browser

3. **Interact with Claude**:
   ```bash
   docker-compose exec claude claude
   ```

4. **View logs**:
   ```bash
   docker-compose logs -f
   ```

## Configuration

### Environment Variables

**NoVNC Container**:
- `RESOLUTION`: Screen resolution (default: 1280x720)
- `VNC_PORT`: VNC server port (default: 5900)
- `NOVNC_PORT`: NoVNC web interface port (default: 6080)

### Volumes

- `./workdir`: Shared workspace mounted in Claude container
- `claude-home`: Persistent home directory for Claude container

## Service Management

Services are managed using supervisor in the NoVNC container:
- **Xvfb**: Virtual framebuffer
- **x11vnc**: VNC server
- **NoVNC**: Web-based VNC client
- **XFCE4**: Desktop environment

## Stopping Services

```bash
docker-compose down
```

To remove volumes:
```bash
docker-compose down -v
```