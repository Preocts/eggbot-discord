"""Alert, via DM, from bot when keyword is said in monitored channels."""
import dataclasses
import re
from typing import Any

from eggbot.model.chat_message import ChatMessage


@dataclasses.dataclass(frozen=True)
class KeywordNotifiConfig:
    """Represents member configuration for Keyword Notifi module."""

    member_id: str
    pattern: re.Pattern[str]
    enabled: bool
    block_list: list[str]


class KeywordNotifi:
    """Alert, via DM, from bot on keyword mention in chat message."""

    config_section = "keyword_notifi"

    def __init__(self) -> None:
        self.configs: dict[str, KeywordNotifiConfig] = {}

    # Interface
    def process_message(self, message: ChatMessage) -> bool:
        """Process chat message."""
        for config in self.configs.values():
            mention = f"<@{config.member_id}>"
            result = config.pattern.search(message.raw_message)
            if result or mention in message.raw_message:
                return True
        return False

    # Interface
    def load_config(self, config: dict[str, Any]) -> None:
        """
        Load config into class, removes existing loaded config values.

        Args:
            config: configuration mapping

        Returns:
            None
        """
        # Reset state config
        self.configs = {}

        try:
            members = config[self.config_section]
        except KeyError as err:
            raise KeyError(f"Config file missing expected key '{err}'") from err

        for member in members:
            self.configs[member["member_id"]] = KeywordNotifiConfig(
                member_id=member["member_id"],
                pattern=re.compile(rf"\b{member['pattern'].lower()}\b", re.I),
                enabled=member["enabled"],
                block_list=member["block_list"],
            )
