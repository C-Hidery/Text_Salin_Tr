import json
from Models.Parser.DicTable import DicTable
class GrammarTable:
    def __init__(self, json2gram_json = 'grammars.json'):
        with open(json2gram_json, 'r') as f:
            self.grammar_dict = json.load(f)
    def get_grammars(self, words = []):
        grammers = []
        Dic = DicTable()
        