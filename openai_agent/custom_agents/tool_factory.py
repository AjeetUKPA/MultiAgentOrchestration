from .email_agent import email_agent
from .summarizer_agent import summarizer_agent
from .translator_agent import translator_agent

email_agent.handoffs = []
translator_agent.handoffs = [email_agent]
summarizer_agent.handoffs = [translator_agent, email_agent]

handoffs = [email_agent, summarizer_agent, translator_agent]
