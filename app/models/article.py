from datetime import datetime
from app import db

class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False, index=True)
    title = db.Column(db.String(300), nullable=False)
    snippet = db.Column(db.Text)
    content = db.Column(db.Text)

    # 3行要約（日本語）
    summary_ja = db.Column(db.Text)
    summary_at = db.Column(db.DateTime)

    source = db.Column(db.String(100))
    category = db.Column(db.String(50), index=True)
    image_url = db.Column(db.String(500))
    author = db.Column(db.String(200))
    published_at = db.Column(db.DateTime)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Article {self.title}>"

    def to_dict(self):
        snippet = self.snippet or ""
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "snippet": snippet[:200] if snippet else "",
            "summary_ja": self.summary_ja,
            "source": self.source,
            "category": self.category,
            "image_url": self.image_url,
            "author": self.author,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "views": self.views,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def get_latest(limit=20, category=None):
        query = Article.query
        if category:
            query = query.filter_by(category=category)
        return query.order_by(Article.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_trending(limit=10):
        return Article.query.order_by(Article.views.desc()).limit(limit).all()

    @staticmethod
    def increment_views(article_id):
        article = Article.query.get(article_id)
        if article:
            article.views += 1
            db.session.commit()
