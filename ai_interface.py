import json

from langchain import LLMChain, OpenAI, PromptTemplate  # , ConversationChain

# https://www.python-engineer.com/posts/langchain-crash-course/
# https://python.langchain.com/en/latest/modules/agents/agent_executors/examples/agent_vectorstore.html

# from langchain.agents import load_tools
from langchain.memory import ConversationBufferWindowMemory

with open("assets/files/prompts.json", "r", encoding="utf-8") as file:
    prompts = json.load(file)

with open("keys/openai_key.txt", "r", encoding="utf-8") as file:
    api_key = file.read().strip()


class AgentInterface:
    """A class which handles the interface between the application and LLM/Agent"""

    def __init__(self) -> None:
        # fmt: off
        template = prompts["system"] + """

        {history}
        Human: {human_input}
        Serenity:""".replace("        ", "")
        # fmt: on

        prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)

        self.chatgpt_chain = LLMChain(
            llm=OpenAI(temperature=0, openai_api_key=api_key, client="idk"),  # model="gpt-3.5-turbo-0301" <- Not sure where to put this
            prompt=prompt,
            # verbose=True,  # Prints stuff to chat
            verbose=False,
            memory=ConversationBufferWindowMemory(k=2),
        )
        # tools = load_tools(["wikipedia"], llm=self.chatgpt_chain)  # In the future

    def continue_chain(self, human_input: str) -> str:
        """Takes an input of text from the user and sends it to the LLMChain, returning the output as a string"""
        output = self.chatgpt_chain.predict(human_input=human_input)
        return output


if __name__ == "__main__":
    while True:
        agent = AgentInterface()
        human_input = input("Human: ")
        output = agent.continue_chain(human_input)
        print(output)
