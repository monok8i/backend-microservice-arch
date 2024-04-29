d = {
    "email": "123",
    "password": "1"
}

from pydantic import BaseModel, EmailStr

class test(BaseModel):
    d: EmailStr

t = test(d="admin@admin.admin")

d = t.model_dump()

if email := d.get("email"):
    if isinstance(email, EmailStr):
        print(email)
    else:
        print(False)