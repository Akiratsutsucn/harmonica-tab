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
