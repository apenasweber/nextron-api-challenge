from typing import List

from pydantic import BaseModel


class Expression(BaseModel):
    expression: str
    result: float


class ExpressionList(BaseModel):
    expressions: List[Expression]
