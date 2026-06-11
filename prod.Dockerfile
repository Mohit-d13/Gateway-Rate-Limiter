# ---------------- Stage 1: Build Dependencies ----------------
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# `UV_COMPILE_BYTECODE=1` enables bytecode compilation (creates .pyc files).
# 'UV_LINK_MODE=copy` Copy from the cached instead of creating symlinks.
# 'UV_PYTHON_DOWNLOADS=0` Disables python downloads to use system interpreter 
ENV UV_COMPILE_BYTECODE=1 \ 
    UV_LINK_MODE=copy \  
    UV_PYTHON_DOWNLOADS=0

# Only install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project

# Copy app source code, uv.lock and pyproject.toml
COPY . .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
    
# ---------------- Stage 2: Final Image ----------------

FROM python:3.12-slim-bookworm

WORKDIR /app

# Create a least privilege user and group,
# without a home directory, no login shell and no password
RUN groupadd --system appgroup && \
    useradd --system \
            --gid appgroup \
            --no-create-home \
            --home-dir /nonexistent \
            --shell /usr/sbin/nologin \
            appuser

# Copy the application source code and dependencies from build stage
COPY --from=builder /app /app

# Place executables in the environmnet
ENV PATH="/app/.venv/bin:$PATH"
 
# Switch to the non-root user
USER appuser

# Run the application
ENTRYPOINT ["uvicorn", "core.main:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
