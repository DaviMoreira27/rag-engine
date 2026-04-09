from pydantic import BaseModel, EmailStr

class UserCreationTenantData(BaseModel):
    tenant_id: str
    name: str

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    tenant: UserCreationTenantData
