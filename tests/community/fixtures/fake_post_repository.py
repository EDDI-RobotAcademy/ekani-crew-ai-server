from app.community.application.port.post_repository_port import PostRepositoryPort
from app.community.domain.post import Post, PostType


class FakePostRepository(PostRepositoryPort):
    """테스트용 Fake 게시글 저장소"""

    def __init__(self):
        self._posts: dict[str, Post] = {}

    def save(self, post: Post) -> None:
        self._posts[post.id] = post

    def find_by_id(self, post_id: str) -> Post | None:
        return self._posts.get(post_id)

    def find_all(self) -> list[Post]:
        posts = list(self._posts.values())
        return sorted(posts, key=lambda p: p.created_at, reverse=True)

    def find_by_post_type(self, post_type: PostType) -> list[Post]:
        posts = [p for p in self._posts.values() if p.post_type == post_type]
        return sorted(posts, key=lambda p: p.created_at, reverse=True)
