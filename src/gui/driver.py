from abc import ABC, abstractmethod


class GuiDriver(ABC):
    @abstractmethod
    def open(self, url: str) -> None: ...

    @abstractmethod
    def click(self, selector: str) -> None: ...

    @abstractmethod
    def fill(self, selector: str, value: str) -> None: ...

    @abstractmethod
    def get_text(self, selector: str) -> str: ...

    @abstractmethod
    def is_visible(self, selector: str) -> bool: ...

    @abstractmethod
    def screenshot(self) -> bytes: ...

    @abstractmethod
    def close(self) -> None: ...