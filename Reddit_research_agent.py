"""
Research Agent (Reddit) — pulls real posts via Reddit's official API (PRAW), not
scraping. The old .json-endpoint trick is dead (confirmed 2026-07-23: hard 403,
"blocked" -- Reddit locked it down after their 2023 API changes). Needs a free
Reddit "script" app (reddit.com/prefs/apps) -- REDDIT_CLIENT_ID/SECRET in .env.
No AI involved here -- source text only, same separation-of-concerns as
MissingVoices' research_agent (facts first, AI narrates later against a fact block).
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import praw

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DATA_DIR, POSTS_PER_RUN, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, CHANNELS

MIN_WORDS = 300     # too short to make a real narrated story
MAX_WORDS = 4000    # too long for a single video without heavy trimming


def _reddit():
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        raise RuntimeError(
            "REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET not set. "
            "Register a free 'script' app at reddit.com/prefs/apps and add both to .env."
        )
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )


def _word_count(text: str) -> int:
    return len(text.split())


def _parse_submission(sub) -> dict | None:
    if sub.stickied or sub.over_18:
        return None
    body = (sub.selftext or "").strip()
    wc = _word_count(body)
    if wc < MIN_WORDS or wc > MAX_WORDS:
        return None
    if sub.removed_by_category or body in ("[removed]", "[deleted]", ""):
        return None
    return {
        "post_id": sub.id,
        "subreddit": sub.subreddit.display_name,
        "title": sub.title.strip(),
        "body": body,
        "word_count": wc,
        "score": sub.score,
        "num_comments": sub.num_comments,
        "created_utc": sub.created_utc,
        "permalink": f"https://reddit.com{sub.permalink}",
        "flair": sub.link_flair_text or "",
        "source": "Reddit (official API)",
        "scraped_at": datetime.utcnow().isoformat(),
    }


def run_research(channel_key: str, limit: int = POSTS_PER_RUN, time_filter: str = "week") -> list[dict]:
    """Pull top posts from a channel's configured subreddits over the given window.
    time_filter: hour/day/week/month/year/all (praw's top() windows)."""
    chan = CHANNELS[channel_key]
    if chan["source"] != "reddit":
        raise ValueError(f"{channel_key} is not a Reddit-sourced channel")

    reddit = _reddit()
    posts = []
    print(f"Research Agent ({chan['label']}): pulling from r/{', r/'.join(chan['subreddits'])}...")

    for sub_name in chan["subreddits"]:
        if len(posts) >= limit * 3:
            break
        try:
            for submission in reddit.subreddit(sub_name).top(time_filter=time_filter, limit=15):
                parsed = _parse_submission(submission)
                if parsed:
                    posts.append(parsed)
                    print(f"  + [{sub_name}] \"{parsed['title'][:60]}\" ({parsed['word_count']} words, score {parsed['score']})")
        except Exception as e:
            print(f"  ! r/{sub_name} failed: {e}")

    posts.sort(key=lambda p: p["score"], reverse=True)
    posts = posts[:limit]

    out_dir = DATA_DIR / "posts" / channel_key
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"posts_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

    print(f"Research Agent: saved {len(posts)} posts to {out_file.name}")
    return posts


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "work_stories"
    result = run_research(key)
    print(f"\n{len(result)} posts ready for Script Agent.")
