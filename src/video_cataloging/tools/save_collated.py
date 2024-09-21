import json
from dataclasses import Field, dataclass
from typing import List, Type, Any
from pydantic import Field, BaseModel

from crewai_tools import BaseTool
from sympy.plotting.intervalmath import interval

from video_cataloging.models.models import Video


# Define any pydantic input schema.
# Pydantic processes carried out with details of Video data class.
@dataclass
class Season(BaseModel):
    number: str = Field("01", description="The number of the season")
    episodes: List[int] = Field(..., description="The video list index of the episode of the season collection")

# Define any pydantic output schema.
@dataclass
class BoxSet(BaseModel):
    name: str = Field(..., description="The name of the box set")
    seasons: List[Season] = Field(..., description="A list of seasons of a BoxSet")

class SaveCollatedInput(BaseModel):
    films: List[int] = Field(..., description="A list of film indexes in the video list")
    box_sets: List[BoxSet] = Field(..., description="A list of named box sets")
    videos: List[int] = Field([],description="A list of video list indexes of files classified as 'video'")

    # Derived class, call parent init.
    def __init__(self, /, **data: Any):
        super().__init__(**data)

# The Tool
class SaveCollated(BaseTool):
    name: str = "Save Collated"
    # No need to inform AI about subdirectories etc. Just needs to know that it crawls a path and returns a list of videos
    description: str = "Saves a collated structured list of grouped video list indexes"
    # The working list and present cursor index
    collated_list: Any = None
    cursor_idx: int = 0

    args_schema: Type[BaseModel] = SaveCollatedInput

    # A reference/pointer to the video list that the crew is working on.
    def __init__(self):
        super().__init__()
        self.args_schema = SaveCollatedInput

    def _run(self, films: List[int], videos: List[int], box_sets: List[BoxSet]) -> str:
        self.collated_list = {
            films: films,
            videos: videos,
            box_sets: box_sets
        }

        resp = ""
        try:
            resp = json.dumps(self.collated_list)
        except Exception as e:
            return f"{e}"

        return resp
