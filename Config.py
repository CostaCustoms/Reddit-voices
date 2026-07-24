"""
Shared config for all 5 faceless narration channels. Each channel is a fork of
MissingVoices' architecture (research -> script -> media -> upload), parameterized
here rather than duplicated per-channel.
"""
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

load_dotenv(Path(r"E:\TradingBrain\trading\.env"), override=False)
load_dotenv(BASE_DIR / ".env", override=False)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = "RedditVoices/1.0 (personal narration project)"

# Kokoro TTS (same model files MissingVoices already uses -- shared, not duplicated)
KOKORO_MODEL = r"E:\MissingVoices\models\kokoro-v1.0.onnx"
KOKORO_VOICES = r"E:\MissingVoices\models\voices-v1.0.bin"

CHANNELS = {
    "work_stories": {
        "label": "Work Stories",
        "source": "reddit",
        "subreddits": ["MaliciousCompliance", "ProRevenge", "TalesFromTechSupport",
                        "IDontWorkHereLady", "talesfromretail", "antiwork", "tifu"],
        "compilation_subreddits": ["Construction", "Welding", "electricians", "Plumbing", "AskReddit"],
        "voice": "am_adam",
        "youtube_client_secret_env": "WORKSTORIES_YT_CLIENT_SECRET_FILE",
        "youtube_token_env": "WORKSTORIES_YT_TOKEN_FILE",
        "facebook_page_id_env": "WORKSTORIES_FB_PAGE_ID",
        "facebook_token_env": "WORKSTORIES_FB_TOKEN",
    },
    "drama": {
        "label": "Drama",
        "source": "reddit",
        "subreddits": ["AmItheAsshole", "TrueOffMyChest", "survivinginfidelity",
                        "relationship_advice", "BestofRedditorUpdates"],
        "compilation_subreddits": [],
        "voice": "af_heart",
        "youtube_client_secret_env": "DRAMA_YT_CLIENT_SECRET_FILE",
        "youtube_token_env": "DRAMA_YT_TOKEN_FILE",
        "facebook_page_id_env": "DRAMA_FB_PAGE_ID",
        "facebook_token_env": "DRAMA_FB_TOKEN",
    },
    "on_this_day": {
        "label": "On This Day",
        "source": "wikipedia_otd",
        "voice": "bm_george",
        "youtube_client_secret_env": "OTD_YT_CLIENT_SECRET_FILE",
        "youtube_token_env": "OTD_YT_TOKEN_FILE",
        "facebook_page_id_env": "OTD_FB_PAGE_ID",
        "facebook_token_env": "OTD_FB_TOKEN",
    },
    "declassified": {
        "label": "Declassified Files",
        "source": "declassified_tbd",  # feasibility unconfirmed -- see build notes
        "voice": "am_michael",
        "youtube_client_secret_env": "DECLASS_YT_CLIENT_SECRET_FILE",
        "youtube_token_env": "DECLASS_YT_TOKEN_FILE",
        "facebook_page_id_env": "DECLASS_FB_PAGE_ID",
        "facebook_token_env": "DECLASS_FB_TOKEN",
    },
    "disasters": {
        "label": "Disaster Retellings",
        "source": "nws_storms_tbd",  # feasibility unconfirmed -- see build notes
        "voice": "af_heart",
        "youtube_client_secret_env": "DISASTERS_YT_CLIENT_SECRET_FILE",
        "youtube_token_env": "DISASTERS_YT_TOKEN_FILE",
        "facebook_page_id_env": "DISASTERS_FB_PAGE_ID",
        "facebook_token_env": "DISASTERS_FB_TOKEN",
    },
}

POSTS_PER_RUN = 5
SHORTS_TARGET_SECONDS = 75
