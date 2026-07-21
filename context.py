from dataclasses import dataclass
from skipped import SkippedPosts
from auth import Auth
from commentary import Commentary
import settings

@dataclass
class PostInfo:
    id: int
    source: str
    gentags: list[str]
    copytags: list[str]
    chartags: list[str]
    metatags: list[str]

    @classmethod
    def from_json(cls, json):
        return cls(
            json["id"],
            json["source"],
            json["tag_string_general"].split(),
            json["tag_string_copyright"].split(),
            json["tag_string_character"].split(),
            json["tag_string_meta"].split())

@dataclass
class OfflineContext:
    tag_script: dict[int, str]
    output: str
    commentary: Commentary
    post_count: int
    index: int

@dataclass
class ExecutionContext:
    skipped_posts: SkippedPosts
    edit_count: int

class NetworkContext:
    def __init__(self, auth, test_mode):
        self.auth = auth
        self.test_mode = test_mode
        self.headers = {
            "User-Agent": settings.HEADERS
        }
