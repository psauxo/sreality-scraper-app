from uuid import UUID
from pydantic import field_validator, model_validator
from pydantic import BaseModel, HttpUrl


class FlatItemModel(BaseModel):
    """
    FlatItemModel is a pydantic model that represents a flat item.
    The model has three fields:
    - uuid: unique identifier of the flat item
    - title: title of the flat listing (e.g. "2+kk, 50m²")
    - image_url: url of the flat listing's image

    The model has two validators:
    - field_validator: validates the title field
    - model_validator: validates the title and image_url fields

    The model has one method:
    - model_dump: returns a dict representation of the model (used for saving the model to the database)
    """

    id: UUID
    title: str
    image_url: HttpUrl

    class Config:
        from_attributes = True

    @field_validator("title")
    def clean_title(cls, value: str):
        return value.replace("\xa0", " ")

    @model_validator(mode="before")
    def check_title_and_image_url(cls, values):
        title = values.get("title")
        image_url = values.get("image_url")
        if not title or not image_url:
            raise ValueError("Both title and image_url must be present")
        return values

    def model_dump(self, *args, **kwargs) -> dict:
        return {"id": self.id, "title": self.title, "image_url": str(self.image_url)}
