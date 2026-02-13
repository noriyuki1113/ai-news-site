import os
from openai import OpenAI

def summarize_3lines_ja(title: str, snippet: str) -> str:
    title = (title or "").strip()
    snippet = (snippet or "").strip()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return ""

    client = OpenAI(api_key=api_key)

    prompt = (
        "以下のニュース情報を、自然な日本語で「3行」要約してください。\n"
        "ルール:\n"
        "- 必ず3行（改行で3段）\n"
        "- 1行は全角35文字以内を目安\n"
        "- 憶測や誇張は禁止。書いてある事実だけ\n"
        "- 固有名詞はなるべく保持\n"
        "- 箇条書き記号は使わない\n\n"
        f"タイトル: {title}\n"
        f"概要: {snippet}\n"
    )

    try:
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )
        text = (resp.output_text or "").strip()

        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if len(lines) >= 3:
            return "\n".join(lines[:3])
        if len(lines) == 2:
            return "\n".join(lines + [""])
        if len(lines) == 1:
            return "\n".join([lines[0], "", ""])
        return ""
    except Exception:
        return ""
