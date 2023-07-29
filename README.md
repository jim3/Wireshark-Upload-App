### FastAPI Wireshark Uploader App

Uses the FastAPI framework to create a REST API that allows users to upload their exported Wireshark files (JSON format) to a MongoDB Atlas database. The app is written in Python and uses the PyMongo library to connect to MongoDB Atlas. After each upload, the `packets` endpoint returns the extracted results to the client.

Uses Python's Poetry package manager to manage dependencies.

## Installation

1. Clone the repository
2. Install Poetry
3. Run `poetry install` to install dependencies
4. Run `poetry shell` to activate the virtual environment
5. Run `uvicorn app:app --reload` to start the server

## Usage

1. Open a browser and navigate to `http://127.0.0.1:8000/`

2. Upload a Wireshark JSON file

3. After the upload is complete, you'll be redirected to the `packets` endpoint, which will display the extracted results from the uploaded file
