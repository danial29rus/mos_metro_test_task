import uvicorn
from fastapi import FastAPI

from app.transport.api import router


def get_application() -> FastAPI:
    application = FastAPI(
        title="News API",
        debug=False,
        redoc_url="/api/docs/_r",
        docs_url="/api/docs/_s",
        max_upload_size=20 * 1024 * 1024,
    )

    application.include_router(router)

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="localhost", port=8010, workers=2, reload=True
    )
