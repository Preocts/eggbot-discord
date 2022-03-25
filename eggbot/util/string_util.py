"""Common helper methods for strings."""
import re


class StringUtil:
    """Common helper methods for strings."""

    @staticmethod
    def has_match(text: str, pattern: str) -> bool:
        """Run pattern match against string and custom restrictions."""
        # TODO: Exclude particulars of regex
        # TODO: Consider pregen of all patterns to compiled expressions
        return bool(re.match(pattern, text, flags=re.I))
