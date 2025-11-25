"""Main module for {{cookiecutter.project_name}}."""
{% if cookiecutter.include_cdk == 'yes' %}
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from {{cookiecutter.package_name}} import logging_config

logger = logging_config.get_logger('{{cookiecutter.package_name}}.main')


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    logger.info("Starting {{cookiecutter.project_name}}...")
    yield
    logger.info("Shutting down {{cookiecutter.project_name}}...")


app = FastAPI(
    title="{{cookiecutter.project_name}}",
    description="{{cookiecutter.description}}",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint."""
    return JSONResponse({
        "message": "Hello from {{cookiecutter.project_name}}!",
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "development")
    })


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "{{cookiecutter.project_name}}"
    })


def main() -> None:
    """Main entry point."""
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "{{cookiecutter.package_name}}.main:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT") != "prod",
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )


if __name__ == "__main__":
    main()
{% else %}
from {{cookiecutter.package_name}} import logging_config

logger = logging_config.get_logger('{{cookiecutter.package_name}}.main')

def main() -> None:
    """Main entry point."""
    logger.info("Hello from {{cookiecutter.project_name}}!")


if __name__ == "__main__":
    main()
{% endif %}