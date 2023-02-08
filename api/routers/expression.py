from typing import Dict, Optional
import ast
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.connection import get_db
from api.models.schemas import ExpressionIn, ExpressionOut, ExpressionCreate
from sqlalchemy.sql import text
from api.auth.auth_bearer import JWTBearer

from api.models.expression import Expression

import logging

router = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["expressions"]
)

logger = logging.getLogger(__name__)

@router.get("/")
def get_expressions(db: Session = Depends(get_db)):
    try:
        query = text("SELECT id, expression, result FROM expression")
        result = db.execute(query).fetchall()
        return {"expressions": [{"id": r[0], "expression": r[1], "result": r[2]} for r in result]}
    except Exception:
        raise HTTPException(status_code=404, detail="No expressions found")


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
    except Exception as info:
        raise HTTPException(status_code=400, detail=f"Error deleting expression: {info}")

@router.get("/evaluate/{expression_id}")
def evaluate_expression(expression_id: int, x: int = None, y: int = None, z: int = None, db: Session = Depends(get_db)):
    expression = db.query(Expression).filter(Expression.id == expression_id).first()
    if not expression:
        raise HTTPException(status_code=404, detail="Expression not found")
    expression = expression.expression
    try:
        if x:
            exec(f"x = {x}")
        if y:
            exec(f"y = {y}")
        if z:
            exec(f"z = {z}")
        result = bool(eval(expression.lower()))
    except Exception as info:
        logger.error(f"Invalid expression or values: {info}")
        raise HTTPException(status_code=400, detail=f"Invalid expression or values: {info}")

    return {"expression": expression, "result": result, "values": {"x": x, "y": y, "z": z}}

@router.post("/expressions", response_model=ExpressionCreate)
def create_expression(
    expression_in: ExpressionIn,
    db: Session = Depends(get_db)
):
    expression = expression_in.expression
    result = 0.0 
    try:
        result = db.execute(
            text("INSERT INTO expression (expression, result) VALUES (:expression, :result) RETURNING id"),
            {"expression": expression, "result": result}
        )
        expression_id = result.fetchone()[0]
        db.commit()
    except Exception as info:
        logger.error(f"Error inserting expression: {info}")
        raise HTTPException(status_code=500, detail=f"Error inserting expression: {info}")

    return ExpressionCreate(id=expression_id)



