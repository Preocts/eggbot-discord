"""Interface ABS for all chat-based modules"""
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from eggbot.model.chat_message import ChatMessage
from eggbot.model.chat_response import ChatResponse


class ChatModuleIntf(ABC):
    """ABC for all chat modules"""

    @abstractmethod
    def process_message(self, message: ChatMessage) -> ChatResponse | None:
        """
        Process a ChatMessage object

        Must be overwritten with desired implementation. ABC must
        return a ChatResponse object or None to indicate to the
        controller if further action are to be taken.
        """
        raise NotImplementedError()

    @abstractmethod
    def load_config(self, config: dict[str, Any]) -> None:
        """
        Load config into class, replaces all existing loaded values

        Must be overwritten with desired implementation. If module
        does not implement a configuration then this method must
        handle an empty dict being passed in.
        """
        raise NotImplementedError()
