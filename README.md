python -m venv xmlapp

.\env\Scripts\activate

pip install -r requirements.txt

uvicorn app:app --reload