"""Alert, via DM, from bot when keyword is said in monitored channels."""
from eggbot.model.chat_message import ChatMessage


class KeywordNotifi:
    """Alert, via DM, from bot on keyword mention in chat message."""

    def process_message(self, message: ChatMessage) -> bool:
        """Process chat message."""
        # TODO: Build
        return False
