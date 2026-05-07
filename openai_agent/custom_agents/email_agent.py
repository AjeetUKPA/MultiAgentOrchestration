from smtplib import SMTP
from email.mime.text import MIMEText

from agents import Agent, Runner, function_tool

from core.exception import EmailSendException
from schemas import EmailAgentOutput
from core.prompts.email_agent_prompt import EMAIL_AGENT_DESCRIPTION_AS_TOOL


class EmailAgent(Agent):
    def __init__(
            self,
            sender_email: str,
            name: str,
            instructions: str,
            *args,
            **kwargs
        ):
        self.sender = sender_email
        self.description = EMAIL_AGENT_DESCRIPTION_AS_TOOL

        sender = sender_email

        # @function_tool
        # async def send_mail(receiver_email: str, subject: str, body: str) -> dict:
        #     """Send an email to receiver_email with the given subject and body."""
        #     email_content = MIMEText(body)
        #     email_content["subject"] = subject
        #     email_content["to"] = receiver_email
        #     email_content["from"] = sender
        #     try:
        #         with SMTP(host="smtp.gmail.com", port=587) as smtp:
        #             smtp.starttls()
        #             smtp.login(sender, "app_password_goes_here")
        #             smtp.send_message(email_content)
        #         return {"status": "success"}
        #     except Exception as e:
        #         raise EmailSendException(
        #             f"failed to send email to {receiver_email}: {e}"
        #         ) from e

        super().__init__(
            name=name,
            instructions=instructions,
            # tools=[send_mail],
            *args,
            **kwargs
        )

    async def run_agent(self, receiver_email: str | None, user_input: str):
        print("calling email agent")
        result = await Runner.run(self, input=user_input)
        return result.final_output


email_agent = EmailAgent(
    sender_email="ukpaajeet@gmail.com",
    name="EmailSenderAgent",
    instructions="Please draft a demo mail for testing using the topic given by the user",
    output_type=EmailAgentOutput,
)
