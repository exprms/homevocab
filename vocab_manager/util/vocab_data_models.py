from pydantic import BaseModel, create_model
import gramma_factory

class ExampleSentence(BaseModel):
    lang_1: list[str]
    lang_2: list[str]

class VocabDataDetailed(BaseModel):
    id: int
    word: str
    language: str = "czech"
    translation: str
    type: str
    notes: str | None
    tags: list[str] | None
    grammar: Substantive | Verb | None
    examples: ExampleSentence

