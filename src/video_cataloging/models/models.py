from typing import Any, Optional, List

from pydantic import BaseModel, Field


class DabnisBaseModel(BaseModel):
    def __init__(self, /, **data: Any):
        super().__init__(**data)

    # Returns a string containing: name; type; descriptions, of fields in a derived class.
    def get_field_info(self) -> str:
        field_info = []
        for field_name, field_instance in self.model_fields.items():
            field_info.append( field_name + ", type " + str(field_instance.annotation) + " described as: " + str(field_instance.description) + ". ")

        response = ' '.join(field_info)

        return response

# Schema of a 'Video' item. Derived from DabnisBseModel to give access to 'get_field_info' method above.
class Video(DabnisBaseModel):
    path: Optional[str] = Field(None, alias='Path to the film/video file')
    title: Optional[str] = Field(None, description='Video title')
    rating: Optional[float] = Field("Unknown", description='IMDB Rating for the video/film')
    genre: Optional[str] = Field("Unknown", description=' Video/film genre')
    year_released: Optional[str] = Field("Unknown", description='The year the video/film was released ')
    main_actors: Optional[str] = Field([], description='A list of the main 3 actors in video/film')
    summary: Optional[str] = Field("None Available", description='A summary of the video')

    # Derived class, call parent init.
    def __init__(self, /, **data: Any):
        super().__init__(**data)