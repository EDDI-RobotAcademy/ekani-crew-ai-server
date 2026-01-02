import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.community.adapter.input.web.post_router import post_router, get_post_repository
from app.community.application.port.post_repository_port import PostRepositoryPort
from app.community.domain.post import Post, PostType
from tests.community.fixtures.fake_post_repository import FakePostRepository


@pytest.fixture
def fake_repository():
    return FakePostRepository()


@pytest.fixture
def client(fake_repository):
    app = FastAPI()
    app.include_router(post_router, prefix="/community")

    def override_get_repository():
        return fake_repository

    app.dependency_overrides[get_post_repository] = override_get_repository
    return TestClient(app)


class TestPostRouter:
    """Post API 라우터 테스트"""

    def test_create_topic_post(self, client):
        """토픽 게시글을 생성할 수 있다"""
        response = client.post(
            "/community/posts",
            json={
                "author_id": "user-1",
                "title": "INTJ 남자 원래 이런가요?",
                "content": "INTJ 남친이 답장을 안 해요...",
                "post_type": "topic",
                "topic_id": "topic-1",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "INTJ 남자 원래 이런가요?"
        assert data["post_type"] == "topic"
        assert data["topic_id"] == "topic-1"
        assert "id" in data

    def test_create_free_post(self, client):
        """자유 게시글을 생성할 수 있다"""
        response = client.post(
            "/community/posts",
            json={
                "author_id": "user-2",
                "title": "ENFP인데 썸남 MBTI 모르겠어요",
                "content": "어떻게 알 수 있을까요?",
                "post_type": "free",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["post_type"] == "free"
        assert data["topic_id"] is None

    def test_get_post_by_id(self, client, fake_repository):
        """게시글 상세를 조회할 수 있다 (SEO용 고유 URL)"""
        post = Post(
            id="post-1",
            author_id="user-1",
            title="INTJ 남자 원래 이런가요?",
            content="INTJ 남친이 답장을 안 해요...",
            post_type=PostType.TOPIC,
            topic_id="topic-1",
        )
        fake_repository.save(post)

        response = client.get("/community/posts/post-1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "post-1"
        assert data["title"] == "INTJ 남자 원래 이런가요?"

    def test_get_post_not_found(self, client):
        """존재하지 않는 게시글 조회 시 404를 반환한다"""
        response = client.get("/community/posts/non-existent")

        assert response.status_code == 404
