from typing import Any, List

from pydantic import BaseModel


class ExpressionIn(BaseModel):
    expression: str


class ExpressionOut(BaseModel):
    expression: str
    result: Any
    id = int


class ExpressionListOut(BaseModel):
    expressions: List[ExpressionOut]
