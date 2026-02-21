import json

class DicTable:
    def __init__(self, json_file='dics.json'):
        self.json_file = json_file
        with open(json_file, 'r') as f:
            self.dic_dict = json.load(f)
    
    def word2index(self, word):
        """返回词对应的索引（假设一个词只对应一个索引）"""
        for index, words in self.dic_dict.items():
            if word in words:
                return index
        return None
    
    def index2word(self, index):
        """返回索引对应的所有词"""
        index_str = str(index)  # 确保索引是字符串
        if index_str in self.dic_dict:
            return self.dic_dict[index_str]
        return None
    
    def get_definitions(self, word):
        """获取词的定义（这里返回该词所在索引的所有词作为定义）"""
        index = self.word2index(word)
        if index is not None:
            # 返回该索引对应的所有词
            return self.dic_dict[index]
        return None
    
    def set_a_word(self, word, index, defs=None, save=False):
        """添加或更新一个词"""
        if defs is None:
            defs = []
        
        index_str = str(index)
        
        if index_str in self.dic_dict:
            if word not in self.dic_dict[index_str]:
                self.dic_dict[index_str].append(word)
            # 添加新的定义词
            for d in defs:
                if d not in self.dic_dict[index_str]:
                    self.dic_dict[index_str].append(d)
        else:
            # 创建新索引，包含词和定义
            self.dic_dict[index_str] = [word] + defs
        
        if save:
            with open(self.json_file, 'w') as f:
                json.dump(self.dic_dict, f, indent=4)
    
    def get_all_words(self):
        """获取所有词"""
        all_words = []
        for words in self.dic_dict.values():
            all_words.extend(words)
        return all_words
    
    def remove_word(self, word, save=False):
        """从所有索引中移除一个词"""
        removed = False
        for index, words in self.dic_dict.items():
            if word in words:
                words.remove(word)
                removed = True
                # 如果索引为空，可以选择删除该索引
                if not words:
                    del self.dic_dict[index]
        
        if removed and save:
            with open(self.json_file, 'w') as f:
                json.dump(self.dic_dict, f, indent=4)
        
        return removed