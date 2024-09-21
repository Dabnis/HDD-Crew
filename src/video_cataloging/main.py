#!/usr/bin/env python
import sys

from src.video_cataloging.crew import VideoCatalogingCrew
from src.video_cataloging.models.models import Video


# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """

    video_fields = Video().get_field_info()
    inputs = {
        'video_fields': video_fields,
    }
    VideoCatalogingCrew(root_path='/media/jonathan/SAMSUNG 2TB/VideoFiles').crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        VideoCatalogingCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        VideoCatalogingCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         VideoCatalogingCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
#
#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")


if __name__ == "__main__":
    print("## Welcome to Dabnis AI Testing##")
    run()
    # train()