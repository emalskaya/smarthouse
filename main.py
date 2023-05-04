from fastapi import FastAPI
from pydantic import BaseModel, \
    validator, Field
from typing import Optional
import re


class Lamp(BaseModel):
    state: bool = False 
    color: str = "#FFFFFF"
    brightness: float = Field(default=1, ge=0, le=1)
    

class UpdatingLamp(Lamp):
    state: Optional[bool] = False 
    color: Optional[str] = "#FFFFFF"
    brightness: Optional[float] = Field(default=1, ge=0, le=1)    

    @validator('color')
    def check_color(cls, color):
        if not re.search(r'^#(?:[0-9A-F]{6})$', color):
            raise ValueError('Color should be HEX color code from #000000 to #FFFFFF')
        return color   
    
    def merge_to(self, item: Lamp) -> Lamp:
        return Lamp.parse_obj({**item.dict(), **self.dict(exclude_none=True)})


app = FastAPI()
lampItem = Lamp(state=True)

@app.get("/api/v1/lamp/state")
async def get_state():
    return lampItem

@app.post("/api/v1/lamp/update")
async def update_lamp(item: UpdatingLamp):
    global lampItem
    lampItem = item.merge_to(lampItem)

    return {"status": "success"}
