from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Chillzone API",
        version="0.0.1",
        description="API for Chillzone guild",
        docs_url="/docs",
        debug=True,
    )

    return app
