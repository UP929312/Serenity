from langchain import OpenAI, LLMChain, PromptTemplate  # , ConversationChain

# from langchain.agents import load_tools
from langchain.memory import ConversationBufferWindowMemory

import json

with open("assets/files/prompts.json", "r") as file:
    prompts = json.load(file)

with open("keys/openai_key.txt", "r") as file:
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
            verbose=True,
            memory=ConversationBufferWindowMemory(k=2),
        )
        # tools = load_tools(["wikipedia"], llm=self.chatgpt_chain)  # In the future

    def continue_chain(self, human_input: str) -> str:
        output = self.chatgpt_chain.predict(human_input=human_input)
        if "As an AI language model" in output:
            print("Nooooooo, we need to account for thissssss")  # TODO: Account for this
        return output


if __name__ == "__main__":
    while True:
        agent = AgentInterface()
        human_input = input("Human: ")
        output = agent.continue_chain(human_input)
        print(output)
