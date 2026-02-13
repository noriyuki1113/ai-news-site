from flask import Blueprint, jsonify, request
from app.models.article import Article
from app import db

api_bp = Blueprint("api", __name__)

@api_bp.route("/articles")
def get_articles():
    category = request.args.get("category")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    query = Article.query
    if category:
        query = query.filter_by(category=category)

    articles = query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "articles": [a.to_dict() for a in articles.items],
            "total": articles.total,
            "pages": articles.pages,
            "current_page": page,
        }
    )

@api_bp.route("/articles/<int:article_id>")
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify(article.to_dict())

@api_bp.route("/trending")
def get_trending():
    articles = Article.get_trending(limit=10)
    return jsonify([a.to_dict() for a in articles])

@api_bp.route("/categories")
def get_categories():
    categories = db.session.query(Article.category).distinct().all()
    return jsonify([c[0] for c in categories if c[0]])
