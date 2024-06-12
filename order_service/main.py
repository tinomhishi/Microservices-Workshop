from fastapi import FastAPI

from routers import orders

app = FastAPI()

# include routers from orders
app.include_router(orders.router)

@app.get("/hello")
def root():
    return {"message": "Hello World!!"}
