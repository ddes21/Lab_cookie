## Run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python wsgi.py


### How to build

docker build -t cookie-app .
docker run --rm -p 9000:5000 --name cookie cookie-app


### Hosting

app is hosted http://localhost:9000