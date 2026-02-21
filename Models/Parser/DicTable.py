import json

class DicTable:
    def __init__(self, json_file='dics.json'):
        self.json_file = json_file
        with open(json_file, 'r', encoding='utf-8') as f:
            self.dic_dict = json.load(f)
    
    def word2index(self, word):
        """根据词查找对应的索引"""
        for index, items in self.dic_dict.items():
            # 假设列表的第一个元素是词本身
            if items and items[0] == word:
                return index
        return None
    
    def index2word(self, index):
        """根据索引返回词（列表的第一个元素）"""
        index_str = str(index)
        if index_str in self.dic_dict and self.dic_dict[index_str]:
            return self.dic_dict[index_str][0]  # 返回词本身
        return None
    
    def get_definitions(self, word):
        """获取词的定义（列表中除第一个元素外的所有元素）"""
        index = self.word2index(word)
        if index is not None:
            items = self.dic_dict[index]
            if len(items) > 1:
                return items[1:]  # 返回定义列表
            return []  # 没有定义
        return None
    
    def set_a_word(self, word, index, definitions=None, save=False):
        """设置一个词，包括其索引和定义
        
        Args:
            word: 词本身
            index: 索引
            definitions: 定义列表（可选）
            save: 是否立即保存到文件
        """
        if definitions is None:
            definitions = []
        
        index_str = str(index)
        
        # 构建词条：第一个元素是词本身，后面是定义
        entry = [word] + definitions
        
        # 检查索引是否已存在
        if index_str in self.dic_dict:
            # 如果索引存在，可以选择覆盖或合并
            print(f"警告：索引 {index} 已存在，将覆盖原有内容")
        
        self.dic_dict[index_str] = entry
        
        if save:
            self.save()
    
    def add_definition(self, word, definition, save=False):
        """为指定词添加一个新的定义"""
        index = self.word2index(word)
        if index is not None:
            if definition not in self.dic_dict[index]:
                self.dic_dict[index].append(definition)
                if save:
                    self.save()
                return True
        return False
    
    def update_word(self, old_word, new_word, save=False):
        """更新词的名称（保持索引和定义不变）"""
        index = self.word2index(old_word)
        if index is not None:
            # 替换第一个元素（词本身）
            definitions = self.dic_dict[index][1:]
            self.dic_dict[index] = [new_word] + definitions
            if save:
                self.save()
            return True
        return False
    
    def remove_word(self, word, save=False):
        """删除一个词及其所有定义"""
        index = self.word2index(word)
        if index is not None:
            del self.dic_dict[index]
            if save:
                self.save()
            return True
        return False
    
    def get_all_words(self):
        """获取所有词"""
        words = []
        for items in self.dic_dict.values():
            if items:  # 确保列表不为空
                words.append(items[0])  # 只添加词本身
        return words
    
    def save(self):
        """保存数据到文件"""
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.dic_dict, f, indent=4, ensure_ascii=False)
    
    def __str__(self):
        """字符串表示"""
        result = "词表内容：\n"
        for index, items in self.dic_dict.items():
            if items:
                word = items[0]
                definitions = items[1:] if len(items) > 1 else []
                result += f"索引 {index}: {word} -> 定义: {definitions}\n"
        return result