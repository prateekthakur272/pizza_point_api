from pydantic import BaseModel


class OrderModel(BaseModel):
    id:int|None = None
    quantity:int
    order_status:str|None = 'PENDING'
    pizza_size:str|None = 'SMALL'
    user_id:int|None = None
    
    
    class Config:
        
        from_attributes = True
        json_schema_extra = {
            'example':{
                'quantity':2,
                'piza_size':'LARGE'
            }
        }