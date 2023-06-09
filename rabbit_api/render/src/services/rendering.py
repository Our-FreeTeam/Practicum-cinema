import logging
from abc import ABC, abstractmethod

from jinja2 import BaseLoader, Environment
from jinja2.exceptions import TemplateSyntaxError

logger = logging.getLogger()


class TemplateRender(ABC):
    @abstractmethod
    def template_render(self, template: str, data: dict) -> str:
        """Method render template to letter.
        Args:
            template: Mesage/Letter template.
            data: Variables for template.
        Returns:
            str: Rendered message/letter.
        """
        pass


class JanjaTemplateRender(TemplateRender):

    def __init__(self) -> None:
        self.env = Environment(loader=BaseLoader)

    def template_render(self, template: str, data: dict) -> str:
        template = self.env.from_string(template)
        try:
            letter = template.render(**data)
        except TemplateSyntaxError:
            logger.exception("Template syntax error %s.", template)
        return letter
