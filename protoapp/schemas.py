from pydantic import BaseModel, Field

class ItemSchema(BaseModel):
    name: str
    color: str