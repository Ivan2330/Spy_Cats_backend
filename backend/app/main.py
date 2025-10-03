from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.errors import install_error_handlers
from app.core.logging import setup_logging
from app.routers.health import router as health_router
from app.routers.cats import router as cats_router
from app.routers.missions import router as missions_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Spy Cat Agency API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # logging
    try:
        setup_logging()
    except Exception:
        pass

    # CORS
    origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # errors
    try:
        install_error_handlers(app)
    except Exception:
        pass


    app.include_router(health_router)
    app.include_router(cats_router)
    app.include_router(missions_router)

    return app

app = create_app()
