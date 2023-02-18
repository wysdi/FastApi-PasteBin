from fastapi import FastAPI
# from events import create_start_app_handler, create_stop_app_handler
from router import router


def get_application() -> FastAPI:
    application = FastAPI(
        title='Paste Bin',
    )

    application.include_router(router)
    return application

app = get_application()