import json

class ActionTable:
    def __init__(self, json_file='actions.json'):
        self.json_file = json_file
        with open(json_file, 'r', encoding='utf-8') as f:
            self.action_dict = json.load(f)
    
    def get_actions_from_word(self, word):
        """根据词获取对应的行为列表"""
        for index, items in self.action_dict.items():
            # items[0] 是词本身，后面的都是行为
            if items and items[0] == word:
                if len(items) > 1:
                    return items[1:]  # 返回行为列表
                return []  # 有词但没有行为
        return None  # 没找到词
    
    def get_actions_from_index(self, index):
        """根据索引获取对应的词和行为"""
        index_str = str(index)
        if index_str in self.action_dict:
            items = self.action_dict[index_str]
            if items:
                word = items[0]
                actions = items[1:] if len(items) > 1 else []
                return {
                    'index': index_str,
                    'word': word,
                    'actions': actions
                }
        return None
    
    def set_an_action(self, index, word, actions=None, save=False):
        """设置一个索引对应的词和行为
        
        Args:
            index: 索引
            word: 词本身
            actions: 行为列表（可选）
            save: 是否立即保存到文件
        """
        if actions is None:
            actions = []
        
        index_str = str(index)
        
        # 构建条目：第一个元素是词，后面是行为
        entry = [word] + actions
        
        # 检查索引是否已存在
        if index_str in self.action_dict:
            print(f"警告：索引 {index} 已存在，将覆盖原有内容")
            print(f"原内容：词 '{self.action_dict[index_str][0]}'，行为 {self.action_dict[index_str][1:]}")
        
        self.action_dict[index_str] = entry
        
        if save:
            self.save()
        
        return True
    
    def add_action(self, index, action, save=False):
        """为指定索引添加一个新的行为"""
        index_str = str(index)
        if index_str in self.action_dict:
            if action not in self.action_dict[index_str][1:]:  # 检查行为是否已存在
                self.action_dict[index_str].append(action)
                if save:
                    self.save()
                return True
            else:
                print(f"行为 '{action}' 已存在")
                return False
        else:
            print(f"索引 {index} 不存在")
            return False
    
    def add_action_by_word(self, word, action, save=False):
        """根据词添加一个新的行为"""
        index = self.word2index(word)
        if index:
            return self.add_action(index, action, save)
        return False
    
    def word2index(self, word):
        """根据词查找对应的索引"""
        for index, items in self.action_dict.items():
            if items and items[0] == word:
                return index
        return None
    
    def index2word(self, index):
        """根据索引返回词"""
        index_str = str(index)
        if index_str in self.action_dict and self.action_dict[index_str]:
            return self.action_dict[index_str][0]
        return None
    
    def remove_action(self, index, action, save=False):
        """从指定索引移除一个行为"""
        index_str = str(index)
        if index_str in self.action_dict:
            items = self.action_dict[index_str]
            if action in items[1:]:  # 在行为列表中查找
                items.remove(action)
                if save:
                    self.save()
                return True
        return False
    
    def remove_word(self, index, save=False):
        """删除一个索引及其对应的词和行为"""
        index_str = str(index)
        if index_str in self.action_dict:
            del self.action_dict[index_str]
            if save:
                self.save()
            return True
        return False
    
    def update_word(self, index, new_word, save=False):
        """更新指定索引的词（保持行为不变）"""
        index_str = str(index)
        if index_str in self.action_dict:
            actions = self.action_dict[index_str][1:]  # 保留原有行为
            self.action_dict[index_str] = [new_word] + actions
            if save:
                self.save()
            return True
        return False
    
    def get_all_words(self):
        """获取所有词"""
        words = []
        for items in self.action_dict.values():
            if items:
                words.append(items[0])
        return words
    
    def get_all_indices(self):
        """获取所有索引"""
        return list(self.action_dict.keys())
    
    def save(self):
        """保存数据到文件"""
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.action_dict, f, indent=4, ensure_ascii=False)
    
    def __str__(self):
        """字符串表示"""
        if not self.action_dict:
            return "行为表为空"
        
        result = "行为表内容：\n"
        for index, items in self.action_dict.items():
            if items:
                word = items[0]
                actions = items[1:] if len(items) > 1 else []
                result += f"索引 {index}: 词 '{word}' -> 行为: {actions}\n"
        return result
    
    def __len__(self):
        """返回条目数量"""
        return len(self.action_dict)