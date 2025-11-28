from .BaseAgent import BaseAgent

class WorkflowAgent(BaseAgent):
    def __init__(self):
        super().__init__("Workflow Agent")
        self.workflow_steps = []

    def process_input(self, user_input):
        """Process user input and determine what workflow action to take"""
        user_input_lower = user_input.lower()
        
        if "add step" in user_input_lower:
            # Extract the step from user input
            step = user_input.replace("add step", "").strip()
            if step:
                self.add_step(step)
                return f"Added step: '{step}' to the workflow."
            else:
                return "Please specify what step to add. Example: 'add step analyze data'"
        
        elif "execute workflow" in user_input_lower or "run workflow" in user_input_lower:
            if self.workflow_steps:
                result = self.execute_workflow()
                return f"Workflow executed successfully:\n{result}"
            else:
                return "No workflow steps defined. Add some steps first!"
        
        elif "status" in user_input_lower or "workflow status" in user_input_lower:
            return self.get_workflow_status()
        
        elif "clear workflow" in user_input_lower:
            self.workflow_steps = []
            return "Workflow cleared."
        
        elif "list steps" in user_input_lower:
            return self.list_workflow_steps()
        
        elif "help" in user_input_lower or "workflow help" in user_input_lower:
            return self.show_help()
        
        else:
            return "I can help you with workflows. Type 'help' to see available commands."

    def process_task(self, task):
        """Process a specific task"""
        return self.process_step(task)

    def add_step(self, step):
        self.workflow_steps.append(step)

    def execute_workflow(self):
        results = []
        for i, step in enumerate(self.workflow_steps, 1):
            result = self.process_step(step)
            results.append(f"Step {i}: {result}")
        return "\n".join(results)

    def process_step(self, step):
        # Logic to process each step in the workflow
        return f"Processed '{step}'"

    def get_workflow_status(self):
        if not self.workflow_steps:
            return "No workflow steps currently defined."
        
        status = f"Current workflow has {len(self.workflow_steps)} steps:\n"
        for i, step in enumerate(self.workflow_steps, 1):
            status += f"  {i}. {step}\n"
        return status.strip()
    
    def list_workflow_steps(self):
        """List all workflow steps"""
        if not self.workflow_steps:
            return "No workflow steps defined."
        
        result = "Workflow Steps:\n"
        for i, step in enumerate(self.workflow_steps, 1):
            result += f"  {i}. {step}\n"
        return result.strip()
    
    def show_help(self):
        """Show available workflow commands"""
        help_text = """
Workflow Agent Commands:
- 'add step [description]' - Add a step to the workflow
- 'execute workflow' or 'run workflow' - Execute all workflow steps
- 'workflow status' or 'status' - Show current workflow status
- 'list steps' - List all workflow steps
- 'clear workflow' - Clear all workflow steps
- 'help' - Show this help message

Examples:
- add step analyze customer data
- add step generate report
- execute workflow
        """
        return help_text.strip()