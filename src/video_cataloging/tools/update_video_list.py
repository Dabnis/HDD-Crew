from typing import List, Optional

from crewai_tools import BaseTool
from pydantic import BaseModel, Field

from video_cataloging.models.models import Video

# Define any pydantic input schema.
class UpdateVideoListInput(BaseModel):
    list_index: int = Field(0, description='Index of the video in the list')
    title: str = Field(..., description='Title of the Film/video')
    valid: Optional[bool] = Field(False, description='Valid title')
    cat: Optional[str] = Field(None, description="One of the following categories (cat), Film, BoxSet Season Episode, Misc"),
    rating: Optional[float] = Field(None, description='Rating of the Film/video')
    genre: Optional[str] = Field(None, description='Genre of the Film/video')
    year_released: Optional[str] = Field(None, description='Year of the Film/video')
    main_actors: Optional[List[str]] = Field(None, description='3 main actors and their roles.')
    summary: Optional[str] = Field(None, description='Summary of the Film/video')
    key_moments: Optional[List[str]] = Field(None, description='5 key moments')



# Define any pydantic output schema.

# The Tool
class UpdateVideoList(BaseTool):
    name: str = "Update Video List"
    # No need to inform AI about subdirectories etc. Just needs to know that it crawls a path and returns a list of videos
    description: str = "Adds details about a video to the video list"

    args_schema: type[BaseModel] = UpdateVideoListInput

    video_list: List[Video] = None

    # A reference/pointer to the video list that the crew is working on.
    def __init__(self, video_list: List[Video]):
        super().__init__()
        self.video_list = video_list

    def _run(self, video_details:  UpdateVideoListInput) -> str:
    # def _run(self,list_index: int,title: str,valid: bool, cat: str, rating: float,  genre:str, year_released: str, main_actors: List[str], summary: str, key_moments: List[str]) -> str:
        # Implementation
        try:
            vid = Video(
                title=video_details.title,
                valid=video_details.valid,
                cat=video_details.cat,
                rating=video_details.rating,
                genre=video_details.genre,
                year_released=video_details.year_released,
                main_actors=video_details.main_actors,
                summary=video_details.summary,
                key_moments=video_details.key_moments
            )
            self.video_list[video_details.list_index] = vid
        except Exception as e:
            return f"{e}"

        # That worked :)
        return "OK"
