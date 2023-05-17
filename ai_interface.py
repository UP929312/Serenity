from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.agents import load_tools
from langchain.memory import ConversationBufferWindowMemory

from prompts import prompts

with open("keys/openai_key.txt", "r") as file:
    api_key = file.read().strip()


class AgentInterface:
    def __init__(self) -> None:
        template = prompts["system"]+"""

        {history}
        Human: {human_input}
        Serenity:""".replace("        ", "")

        prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)

        self.chatgpt_chain = LLMChain(
            llm=OpenAI(temperature=0, openai_api_key=api_key),  # model="gpt-3.5-turbo-0301" <- Not sure where to put this
            prompt=prompt, 
            verbose=True, 
            memory=ConversationBufferWindowMemory(k=2),
        )
        tools = load_tools(["wikipedia"], llm=self.chatgpt_chain)

    def continue_chain(self, human_input) -> str:
        output = self.chatgpt_chain.predict(human_input=human_input)
        return output

while True:
    agent = AgentInterface()
    human_input = input("Human: ")
    output = agent.continue_chain(human_input)
    print(output)
