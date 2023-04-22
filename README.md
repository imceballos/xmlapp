python -m venv env

.\env\Scripts\activate

source venv/bin/activate

pip install -r requirements.txt

uvicorn app:app --reload