# Vibestack Docker

Combined container with both Claude Code and NoVNC capabilities.

## Current Configuration

**Active**: Claude Code only
**Available**: Full NoVNC infrastructure (WindowMaker, VNC, NoVNC web interface)

## Architecture

- **Base**: Ubuntu 22.04
- **Claude**: Node.js + Claude Code + development tools (jq, git, vim, etc.)
- **NoVNC**: WindowMaker + VNC + NoVNC web interface (installed but not started)
- **Service Management**: Supervisor (configured but not active)

## Current Usage

The container currently runs Claude Code in interactive mode:

```bash
docker-compose up vibestack
docker-compose exec vibestack claude
```

## Future Expansion

To enable NoVNC services, modify `entrypoint.sh` to:
1. Start supervisor instead of claude directly
2. Set `autostart=true` for desired services in `supervisord.conf`
3. Access NoVNC at http://localhost:6080

## Files

- `Dockerfile`: Combined installation of Claude + NoVNC packages
- `entrypoint.sh`: Currently starts Claude, ready for supervisor integration
- `supervisord.conf`: Service definitions (autostart=false for VNC services)
- `README.md`: This documentation