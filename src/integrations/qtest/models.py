from pydantic import BaseModel, Field


class QTestAttachment(BaseModel):
    name: str
    content_type: str = "image/png"
    data: str


class QTestStepLog(BaseModel):
    order: int
    description: str
    expected_result: str
    actual_result: str
    status: str


class QTestLogPayload(BaseModel):
    name: str
    automation_content: str
    status: str
    exe_start_date: str
    exe_end_date: str
    test_step_logs: list[QTestStepLog] = Field(default_factory=list)
    attachments: list[QTestAttachment] = Field(default_factory=list)