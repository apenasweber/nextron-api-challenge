from typing import List

from sqlalchemy import text
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from api.database.connection import get_db
from api.models.schemas import ExpressionIn, ExpressionOut, ExpressionListOut

from api.core.settings import settings
from api.database.create_table import create_database
from api.auth.auth_bearer import JWTBearer

router = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["expressions"]
)


@router.get("/", response_model=ExpressionListOut)
async def get_expressions(db: Session = Depends(get_db)):
    try:
        results = await db.execute(text("SELECT * FROM expressions"))
        if expressions := [
        ExpressionOut(expression=e[0], result=e[1], id=e[2])
            for e in results.fetchall()
        ]:
            return ExpressionListOut(expressions=expressions)

        else:
            raise HTTPException(status_code=404, detail="No expressions found")
    except Exception as e:
        raise HTTPException(status_code=404, detail="No expressions found")




@router.post("/", response_model=ExpressionOut)
async def create_expression(
    expression_in: ExpressionIn, db: Session = Depends(get_db)):
    expression = expression_in.expression
    try:
        await create_database()
        result = eval(expression)
        await db.execute(
            text(
                f"INSERT INTO expressions (expression, result) VALUES ('{expression}', {result})"
            )
        )
        await db.commit()

        return ExpressionOut(expression=expression, result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid expression: {e}")


@router.delete("/{expression_id}")
async def delete_expression(expression_id: int, db: Session = Depends(get_db)):
    try:
        await db.execute(text(f"DELETE FROM expressions WHERE id = {expression_id}"))
        await db.commit()
        return {"message": "Expression successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Expression not found")


@router.post("/evaluate")
async def evaluate_expression(expression: str):
    try:
        result = eval(expression)
    except:
        raise HTTPException(status_code=400, detail="Invalid expression")
    return {"result": result}
