FROM python:3.11-slim

WORKDIR /app

# Copy configuration first for better caching
COPY pyproject.toml .

# Copy the source code and documentation
COPY nba_cli/ ./nba_cli/
COPY README.md .

# Install the package
RUN pip install --no-cache-dir .

# Create a non-root user
RUN useradd -m appuser
USER appuser

ENTRYPOINT ["nba-cli"]
CMD ["--help"]