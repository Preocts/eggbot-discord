"""Alert, via DM, from bot when keyword is said in monitored channels."""
from __future__ import annotations

import dataclasses
import re
from typing import Any

from eggbot.model.chat_message import ChatMessage
from eggbot.model.chat_response import ChatResponse
from eggbot.module.chat_module_intf import ChatModuleIntf


@dataclasses.dataclass(frozen=True)
class KeywordNotifiConfig:
    """Represents member configuration for Keyword Notifi module."""

    member_id: str
    pattern: re.Pattern[str]
    enabled: bool
    block_list: list[str]


class KeywordNotifi(ChatModuleIntf):
    """Alert, via DM, from bot on keyword mention in chat message."""

    config_section = "keyword_notifi"

    def __init__(self) -> None:
        self.configs: dict[str, KeywordNotifiConfig] = {}

    def process_message(self, message: ChatMessage) -> ChatResponse | None:
        """Process chat message, returns response or None if no response exists"""
        for config in self.configs.values():
            mention = f"<@{config.member_id}>"
            result = config.pattern.search(message.raw_message)
            if result or mention in message.raw_message:
                return ChatResponse()
        return None

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
