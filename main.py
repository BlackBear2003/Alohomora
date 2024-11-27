from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from crawler import crawler

app = FastAPI()

app.include_router(crawler.router)

# 设置模板路径
templates = Jinja2Templates(directory="templates")

# 提供静态文件支持，如 CSS 和 JS
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index(request: Request):
    # 渲染前端页面
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
