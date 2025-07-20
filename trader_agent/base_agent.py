from typing import List, Optional
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate
from langchain_core.tools import BaseTool
from langchain_community.llms import Ollama
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain.memory import ConversationBufferMemory

from enum import Enum
from trader_agent.context.database_queries import ContextQueries

"""
TODO: 
    - Define Prompt Template
    - Split context generator as a tool
    - Define LLM Agent in a separate Class
    - Create LangChain in Main.
    - Package as an API that receives requests and parses agents based on that
AGENT_STRUCTURE:
    SELECT Tickers by Sector (ContextQueries.get_all_tickers)
    1. Summarizer
        1.1. Fundamental
        1.2. Quantitative
        (1.1, 1.2) => Combined (summary)
    => Produces a ticker summary based on the stats provided.
    2. Analyzer (Takes input from goals and Summary from 1.)
        2.1. Pros
            2.1.1 Fundamental
            2.1.2 Quantitative
            2.1.3 Payouts
            (2.1.1, 2.1.2, 2.1.3) => Combined (+ve analysis)
        2.2. Cons
            2.2.1 Fundamental
            2.2.2 Quantitative
            2.2.3 Payouts
            (2.2.1, 2.2.2, 2.2.3) => Combined (-ve analysis)
        => Loop, N-Times
    3. Busines Executive (Stock screener)
    => Produces a list of potential tickers with reasoning
"""

class BaseAgent:
    def __init__(
        self,
        agent_name,
        model_name: str = "llama3",
        temperature: float = 0.7,
        tools: Optional[List[BaseTool]] = None,
        verbose: bool = True,
        system_prompt: str = "You are a helpful and concise AI assistant."
    ):
        self._query = {
            "quantitative_summarizer": [
                ContextQueries.get_technical_indicators,
                ContextQueries.get_price_history
            ],
            "fundamental_summarizer": ContextQueries.get_company_finances,
            "payouts_summarizer": ContextQueries.get_payouts,
        }[agent_name]
        self._agent_name = agent_name
        """
        Initialize an AI Agent with a system prompt and memory support.

        :param model_name: Ollama model name (e.g. "llama3", "mistral", "phi3")
        :param temperature: Temperature for sampling
        :param tools: LangChain tools the agent can use
        :param verbose: Enable verbose logging
        :param system_prompt: Instructional system prompt to guide LLM behavior
        """
        self.model_name = model_name
        self.temperature = temperature
        self.tools = tools or []
        self.verbose = verbose
        self.system_prompt = system_prompt

        self.llm = self._load_llm()
        self.memory = self._setup_memory()
        self.agent = self._initialize_agent()

    def _produce_context(self, func):
        def inner(*args, **kwargs):
            dfs = func(*args, **kwargs)
            context = f"{kwargs['company_name']} has the following {self._agent_name.split('_')[0]}\n"
            for df in dfs:
                for _, row in df.iterrows():
                    context += f'\t{"; ".join([f"{col}: {row[col]}" for col in df.columns])} \n'
            return context
        return inner

    def _load_llm(self):
        """Initialize Ollama LLM"""
        return Ollama(model=self.model_name, temperature=self.temperature)

    def _setup_memory(self):
        """Setup simple conversation memory"""
        return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def _initialize_agent(self):
        """Build LangChain agent with memory and custom system prompt"""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=self.verbose,
            agent_kwargs={
                "system_message": self.system_prompt
            }
        )

    def run(self, prompt: str) -> str:
        """Send a prompt to the agent"""
        return self.agent.run(prompt)

    def reset_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
