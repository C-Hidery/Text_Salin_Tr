import json
class DicTable:
    def __init__(self, json2dic_json = 'dics.json'):
        with open(json2dic_json, 'r') as f:
            self.dic_dict = json.load(f)
    def word2index(self, word):
        for key in self.dic_dict.keys():
            if word in self.dic_dict[key]:
                return key
        return None
    def index2word(self, index):
        if index in self.dic_dict.keys():
            return self.dic_dict[index]
        return None
    def get_definitions(self, word):
        index = self.word2index(word)
        defs = []
        if index is not None:
            for key in self.dic_dict.keys():
                if index in self.dic_dict[key]:
                    defs += self.dic_dict[key]
            return defs
        return None
    def set_a_word(self, word, index, defs = [], save = False):
        if index in self.dic_dict.keys():
            self.dic_dict[index].append(word)
            self.dic_dict[index] += defs
        else:
            self.dic_dict[index] = [word] + defs
        if save:
            with open('dics.json', 'w') as f:
                json.dump(self.dic_dict, f, indent=4)