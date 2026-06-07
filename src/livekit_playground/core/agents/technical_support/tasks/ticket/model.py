from enum import StrEnum

from pydantic import BaseModel


class TicketStatus(StrEnum):
    OPEN = "open"
    RESOLVED = "resolved"


class TicketTaskResult(BaseModel):
    details: str
    notes: list[str]
    number: str
    status: TicketStatus

    def __str__(self) -> str:
        items = [
            f"Ticket Number: {self.number}",
            f"Ticket Status: {self.status}",
            f"Ticket Details: {self.details}",
        ]
        if self.notes:
            notes_as_string = "\n- ".join(self.notes)
            items.append(f"Ticket Notes: \n- {notes_as_string}")
        return "\n\n".join(items)
