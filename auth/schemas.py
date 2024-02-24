from pydantic import BaseModel

class UserSignUp(BaseModel):
    id: int|None = None
    username:str
    email:str
    password:str
    is_staff: bool|None = None
    is_active: bool|None = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            'example':{
                'username':'prateekthakur',
                'email':'prateekthakur@example.com',
                'password':'password@123',
                'is_staff':False,
                'is_active':True,
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
    username:str
    email:str
    is_staff: bool|None = None
    is_active: bool|None = None
    
    
class TokenResponse(BaseModel):
    
    access_token:str
    refresh_token:str