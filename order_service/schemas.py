from pydantic import BaseModel

class OrderBase(BaseModel):
    customer_id: int
    customer_name: str
    address: str
    

class CreateOrder(OrderBase):
    product_id: int
    quantity: int
    customer_id: int
    customer_name: str
    address: str
    
    class Config:
        orm_mode = True
        
    # validate that customer_id, customer_name and address are not empty
    @classmethod
    def validate_customer_id(cls, v):
        if not v:
            raise ValueError('customer_id cannot be empty')
        return v
    
    @classmethod
    def validate_customer_name(cls, v):
        if not v:
            raise ValueError('customer_name cannot be empty')
        return v
    
    @classmethod
    def validate_address(cls, v):
        if not v:
            raise ValueError('address cannot be empty')
        return v