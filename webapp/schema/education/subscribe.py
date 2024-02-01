from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Subscription(BaseModel):
    user_id: int = Field(..., example=1)
    course_id: int = Field(..., example=1)
    subscription_date: datetime = Field(..., example=datetime.now())

    model_config = ConfigDict(from_attributes=True)
