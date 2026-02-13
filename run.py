import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app, db
from app.models import Article

env = os.environ.get("FLASK_ENV", "development")
app = create_app(env)

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Article": Article}

@app.cli.command()
def init_db():
    db.create_all()
    print("✅ データベーステーブルを作成しました")

@app.cli.command()
def collect():
    from app.collectors.ai_collector import AINewsCollector
    with app.app_context():
        collector = AINewsCollector()
        count = collector.collect_from_rss()
        print(f"✅ {count}件の記事を収集しました")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
