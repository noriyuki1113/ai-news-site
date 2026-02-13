from flask import Blueprint, render_template, request, redirect, url_for
from app.models.article import Article
from app import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    category = request.args.get("category")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    query = Article.query
    if category:
        query = query.filter_by(category=category)

    articles = query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    categories = db.session.query(Article.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    return render_template(
        "index.html",
        articles=articles.items,
        pagination=articles,
        categories=categories,
        current_category=category,
    )

@main_bp.route("/article/<int:article_id>")
def article_detail(article_id):
    article = Article.query.get_or_404(article_id)
    Article.increment_views(article_id)

    related = (
        Article.query.filter_by(category=article.category)
        .filter(Article.id != article_id)
        .order_by(Article.created_at.desc())
        .limit(5)
        .all()
    )

    categories = db.session.query(Article.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    return render_template(
        "article.html",
        article=article,
        related_articles=related,
        categories=categories,
        current_category=None,
    )

@main_bp.route("/trending")
def trending():
    articles = Article.get_trending(limit=20)

    categories = db.session.query(Article.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    return render_template(
        "trending.html",
        articles=articles,
        categories=categories,
        current_category=None,
    )

@main_bp.route("/search")
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return redirect(url_for("main.index"))

    articles = (
        Article.query.filter(Article.title.contains(q) | Article.snippet.contains(q))
        .order_by(Article.created_at.desc())
        .limit(50)
        .all()
    )

    categories = db.session.query(Article.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    return render_template(
        "search.html",
        articles=articles,
        query=q,
        categories=categories,
        current_category=None,
    )
