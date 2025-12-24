
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict

class TestType(Enum):
    HUMAN = "human"
    AI = "ai"

class TestStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

@dataclass
class MBTITestSession:
    id: uuid.UUID
    user_id: uuid.UUID
    test_type: TestType
    status: TestStatus
    created_at: datetime
    questions: List[str] = field(default_factory=list)
    answers: List[Dict] = field(default_factory=list)
    current_question_index: int = 0
