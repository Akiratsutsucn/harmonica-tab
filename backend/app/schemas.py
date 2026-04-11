"""Pydantic schemas."""
from pydantic import BaseModel


class SongBase(BaseModel):
    title: str
    artist: str = ""
    key: str = "C"
    time_signature: str = "4/4"
    bpm: int = 120


class SongOut(SongBase):
    id: int
    source: str = "manual"
    verified: bool = False
    status: str = "verified"
    difficulty: int = 1


class NoteOut(BaseModel):
    id: int
    measure: int
    position: int
    pitch: str
    duration: str
    dot: bool = False
    tie: bool = False


class SongDetail(SongOut):
    notes: list[NoteOut] = []


class MappingRequest(BaseModel):
    key: str = "C"
    tuning: str = "paddy"


# --- Admin schemas ---

class SongCreate(SongBase):
    status: str = "pending"
    source: str = "manual"


class SongUpdate(BaseModel):
    title: str | None = None
    artist: str | None = None
    key: str | None = None
    time_signature: str | None = None
    bpm: int | None = None


class NoteIn(BaseModel):
    measure: int
    position: int
    pitch: str
    duration: str = "quarter"
    dot: bool = False
    tie: bool = False


class NotesUpdate(BaseModel):
    notes: list[NoteIn]


class TaskOut(BaseModel):
    id: int
    type: str
    status: str
    params: dict = {}
    result: dict = {}
    created_at: str = ""
    updated_at: str = ""


class AIGenerateRequest(BaseModel):
    title: str
    artist: str = ""
    original_key: str = ""
    time_signature: str = "4/4"


class CrawlRequest(BaseModel):
    query: str
    source: str = "jianpu.cn"
    max_results: int = 10


class DashboardOut(BaseModel):
    total_songs: int = 0
    verified_songs: int = 0
    pending_songs: int = 0
    rejected_songs: int = 0
    total_tasks: int = 0
    running_tasks: int = 0
    source_stats: dict = {}


class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    token: str
