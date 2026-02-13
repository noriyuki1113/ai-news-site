import feedparser
from datetime import datetime
from app.models.article import Article
from app import db
from config import Config
from app.services.summarizer import summarize_3lines_ja

class AINewsCollector:
    def __init__(self):
        self.feeds = Config.RSS_FEEDS

    def collect_from_rss(self):
        collected_count = 0

        for feed_info in self.feeds:
            print(f"📰 収集中: {feed_info['name']}")

            try:
                feed = feedparser.parse(feed_info["url"])

                for entry in feed.entries[:10]:
                    try:
                        link = getattr(entry, "link", None)
                        title = getattr(entry, "title", "").strip()
                        summary = entry.get("summary", "")[:500]

                        if not link or not title:
                            continue

                        if Article.query.filter_by(url=link).first():
                            continue

                        article = Article(
                            url=link,
                            title=title,
                            snippet=summary,
                            source=feed_info["name"],
                            category=feed_info["category"],
                            published_at=self._parse_date(entry.get("published")),
                        )

                        # 3行要約（APIキーが無い/失敗なら空）
                        article.summary_ja = summarize_3lines_ja(title, summary)
                        article.summary_at = datetime.utcnow() if article.summary_ja else None

                        # 画像拾えるなら拾う（無ければNone）
                        if hasattr(entry, "media_content") and entry.media_content:
                            article.image_url = entry.media_content[0].get("url")
                        elif hasattr(entry, "enclosures") and entry.enclosures:
                            article.image_url = entry.enclosures[0].get("href")

                        db.session.add(article)
                        collected_count += 1
                        print(f"  ✅ 追加: {title[:60]}")

                    except Exception as e:
                        print(f"  ❌ エラー(記事): {str(e)}")
                        continue

                db.session.commit()

            except Exception as e:
                print(f"❌ フィード取得エラー ({feed_info['name']}): {str(e)}")
                continue

        print(f"\n🎉 収集完了: {collected_count}件の新規記事")
        return collected_count

    def _parse_date(self, date_string):
        if not date_string:
            return None
        try:
            from dateutil import parser
            return parser.parse(date_string)
        except Exception:
            return None
