from .chat_handler import ChatHandler
from agents.WorkflowAgent import WorkflowAgent
from agents.PolicyAgent import PolicyAgent
from agents.SuperFundSiteAgent import SuperFundSiteAgent
from agents.AddressScoringAgent import AddressScoringAgent
from agents.ReportingAgent import ReportingAgent
from agents.PolicyProcessingAgent import PolicyProcessingAgent

class ConsoleInterface:
    def __init__(self):
        # Initialize available agents
        self.workflow_agent = WorkflowAgent()
        self.policy_agent = PolicyAgent()
        self.superfundsite_agent = SuperFundSiteAgent()
        self.address_scoring_agent = AddressScoringAgent()
        self.reporting_agent = ReportingAgent()
        self.policy_processing_agent = PolicyProcessingAgent()
        self.current_agent = None
        self.chat_handler = None
        self.welcome_message()

    def welcome_message(self):
        print("Welcome to the Agentic Workflow Chatbot!")
        print("Available agents:")
        print("  1. Workflow Agent - Manage workflows and tasks")
        print("  2. Policy Agent - Retrieve and search policy information")
        print("  3. SuperFund Site Agent - Retrieve and search superfund site information")
        print("  4. Address Scoring Agent - Evaluate address safety based on nearby superfund sites")
        print("  5. Reporting Agent - Generate formatted reports from location scoring results")
        print("  6. Policy Processing Agent - Process policies and evaluate location safety")
        print("\nType 'switch agent [1|2|3|4|5|6]' to change agents")
        print("Type 'help' for agent-specific commands")
        print("Type 'exit' to quit the chatbot.")
        print("-" * 60)

    def get_user_input(self):
        agent_name = self.current_agent.get_name() if self.current_agent else "No Agent"
        return input(f"[{agent_name}] You: ")

    def display_message(self, message):
        print(f"Agent: {message}")

    def switch_agent(self, agent_number):
        """Switch to a different agent"""
        if agent_number == "1":
            self.current_agent = self.workflow_agent
            self.chat_handler = ChatHandler(self.current_agent)
            return f"Switched to {self.current_agent.get_name()}"
        elif agent_number == "2":
            self.current_agent = self.policy_agent
            self.chat_handler = ChatHandler(self.current_agent)
            return f"Switched to {self.current_agent.get_name()}"
        elif agent_number == "3":
            self.current_agent = self.superfundsite_agent
            self.chat_handler = ChatHandler(self.current_agent)
            return f"Switched to {self.current_agent.get_name()}"
        elif agent_number == "4":
            self.current_agent = self.address_scoring_agent
            self.chat_handler = ChatHandler(self.current_agent)
            return f"Switched to {self.current_agent.get_name()}"
        elif agent_number == "5":
            self.current_agent = self.reporting_agent
            self.chat_handler = ChatHandler(self.current_agent)
            return f"Switched to {self.current_agent.get_name()}"
        elif agent_number == "6":
            self.current_agent = self.policy_processing_agent
            self.chat_handler = ChatHandler(self.current_agent)
            return f"Switched to {self.current_agent.get_name()}"
        else:
            return "Invalid agent number. Use 1 for Workflow Agent, 2 for Policy Agent, 3 for SuperFund Site Agent, 4 for Address Scoring Agent, 5 for Reporting Agent, or 6 for Policy Processing Agent."

    def run(self):
        while True:
            user_input = self.get_user_input().strip()
            
            if user_input.lower() == 'exit':
                print("Exiting the chatbot. Goodbye!")
                break
            
            if not user_input:
                continue
            
            if user_input.lower().startswith('switch agent'):
                parts = user_input.split()
                if len(parts) >= 3:
                    response = self.switch_agent(parts[2])
                    self.display_message(response)
                else:
                    self.display_message("Please specify agent number. Example: 'switch agent 1', 'switch agent 2', 'switch agent 3', 'switch agent 4', 'switch agent 5', or 'switch agent 6'")
            
            elif user_input.lower() == 'help' and not self.current_agent:
                self.display_message("Please select an agent first using 'switch agent [1|2|3|4|5|6]'")
            
            elif self.current_agent and self.chat_handler:
                # Process input through the current agent
                response = self.chat_handler.handle_input(user_input)
                self.display_message(response)
            
            else:
                self.display_message("Please select an agent first using 'switch agent [1|2|3|4|5|6]'")