import json
import enum

class DefinitionType(enum.Enum):
	noun = 1
	verb = 2
	adjective = 3
	adverb = 4
	pronoun = 5
	preposition = 6
	conjunction = 7
	interjection = 8
class MoodType(enum.Enum):
    indicative = 1
    subjunctive = 2
    imperative = 3
    conditional = 4
    infinitive = 5
    gerund = 6
    participle = 7
class TenseType(enum.Enum):
    present = 1
    past = 2
    future = 3
    present_perfect = 4
    past_perfect = 5
    future_perfect = 6
class OtherType(enum.Enum):
    """Additional types for custom"""
    plural = 1
    singular = 2
    masculine = 3
    feminine = 4
    neuter = 5
    
	

