# AI Today Japan (Minimal)

Flask + RSS収集 + OpenAI 3行要約 + Render想定

## Local
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=...
python run.py
flask collect
