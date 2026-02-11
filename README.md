# Akshay Daily Dashboard (Container App)

A simple containerized Python app that displays:

- Current date
- Current weather in **Celina, TX**
- A random motivational quote
- A watermark with the name **Akshay**

## Run locally

```bash
python app.py
```

Then open: <http://localhost:8000>

## Run with Docker

```bash
docker build -t akshay-dashboard .
docker run --rm -p 8000:8000 akshay-dashboard
```

Then open: <http://localhost:8000>
