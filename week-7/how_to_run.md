streamlit run src/deployment/streamlit_app.py


python -m uvicorn src.deployment.app:app --reload
