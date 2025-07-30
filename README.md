## PineText

[![test](https://github.com/ezhuk/pinetext/actions/workflows/test.yml/badge.svg)](https://github.com/ezhuk/pinetext/actions/workflows/test.yml)
[![codecov](https://codecov.io/github/ezhuk/pinetext/graph/badge.svg?token=0YJASFE5OM)](https://codecov.io/github/ezhuk/pinetext)
[![PyPI - Version](https://img.shields.io/pypi/v/pinetext.svg)](https://pypi.org/p/pinetext)

## Getting Started

Use [uv](https://github.com/astral-sh/uv) to add and manage PineText as a dependency in your project, or install it directly via `uv pip install` or `pip install`. See the [Installation](https://github.com/ezhuk/modbus-mcp/blob/main/docs/modbus-mcp/installation.mdx) section of the documentation for full installation instructions and more details.

```bash
uv add pinetext
```

It can also be launched from the command line using the provided `CLI` without modifying the source code.

```
pinetext
```

Or in an ephemeral, isolated environment using `uvx`. Check out the [Using tools](https://docs.astral.sh/uv/guides/tools/) guide for more details.

```bash
uvx pinetext
```

## Docker

The PineText CLI can be deployed as a Docker container as follows:

```bash
docker run -it \
  --name pinetext \
  --env-file .env \
  -v $(pwd)/data:/app/data
  ghcr.io/ezhuk/pinetext:latest
```

## License

The server is licensed under the [MIT License](https://github.com/ezhuk/pinetext?tab=MIT-1-ov-file).
