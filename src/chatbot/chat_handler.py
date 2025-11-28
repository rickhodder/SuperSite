class ChatHandler:
    def __init__(self, agent):
        self.agent = agent


    

    def handle_input(self, user_input):
        response = self.agent.process_input(user_input)
        return response

    def start_conversation(self):
        print("Chatbot: Hello! How can I assist you today?")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Chatbot: Goodbye!")
                break
            response = self.handle_input(user_input)
            print(f"Chatbot: {response}")