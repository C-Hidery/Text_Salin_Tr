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

    @staticmethod
    def from_string(s):
        for member in DefinitionType:
            if member.name == s:
                return member
        raise ValueError(f"Invalid DefinitionType: {s}")
    def from_value(value): 
        for member in DefinitionType:
            if member.value == value:
                return member
        raise ValueError(f"Invalid DefinitionType value: {value}")

class MoodType(enum.Enum):
    indicative = 1
    subjunctive = 2
    imperative = 3
    conditional = 4
    infinitive = 5
    gerund = 6
    participle = 7

    @staticmethod
    def from_string(s):
        for member in MoodType:
            if member.name == s:
                return member
        raise ValueError(f"Invalid MoodType: {s}")
    def from_value(value):
        for member in MoodType:
            if member.value == value:
                return member
        raise ValueError(f"Invalid MoodType value: {value}")
class TenseType(enum.Enum):
    present = 1
    past = 2
    future = 3
    present_perfect = 4
    past_perfect = 5
    future_perfect = 6

    @staticmethod
    def from_string(s):
        for member in TenseType:
            if member.name == s:
                return member
        raise ValueError(f"Invalid TenseType: {s}")
    def from_value(value):
        for member in TenseType:
            if member.value == value:
                return member
        raise ValueError(f"Invalid TenseType value: {value}")
class OtherType(enum.Enum):
    """Additional types for custom"""
    plural = 1
    singular = 2
    masculine = 3
    feminine = 4
    neuter = 5
    happiness = 6
    sadness = 7
    anger = 8
    fear = 9
    surprise = 10
    disgust = 11
    trust = 12
    anticipation = 13
    joy = 14
    love = 15
    hate = 16
    confidence = 17
    doubt = 18
    excitement = 19
    boredom = 20
    calm = 21
    anxiety = 22
    relaxation = 23
    curiosity = 24
    confusion = 25
    clarity = 26
    creativity = 27
    logic = 28
    intuition = 29
    reason = 30
    emotion = 31
    physical = 32
    mental = 33
    social = 34
    cultural = 35
    historical = 36
    scientific = 37
    artistic = 38
    philosophical = 39
    religious = 40
    political = 41
    economic = 42
    environmental = 43
    technological = 44
    ethical = 45

    @staticmethod
    def from_string(s):
        for member in OtherType:
            if member.name == s:
                return member
        raise ValueError(f"Invalid OtherType: {s}")
    def from_value(value):
        for member in OtherType:
            if member.value == value:
                return member
        raise ValueError(f"Invalid OtherType value: {value}")

	

