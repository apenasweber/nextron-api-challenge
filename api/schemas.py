from typing import List

from pydantic import BaseModel


class ExpressionIn(BaseModel):
    expression: str


class ExpressionOut(BaseModel):
    expression: str
    result: float


class ExpressionListOut(BaseModel):
    expressions: List[ExpressionOut]
