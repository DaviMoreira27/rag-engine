from pydantic import BaseModel, EmailStr

class UserCreationTenantData(BaseModel):
    tenant_id: str
    name: str

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password_hash: str
    tenant: UserCreationTenantData

class UserCreationResponse(BaseModel):
    user_id: str
    email: str
    tenant_id: str
