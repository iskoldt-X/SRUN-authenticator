# SRUN Authenticator Pro v2.1

A high-performance, containerized campus network authenticator.
"Talk is cheap. Show me the code." - Linus Torvalds

## Features
- **Zero Globals**: Structured as a robust client.
- **Vigilant Loop**: High-frequency connectivity checking with configurable intervals.
- **Graceful Termination**: Handles `SIGTERM/SIGINT` for clean Docker exits.
- **Pro CI**: Automated unit testing before every Docker build.
- **Multi-stage Docker**: Tiny footprint, runs as a non-root user.

## Quick Start
```bash
# Set your environment variables
export USERNAME=your_username
export PASSWORD=your_password

# Use the Makefile
make install
make test
make run
```

## Docker
```bash
docker build -t srun-authenticator -f Dockerfile.pro .
docker run --rm \
  -e USERNAME=xxx \
  -e PASSWORD=yyy \
  srun-authenticator
```

## Protocol
The SRUN authentication protocol uses a custom Base64 implementation combined with a proprietary variant of the TEA block cipher (XEncode). This script implements those primitives in pure Python for maximum portability.
