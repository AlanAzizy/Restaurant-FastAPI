from fastapi import FastAPI
from Router.pesanan import pesanan_router
from Router.bahanmenu import bahanmenu_router
from Router.bahanmakanan import bahanmakanan_router
from Router.menu import menu_router
from Router.auth import auth_router
from Router.menupesanan import menupesanan_router
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
app.include_router(bahanmenu_router, prefix="/bahanmenu")
app.include_router(menu_router, prefix="/menu")
app.include_router(menupesanan_router, prefix="/menupesanan")
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)