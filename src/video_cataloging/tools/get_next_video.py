import json
from dataclasses import Field
from typing import List, Type
from pydantic import Field, BaseModel

from crewai_tools import BaseTool

from video_cataloging.models.models import Video


# Define any pydantic input schema.
# Pydantic processes carried out with details of Video data class.

# Define any pydantic output schema.
class GetNextIndexInput(BaseModel):
    list_index: int = Field(0,description="index of item in video_list")

# The Tool
class GetNextVideo(BaseTool):
    name: str = "Get Next Video"
    # No need to inform AI about subdirectories etc. Just needs to know that it crawls a path and returns a list of videos
    description: str = "Gets the next video from the list of videos"
    # The working list and present cursor index
    video_list: List[Video] = None
    cursor_idx: int = 0

    # A reference/pointer to the video list that the crew is working on.
    def __init__(self, video_list: List[Video]):
        super().__init__()
        self.video_list = video_list

    def _run(self, list_index: int) -> str:
        # Implementation
        try:
            vid = self.video_list[self.cursor_idx]
            print(f"Retrieving item at index: {self.cursor_idx}")
        except IndexError:
            # Move cursor index back to start.
            self.cursor_idx = 0
            # **REM Hopefully! we are responding to a cognitive process, 'say something',
            return "END OF VIDEO LIST."
        except Exception as e:
            return f"{e}"

        resp = {
            # Need if details are to be updated in process.
            'list_index': self.cursor_idx,
            'video_details': {
                'title': vid.title,
                'rating': vid.rating,
                'genre': vid.genre,
                'year_released': vid.year_released,
                'main_actors': vid.main_actors,
                'summary': vid.summary,

            }
        }
        # Increment index
        self.cursor_idx += 1
        print(f"Index updated to:{self.cursor_idx}]")

        return json.dumps(resp)
