from typing import Any, List

from pydantic import BaseModel


class ExpressionIn(BaseModel):
    expression: str


class ExpressionOut(BaseModel):
    id = int
    expression: str
    result: Any


class ExpressionListOut(BaseModel):
    expressions: List[ExpressionOut]
