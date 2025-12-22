from abc import ABC, abstractmethod

class Mode(ABC):
    
    def __init__(self, seed: int, source_path: str, unallowed_chars: dict) -> None:
        self.recent_description = ""
        self.source_path = source_path
        self.seed = seed
        self.unallowed_chars = unallowed_chars    



    @abstractmethod
    def generate_text(self, amount: int, allowedLen: list) -> str:
       pass 


