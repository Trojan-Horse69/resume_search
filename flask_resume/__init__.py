import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from utils import hf
import logging

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        raise ValueError("No SECRET_KEY set for Flask application. Please set the environment variable.")
    app.config['SECRET_KEY'] = secret_key

    vectorstore = Chroma(embedding_function=hf, persist_directory="./index2_resume_chroma_db")
    app.vectorstore = vectorstore  # Attach vectorstore to app context

    logging.basicConfig(level=logging.INFO)

    from flask_resume.routes import bp as resume_bp
    app.register_blueprint(resume_bp)

    return app
