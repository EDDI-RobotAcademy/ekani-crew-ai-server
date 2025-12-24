import uuid
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from app.mbti_test.application.use_case.start_mbti_test import StartMBTITestUseCase, StartMBTITestCommand
from app.mbti_test.domain.mbti_test_session import TestType
from app.auth.adapter.input.web.auth_dependency import get_current_user_id
from app.mbti_test.application.port.outgoing.mbti_test_session_repository import MBTITestSessionRepository
from app.mbti_test.application.port.outgoing.question_set_provider import QuestionSetProvider
from app.mbti_test.infrastructure.repository.in_memory_mbti_test_session_repository import InMemoryMBTITestSessionRepository
from app.mbti_test.infrastructure.service.in_memory_question_set_provider import InMemoryQuestionSetProvider

mbti_router = APIRouter()

def get_session_repository() -> MBTITestSessionRepository:
    return InMemoryMBTITestSessionRepository()

def get_question_set_provider() -> QuestionSetProvider:
    return InMemoryQuestionSetProvider()

@mbti_router.post("/start")
async def start_mbti_test(
    test_type: TestType,
    user_id: str = Depends(get_current_user_id),
    session_repository: MBTITestSessionRepository = Depends(get_session_repository),
    question_set_provider: QuestionSetProvider = Depends(get_question_set_provider)
):
    use_case = StartMBTITestUseCase(session_repository, question_set_provider)
    command = StartMBTITestCommand(user_id=uuid.UUID(user_id), test_type=test_type)
    session, first_question = use_case.execute(command)

    return jsonable_encoder({"session": session, "first_question": first_question})