from typing import List
import ast
from sqlalchemy import text, select

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.connection import get_db
from api.models.schemas import ExpressionIn, ExpressionOut, ExpressionListOut
from api.models.expression import Expression
from api.auth.auth_bearer import JWTBearer

import logging

router = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["expressions"]
)

logger = logging.getLogger(__name__)

def _evaluate_expression(expression: str) -> bool:
    try:
        parsed = ast.parse(expression, mode='eval')
        result = eval(compile(parsed, filename='<ast>', mode='eval'))
    except Exception as info:
        logger.error(f"Invalid expression: {info}")
        raise HTTPException(status_code=400, detail=f"Invalid expression: {info}")

    return result


@router.get("/", response_model=ExpressionListOut)
def get_expressions(db: Session = Depends(get_db)):
    try:
        query = text("SELECT id, expression, result FROM expression")
        results = db.execute(query).all()
        return {"expressions": [{"id": r[0], "expression": r[1], "result": r[2]} for r in results]}
    except Exception:
        raise HTTPException(status_code=404, detail="No expressions found")



@router.post("/", response_model=ExpressionOut)
def create_expression(
    expression_in: ExpressionIn, db: Session = Depends(get_db)):
    expression = expression_in.expression
    result = _evaluate_expression(expression)
    try:
        db.execute(
            text("INSERT INTO expression (expression, result) VALUES (:expression, :result)"),
            {"expression": expression, "result": result}
        )
        db.commit()
    except Exception as info:
        logger.error(f"Error inserting expression: {info}")
        raise HTTPException(status_code=500, detail=f"Error inserting expression: {info}")

    return ExpressionOut(expression=expression, result=result)


@router.delete("/{expression_id}")
def delete_expression(expression_id: int, db: Session = Depends(get_db)):
    try:
        query = text(f"SELECT id FROM expression WHERE id = {expression_id}")
        result = db.execute(query).fetchall()
        if result == []:
            raise HTTPException(status_code=404, detail="Expression not found")
        db.execute(text(f"DELETE FROM expression WHERE id = {expression_id}"))
        db.commit()
        return {"message": "Expression successfully deleted"}
    except Exception:
        raise HTTPException(status_code=400, detail="Error deleting expression")

