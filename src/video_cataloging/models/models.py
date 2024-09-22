from typing import Any, Optional, List
import re

from pydantic import BaseModel, Field


class DabnisBaseModel(BaseModel):
    def __init__(self, /, **data: Any):
        super().__init__(**data)

    # Returns a string containing: name; type; descriptions, of fields in a derived class.
    def get_field_info(self) -> str:
        field_info = []
        for field_name, field_instance in self.model_fields.items():
            _type = self.extract_type_hint(str(field_instance.annotation))
            field_info.append( field_name + ", type " + _type + " described as: " + str(field_instance.description) + ". ")

        response = ' '.join(field_info)

        return response

    @staticmethod
    def extract_type_hint(type_hint_str) -> str:
        match = re.match(r"typing\.Optional\[(.*)\]", type_hint_str)
        if match:
            return match.group(1)
        else:
            return type_hint_str

# Schema of a 'Video' item. Derived from DabnisBseModel to give access to 'get_field_info' method above.
class Video(DabnisBaseModel):
    path: Optional[str] = Field(None, description='Path to the film/video file')
    title: Optional[str] = Field(None, description='Video title')
    valid: Optional[bool] = Field(False, description='Valid title')
    cat: Optional[str] = Field(None ,description="One of the following categories (cat) Film, BoxSet Season Episode, Misc"),
    rating: Optional[float] = Field("Unknown", description='IMDB Rating for the video/film if it exists')
    genre: Optional[str] = Field("Unknown", description='IMDB recorded genre')
    year_released: Optional[str] = Field("Unknown", description='The year of released ')
    main_actors: Optional[List[str]] = Field(None, description='3 main actors and their roles.')
    summary: Optional[str] = Field("None", description='A summary of the video')
    key_moments: Optional[List[str]] = Field(None, description='5 key moments')

    # Derived class, call parent init.
    def __init__(self, /, **data: Any):
        super().__init__(**data)
