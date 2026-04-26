from fastapi import FastAPI
from router import router

app = FastAPI(title='Redirect Service API')
app.include_router(router)
