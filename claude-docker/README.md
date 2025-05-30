# Claude Docker Project

This project provides a Docker setup for running Claude code using the `@anthropic-ai/claude-code` package. The Docker image is based on Debian and includes Node.js, Python, and Git, allowing you to manipulate code within a specified working directory.

## Project Structure

```
claude-docker
├── Dockerfile
├── docker-compose.yml
├── scripts
│   └── entrypoint.sh
├── .dockerignore
└── README.md
```

## Getting Started

### Prerequisites

- Docker installed on your machine.
- Basic knowledge of Docker commands.

### Building the Docker Image

To build the Docker image, navigate to the project directory and run:

```bash
docker build -t your-docker-image-name .
```

### Running the Docker Container

To run the Docker container and mount a local folder to the `/workdir` directory in the container, use the following command:

```bash
docker run -v /path/to/your/local/folder:/workdir your-docker-image-name
```

Replace `/path/to/your/local/folder` with the path to the folder you want to mount.

### Accessing Claude

Once the container is running, the `claude` command will be executed automatically. You can interact with the Claude code environment as needed.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.