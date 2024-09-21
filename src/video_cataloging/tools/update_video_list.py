from typing import List, Optional

from crewai_tools import BaseTool
from pydantic import BaseModel, Field

from video_cataloging.models.models import Video

# Define any pydantic input schema.
class UpdateVideoListInput(BaseModel):
    list_index: int = Field(0, description='Index of the video in the list')
    title: str = Field(..., description='Title of the Film/video')
    rating: Optional[float] = Field(None, description='Rating of the Film/video')
    genre: Optional[str] = Field(None, description='Genre of the Film/video')
    year_released: Optional[str] = Field(None, description='Year of the Film/video')
    main_actors: Optional[List[str]] = Field(None, description='Main actors of the Film/video')
    summary: Optional[str] = Field(None, description='Summary of the Film/video')



# Define any pydantic output schema.

# The Tool
class UpdateVideoList(BaseTool):
    name: str = "Update Video List"
    # No need to inform AI about subdirectories etc. Just needs to know that it crawls a path and returns a list of videos
    description: str = "Adds details about a video to the video list"

    video_list: List[Video] = None

    # A reference/pointer to the video list that the crew is working on.
    def __init__(self, video_list: List[Video]):
        super().__init__()
        self.video_list = video_list

    def _run(self,list_index: int, title: str,rating: float, genre:str, year_released: str, main_actors: str, summary: str) -> str:
        # Implementation
        try:
            vid = Video(
                title=title,
                rating=rating,
                genre=genre,
                year_released=year_released,
                main_actors=main_actors,
                summary=summary,
            )
            self.video_list.append(vid)
        except Exception as e:
            return f"{e}"

        # That worked :)
        return "OK"
