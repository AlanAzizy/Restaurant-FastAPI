from fastapi import FastAPI
from app.Router.pesanan import pesanan_router
from app.Router.hidanganbahanmakanan import hidanganbahanmakanan_router
from app.Router.bahanmakanan import bahanmakanan_router
from app.Router.menu import menu_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(pesanan_router, prefix="/pesanan")
app.include_router(bahanmakanan_router, prefix="/bahanmakanan")
app.include_router(hidanganbahanmakanan_router, prefix="/hidanganbahanmakanan")
app.include_router(menu_router, prefix="/menu")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)