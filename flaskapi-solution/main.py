from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = FlaskPydanticSpec('flask')
