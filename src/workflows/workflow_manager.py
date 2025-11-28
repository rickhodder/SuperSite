class WorkflowManager:
    def __init__(self):
        self.agents = []

    def register_agent(self, agent):
        self.agents.append(agent)

    def execute_workflow(self, workflow):
        for task in workflow:
            self.process_task(task)

    def process_task(self, task):
        for agent in self.agents:
            if agent.can_handle(task):
                agent.handle(task)
                break
        else:
            print(f"No agent found to handle task: {task}")