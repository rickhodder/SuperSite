class BaseAgent:
    def __init__(self, name):
        self.name = name

    def process_task(self, task):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def process_input(self, user_input):
        """Process user input and return a response"""
        raise NotImplementedError("Subclasses should implement this method.")
    
    def get_name(self):
        return self.name