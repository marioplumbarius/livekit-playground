from livekit.agents import Agent, function_tool
from livekit.agents.beta.workflows import TaskGroup

from livekit_playground.core.agents.technical_support.tasks.ticket.create import TicketCreateTask
from livekit_playground.core.agents.technical_support.tasks.ticket.exceptions import TicketNotFoundException
from livekit_playground.core.agents.technical_support.tasks.ticket.lookup import TicketLookupTask
from livekit_playground.core.agents.technical_support.tasks.ticket.note import TicketNoteTask


class SupervisorAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""
            You are a professional technical support supervisor.
            Your role is to greet customers, understand their needs, and delegate to the right specialist.

            Always maintain a friendly, professional tone. Be aware of the customer's
            complete journey through this call.
            """,
        )

    async def on_enter(self):
        await self.session.generate_reply()

    @function_tool
    async def lookup_ticket(self) -> str:
        """
        Use when the customer wants to lookup a ticket.
        """
        result = await TicketLookupTask(chat_ctx=self.chat_ctx.copy(exclude_instructions=True))
        return str(result)

    @function_tool
    async def create_ticket(self) -> str:
        """
        Use when the customer wants to create a new ticket.
        """
        result = await TicketCreateTask(chat_ctx=self.chat_ctx.copy(exclude_instructions=True))
        return str(result)

    @function_tool
    async def add_note_to_ticket(self) -> str:
        """
        Use when the customer wants to add a note to an existing ticket.
        """
        task_group = TaskGroup(chat_ctx=self.chat_ctx)
        task_group.add(lambda: TicketLookupTask(), id="find_ticket_task", description="Finds an existing ticket.")
        task_group.add(
            lambda ticket_number: TicketNoteTask(ticket_number=ticket_number),
            id="add_note_task",
            description="Adds a note to the ticket.",
        )

        try:
            await task_group
            return "The note was successfully added to the ticket."
        except TicketNotFoundException:
            return "The ticket was not found."
