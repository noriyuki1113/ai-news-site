import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///ai_news.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SITE_NAME = "AI Today Japan"
    SITE_DESCRIPTION = "最新のAI・機械学習ニュースをお届け"
    ARTICLES_PER_PAGE = 20

    RSS_FEEDS = [
        {"url": "https://openai.com/blog/rss/", "name": "OpenAI Blog", "category": "AI企業"},
        {"url": "https://blog.google/technology/ai/rss/", "name": "Google AI Blog", "category": "AI企業"},
        {"url": "https://www.anthropic.com/news/rss.xml", "name": "Anthropic", "category": "AI企業"},
        {"url": "https://techcrunch.com/tag/artificial-intelligence/feed/", "name": "TechCrunch AI", "category": "AIニュース"},
        {"url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "name": "The Verge AI", "category": "AIニュース"},
    ]

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
