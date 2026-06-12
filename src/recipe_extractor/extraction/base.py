from abc import ABC, abstractmethod

from recipe_extractor.data.schemas import RecipeData

class RecipeExtractor(ABC):

    @abstractmethod
    def extract(
        self,
        html: str,
        url: str,
    ) -> RecipeData:
        ...