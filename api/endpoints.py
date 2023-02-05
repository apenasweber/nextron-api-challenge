from typing import List

import sys
sys.path.append('..')

from fastapi import APIRouter, Depends, HTTPException, Path

from core.authentication import get_current_user
from core.database import get_db
from api.models import Expression, ExpressionList
from api.schemas import ExpressionIn, ExpressionOut, ExpressionListOut


router = APIRouter()


@router.get("/", response_model=ExpressionListOut)
async def get_expressions(current_user=Depends(get_current_user)):
    db = await get_db()
    expressions = await db.fetch_all("SELECT * FROM expressions")
    return ExpressionListOut(
        expressions=[
            ExpressionOut(expression=e['expression'], result=e['result'])
            for e in expressions
        ]
    )


@router.post("/", response_model=ExpressionOut)
async def create_expression(
    expression_in: ExpressionIn, current_user=Depends(get_current_user)
):
    expression = expression_in.expression
    # Evaluate the expression
    try:
        result = eval(expression)
    except:
        raise HTTPException(status_code=400, detail="Invalid expression")

    db = await get_db()
    await db.execute(
        "INSERT INTO expressions (expression, result) VALUES ($1, $2)",
        expression, result
    )
    return ExpressionOut(expression=expression, result=result)


@router.delete("/{expression_id}")
async def delete_expression(expression_id: int, current_user=Depends(get_current_user)):
    db = await get_db()
    await db.execute("DELETE FROM expressions WHERE id = $1", expression_id)
    return {"message": "Expression successfully deleted"}


@router.post("/evaluate")
async def evaluate_expression(expression: str, current_user=Depends(get_current_user)):
    try:
        result = eval(expression)
    except:
        raise HTTPException(status_code=400, detail="Invalid expression")
    return {"result": result}
