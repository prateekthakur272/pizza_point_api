from pydantic import BaseModel

class UserSignUp(BaseModel):
    username:str
    email:str
    password:str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            'example':{
                'username':'prateekthakur',
                'email':'prateekthakur@example.com',
                'password':'password@123',
            }
        }
        
        
class UserSignIn(BaseModel):
    
    username:str
    password:str
    
    class Config:
        
        from_attributes = True
        json_schema_extra = {
            'example':{
                'username':'prateekthakur',
                'password':'password@123',
            }
        }
        

class UserResponse(BaseModel):
    
    id: int|None = None
    username:str|None = None
    email:str|None = None
    is_staff: bool|None = None
    is_active: bool|None = None
    
    
class TokenResponse(BaseModel):
    
    access_token:str
    refresh_token:str
    type:str = 'Bearer'