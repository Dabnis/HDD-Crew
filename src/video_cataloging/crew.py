from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

from base.llms import LLMS60
from src.video_cataloging.tools.get_next_video import GetNextVideo
from src.video_cataloging.tools.get_video_list_summary import GetListSummary
from src.video_cataloging.tools.save_collated import SaveCollated
from src.video_cataloging.tools.update_video_list import UpdateVideoList
from src.video_cataloging.tools.video_collector import VideoCollector


# Uncomment the following line to use an example of a custom tool
# from video_cataloging.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class VideoCatalogingCrew:
	"""VideoCataloging crew"""

	# Pass in the root path when we initialise the crew.
	def __init__(self, root_path: str):
		# Keep things grounded, call the base init func.
		super().__init__()
		# Reduce IDE warnings noise!
		self.tasks = None
		self.agents = None
		self.agents_config = None
		self.tasks_config = None
		# My LLM data class
		self.llms = LLMS60()
		# The root path that the crew should crawl & process video files.
		self.root_path = root_path
		# Initiate the video_list. Crew will be provided with 'tools' to read & mutate
		self.video_list = []

		# --- A set of tools to work with the video list ---
		# Pass the root_path to the video_collector tool
		self.video_collector = VideoCollector(root_path=root_path, video_list=self.video_list)
		# # Pass a reference to the video list object to the update video tool
		self.update_video_list = UpdateVideoList(video_list=self.video_list)
		# # Get the list of videos
		# self.get_video_list = GetVideoList(video_list=self.video_list)
		# # Auto incrementing Get Next video tool
		self.get_next_video = GetNextVideo(video_list=self.video_list)
		# Gets a list summary for the collator.
		self.get_list_summary = GetListSummary(video_list=self.video_list)
		# Collate Films; Box-Sets; Videos
		self.save_collated = SaveCollated()
		# # A genre grouping tool
		# self.group_videos = GroupVideos(video_list=self.video_list)

		# CrewAI tools
		self.OnlineSearchTool = SerperDevTool()

	@agent
	def film_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['film_researcher'],
			# This guy will need to be able to search the internet.
			tools=[self.OnlineSearchTool],
			llm=self.llms.GTP4oMini,
			max_iter=100,
			verbose=True
		)

	@agent
	def film_cataloger(self) -> Agent:
		return Agent(
			config=self.agents_config['film_cataloger'],
			# This guy will need read/write access to the video list.
			# tools=[ self.group_videos],
			# This guy will need to pass tasks off to other crew members.
			allow_delegation=True,
			llm=self.llms.GTP4oMini,
			max_iter=100,
			verbose=True
		)

	@agent
	def collation_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['collation_expert'],
			allow_delegation=False,
			llm=self.llms.GTP4oMini,
			tools=[self.save_collated],
			max_iter=100,
			verbose=True
		)

	# <<< Tasks >>>
	@task
	def collect_video_filenames_task(self) -> Task:
		return Task(
			config=self.tasks_config['collect_video_filenames_task'],
			tools=[self.video_collector],
		)

	@task
	def hydration_task(self) -> Task:
		return Task(
			config=self.tasks_config['hydration_task'],
			tools=[self.get_next_video, self.update_video_list],
			output_file='validated_titles.md'
		)

	@task
	def collate_video_list_task(self) -> Task:
		return Task(
			config=self.tasks_config['collate_video_list_task'],
			tools=[self.get_list_summary, self.save_collated],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the VideoCataloging crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			manager_llm=self.llms.GTP4oMini,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)