import json
class ActionTable:
    def __init__(self, json2act_json = 'actions.json'):
        with open(json2act_json, 'r') as f:
            self.action_dict = json.load(f)
    def get_actions_from_word(self, action_name):
        words = []
        for key in self.action_dict.keys():
            if action_name in key:
                words += self.action_dict[key]
        return words
    def set_an_action(self, word, action_name, save = False):
        if action_name in self.action_dict.keys():
            self.action_dict[action_name].append(word)
        else:
            self.action_dict[action_name] = [word]
        if save:
            with open('actions.json', 'w') as f:
                json.dump(self.action_dict, f, indent=4)
