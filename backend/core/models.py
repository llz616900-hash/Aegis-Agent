from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class PersonaRequest(BaseModel):
    persona: str


class SceneRequest(BaseModel):
    scene: str


class SpeechResponse(BaseModel):
    text: str


class PushToggleRequest(BaseModel):
    enabled: bool


class ProactiveRequest(BaseModel):
    text: str


class DeleteMemoryRequest(BaseModel):
    memory_id: str
