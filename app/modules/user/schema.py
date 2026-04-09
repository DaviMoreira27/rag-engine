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

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    session_id: str
    user_id: str
    tenant_id: str

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    tenant_id: str

class SignupResponse(BaseModel):
    session_id: str
    user_id: str
    tenant_id: str
    email: str
    name: str
