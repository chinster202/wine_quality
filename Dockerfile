FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH "/root/.local/bin:$PATH"
ENV UV_SYSTEM_PYTHON 1
RUN which uv && uv --version
# COPY pyproject.toml uv.lock ./
COPY . .
RUN uv sync
EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "src/modeling/main.py"]