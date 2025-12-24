from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime

from app.chat.application.use_case.get_chat_history_use_case import GetChatHistoryUseCase
from app.chat.application.port.chat_message_repository_port import ChatMessageRepositoryPort
from app.chat.infrastructure.repository.mysql_chat_message_repository import MySQLChatMessageRepository
from config.database import get_db_session

chat_router = APIRouter()


def get_chat_message_repository() -> ChatMessageRepositoryPort:
    """ChatMessage Repository 의존성 주입"""
    return MySQLChatMessageRepository(get_db_session())


class ChatMessageResponse(BaseModel):
    """채팅 메시지 응답 DTO"""
    id: str
    room_id: str
    sender_id: str
    content: str
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    """채팅 기록 응답 DTO"""
    messages: list[ChatMessageResponse]


@chat_router.get("/chat/{room_id}/messages", response_model=ChatHistoryResponse)
def get_chat_history(
    room_id: str,
    repository: ChatMessageRepositoryPort = Depends(get_chat_message_repository)
):
    """
    채팅방의 메시지 기록을 조회한다.

    - room_id: 채팅방 ID
    - 반환: 시간순으로 정렬된 메시지 목록
    """
    use_case = GetChatHistoryUseCase(repository)
    messages = use_case.execute(room_id)

    message_responses = [
        ChatMessageResponse(
            id=msg.id,
            room_id=msg.room_id,
            sender_id=msg.sender_id,
            content=msg.content,
            created_at=msg.created_at
        )
        for msg in messages
    ]

    return ChatHistoryResponse(messages=message_responses)
