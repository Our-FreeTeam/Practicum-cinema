from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec

app = Flask(__name__)

api = FlaskPydanticSpec('flask')
