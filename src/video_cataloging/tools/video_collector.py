import os
from typing import Type, Any, List, ClassVar

from crewai_tools import BaseTool
from pydantic import BaseModel, Field

from video_cataloging.models.models import Video

# import our class/model defs
# Define our output schema.
class VideoCollectorOutput(BaseModel):
    videos: list[Video] = Field(..., description='List of Videos')

# Collects all videos from a root_path that is assigned at initiation
class VideoCollector(BaseTool):
    name: str = "Video Collector"
    # No need to inform AI about subdirectories etc. Just needs to know that it crawls a path and returns a list of videos
    description: str = "Collects video files"

    # Let our crew know the 'shape'/schema of expected inputs & outputs, to/from this tool.
    # args_schema: Type[BaseModel] = Not Required
    return_schema: Type[BaseModel] = VideoCollectorOutput

    root_path: str = None
    video_list: List[Video] = None
    vid_extensions: ClassVar[tuple[str, ...]] = ('.mkv', '.avi', '.mp4')

    # root_path passed in when initiated.
    def __init__(self, root_path: str, video_list: List[Video]):
        super().__init__()
        self.root_path = root_path
        self.video_list = video_list

    def _run(self) -> str:
        # Implementation
        try:
            for dir_path, _, files in os.walk(self.root_path):
                for file in files:
                    if file.lower().endswith(self.vid_extensions):
                        # Remove extension: .avi, .mkv, etc
                        file_name = os.path.splitext(file)[0]
                        # Build a full filepath
                        file_path = os.path.join(dir_path, file_name)
                        # Remove the root_path from file_path (privacy)
                        file_path = file_path[len(self.root_path) + 1:]
                        vid = Video(path=file_path)
                        self.video_list.append(vid)
        except Exception as e:
           return f"{e}"

        return "OK"
