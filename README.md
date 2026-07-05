# EduGenie-Google-Gemini-
EduGenie is a lightweight AI-powered educational assistant designed to simplify and enhance the learning experience through the power of Generative AI. Developed for students, self-learners, and educators.
open ' https://edugenie-google-gemini.onrender.com ' acesses my application.
## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

## Deploy publicly with Render

1. Push this repository to GitHub.
2. Open Render and create a new Web Service from this GitHub repository.
3. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Health Check Path: `/health`
4. Deploy the service.
5. Render will provide a public URL that works on other machines.
