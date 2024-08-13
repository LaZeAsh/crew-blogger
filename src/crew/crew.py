from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, llm
from langchain_cohere import ChatCohere
import os
# Uncomment the following line to use an example of a custom tool
from crew.tools.research_link import ResearchLink 
from crew.tools.upload_medium import UploadMedium 
from crew.tools.write_blog import WriteBlog 

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class CrewCrew():
	"""Crew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def summarizer(self) -> Agent:
		return Agent(
			config=self.agents_config['summarizer'],
			tools=[ResearchLink()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			# llm=self.cohere_llm(),
			max_iter=4
		)

	@agent
	def blogger(self) -> Agent:
		return Agent(
			config=self.agents_config['blogger'],
			tools=[WriteBlog()],
			verbose=True,
			# llm=self.cohere_llm(),
			max_iter=4
		)

	@agent
	def medium_upload(self) -> Agent:
		return Agent(
			config=self.agents_config['medium_upload'],
			tools=[UploadMedium()],
			verbose=True,
			# llm=self.cohere_llm(),
			max_iter=4
		)
	"""
	Use langchain_cohere
	"""
	# @llm
	# def cohere_llm(self):
	# 	llm = ChatCohere(cohere_api_key=os.environ['COHERE'])
	# 	return llm

	@task
	def research_link(self) -> Task:
		return Task(
			config=self.tasks_config['research_link'],
			agent=self.summarizer()
		)
	
	@task
	def write_blog(self) -> Task:
		return Task(
			config=self.tasks_config['write_blog'],
			agent=self.blogger(),
			output_file='blog.txt'
		)
	
	@task
	def upload_medium(self) -> Task:
		return Task(
			config=self.tasks_config['upload_medium'],
			agent=self.medium_upload(),
			output_file='test.txt'

		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Crew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)