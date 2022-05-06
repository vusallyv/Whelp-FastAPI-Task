# Whelp-Task

# 1. FastAPI project
uvicorn main:app --reload

# 2. Celery worker in background.
celery -A tasks.tasks worker --loglevel=info

# 3. Unit Tests
python -m pytest tests/tests.py
