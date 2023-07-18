from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn
app = FastAPI()

# Set up CORS middleware
origins = ["http://localhost:9000"]  # Update with your front-end URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Mount the "static" directory to serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def show_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard.html")
async def show_form(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/v1/auth/login")
async def login(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    # Your authentication logic here
    # Check username and password against your database or any other data source

    # Redirect the user to another page if login is successful
    return templates.TemplateResponse("dashboard.html", {"request": request})

if __name__ == "__main__":

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=9000,
    )