from livekit.agents import AgentTask, ChatContext, function_tool

from livekit_playground.core.agents.technical_support.tasks.ticket.model import TicketStatus, TicketTaskResult

TicketCreateTaskResult = TicketTaskResult


class TicketCreateTask(AgentTask[TicketCreateTaskResult]):
    def __init__(self, chat_ctx: ChatContext = None) -> None:
        super().__init__(
            instructions="Create a new ticket.",
            chat_ctx=chat_ctx,
        )

    async def on_enter(self):
        await self.session.generate_reply()

    @function_tool
    async def create(self, details: str) -> None:
        """
        Call when the customer has provided their ticket details.

        Args:
            details (str): The ticket details provided by the customer.
        """
        result = TicketCreateTaskResult(details=details, number="1", status=TicketStatus.OPEN, notes=[])
        self.complete(result=result)
