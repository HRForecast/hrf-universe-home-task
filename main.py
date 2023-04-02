import uvicorn
from fastapi import FastAPI
from home_task.endpoints import router


def get_application():
    _app = FastAPI()
    _app.include_router(router)
    return _app


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
