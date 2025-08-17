python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

---

docker build -t flask-api .
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-api