import typing
from typing import Dict, Text, List, Any, Type

from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.message import Message
import MeCab
import unidic_lite



@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER, is_trainable=False
)
class MecabTokenizer(Tokenizer):
    """Tokenizer that uses Mecab."""

    @classmethod
    def required_components(cls) -> List[Type]:
        """Components that should be included in the pipeline before this component."""
        return []

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """The component's default config (see parent class for full docstring)."""
        return {
            # Flag to check whether to split intents
            "intent_tokenization_flag": False,
            # Symbol on which intent should be split
            "intent_split_symbol": "_",
            # Regular expression to detect tokens
            "token_pattern": None,
            # Symbol on which prefix should be split
            "prefix_separator_symbol": None,
        }

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        """Tokenizes the text of the provided attribute of the incoming message."""
       
        mecab = MeCab.Tagger(f'-r nul -d {unidic_lite.DICDIR}')
        text = message.get(attribute)
        if not text:
            return []

        words = mecab.parse(text).split()
        tokens = [
            Token(word, idx)
            for idx, word in enumerate(words)
            if word and word.strip()
        ]

        return self._apply_token_pattern(tokens)
