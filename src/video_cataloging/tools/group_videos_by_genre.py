from typing import List

from crewai_tools import BaseTool

from video_cataloging.models.models import Video


# Define any pydantic input schema.
# Pydantic processes carried out with details of Video data class.

# Define any pydantic output schema.

# The Tool
class GroupVideosByGenre(BaseTool):
    name: str = "Group Videos."
    # No need to inform AI about subdirectories etc. Just needs to know that it crawls a path and returns a list of videos
    description: str = "Groups a list of videos by genre"

    # Let our crew know the 'shape'/schema of expected inputs & outputs, to/from this tool.
    # args_schema: Type[BaseModel] = Not Required

    video_list: List[Video] = None
    cursor_idx: int = 0

    # A reference/pointer to the video list that the crew is working on.
    def __init__(self, video_list: List[Video]):
        super().__init__()
        self.video_list = video_list

    def _run(self) -> str:
        # Implementation
        groups = {}
        for v in self.video_list:
            field_value = getattr(v, 'genre')
            if field_value not in groups:
                groups[field_value] = []
            groups[field_value].append(v)

        return "OK"
