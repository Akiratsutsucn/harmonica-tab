"""Jianpu page parsers for various sites."""
import logging

logger = logging.getLogger(__name__)


class BaseParser:
    """Base class for jianpu site parsers."""

    def parse(self, html: str) -> list[dict]:
        raise NotImplementedError


class Tan8Parser(BaseParser):
    """Parser for tan8.com jianpu pages."""

    def parse(self, html: str) -> list[dict]:
        # Placeholder - needs real implementation with BeautifulSoup
        logger.info("Tan8 parser not yet implemented")
        return []


class JianpuCnParser(BaseParser):
    """Parser for jianpu.cn pages."""

    def parse(self, html: str) -> list[dict]:
        logger.info("JianpuCn parser not yet implemented")
        return []


PARSERS = {
    "tan8": Tan8Parser,
    "jianpu_cn": JianpuCnParser,
}


def get_parser(source: str) -> BaseParser:
    cls = PARSERS.get(source)
    if not cls:
        raise ValueError(f"Unknown source: {source}")
    return cls()
