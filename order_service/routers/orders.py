from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import Order
from schemas import CreateOrder


router = APIRouter(
    prefix="/api/v1",
    tags=["Orders"]
)


@router.get("/orders")
def orders(db: Session = Depends(get_db)):
    data = db.query(Order).all()
    return data


@router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order_post:CreateOrder, db:Session = Depends(get_db)):
    new_post = Order(**order_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/orders/{id}")
def get_order(id:int, db:Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    return order


@router.delete("/orders/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id:int, db:Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == id)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    order.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Order deleted"}


@router.patch("/orders/{id}")
def update_order(id:int, updated_order:CreateOrder, db:Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == id)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    order.update(updated_order.dict(), synchronize_session=False)
    db.commit()
    return {"detail": "Order updated"}
