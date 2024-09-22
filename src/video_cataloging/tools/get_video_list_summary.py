import json
from typing import List, Type

from crewai_tools import BaseTool
from pydantic import BaseModel

from video_cataloging.models.models import Video


# Define any pydantic input schema.
# Pydantic processes carried out with details of Video data class.
class GetListSummaryInput(BaseModel):
    def __init__(self):
        super().__init__()


# Define any pydantic output schema.

# The Tool
class GetListSummary(BaseTool):
    name: str = "Get List Summary"
    # No need to inform AI about subdirectories etc. Just needs to know that it crawls a path and returns a list of videos
    description: str = "Returns the: index; title; cat (category), for each item in the list"

    # Let our crew know the 'shape'/schema of expected inputs & outputs, to/from this tool.
    args_schema: Type[BaseModel] = GetListSummaryInput

    video_list: List[Video] = None

    # A reference/pointer to the video list that the crew is working on.
    def __init__(self, video_list: List[Video]):
        super().__init__()
        self.video_list = video_list

    def _run(self) -> str:
        # Implementation
        list_summary = ""

        try:
            for index, video in self.video_list:
                list_summary += f"index:{index}, title:{video.title}, path:{video.path}, cat:{video.cat}\n. "
        except Exception as e:
            return f"error: {e}"

        return list_summary
