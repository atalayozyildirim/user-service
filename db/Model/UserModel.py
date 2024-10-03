from pydantic import BaseModel

class UserModel(BaseModel):
    username: str
    email: str
    phoneNumber: int
    profilePicture: str
    bio: str
    city: str
