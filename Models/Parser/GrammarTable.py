import json
from Models.Parser.DicTable import DicTable
from Models.Parser.DefParser import DefinitionType, MoodType, TenseType, OtherType

class GrammarTable:
    def __init__(self, json_file='grammars.json'):
        self.json_file = json_file
        with open(json_file, 'r', encoding='utf-8') as f:
            self.grammar_dict = json.load(f)
        
        # 词性类型映射
        self.type_mapping = {
            'DefinitionType': DefinitionType,
            'MoodType': MoodType,
            'TenseType': TenseType,
            'OtherType': OtherType
        }
    
    def get_grammars(self, words=None, min_match=5):
        """根据一组词获取匹配的语法规则
        
        Args:
            words: 词列表
            min_match: 最小匹配词性数量（默认5）
        
        Returns:
            匹配的语法规则列表
        """
        if words is None:
            words = []
        
        # 获取每个词的词性
        word_types = self._get_words_types(words)
        
        if not word_types:
            return []
        
        matched_grammars = []
        
        # 遍历所有语法规则
        for rule_name, rule_data in self.grammar_dict.items():
            # 规则数据格式：index: [词性index1, 词性index2, ...]
            for index, type_indices in rule_data.items():
                # 转换词性索引为实际词性值
                rule_types = self._convert_type_indices(type_indices)
                
                # 计算匹配数量
                match_count = self._count_matches(word_types, rule_types)
                
                if match_count >= min_match:
                    matched_grammars.append({
                        'rule_name': rule_name,
                        'index': index,
                        'match_count': match_count,
                        'rule_types': rule_types,
                        'matched_words': self._get_matched_words(word_types, rule_types)
                    })
        
        # 按匹配数量排序
        matched_grammars.sort(key=lambda x: x['match_count'], reverse=True)
        
        return matched_grammars
    
    def _get_words_types(self, words):
        """获取一组词的词性"""
        dic_table = DicTable()
        word_types = []
        
        for word in words:
            # 从 DicTable 获取词的索引
            index = dic_table.word2index(word)
            if index:
                # 从 grammar_dict 中查找该索引对应的词性
                for rule_name, rule_data in self.grammar_dict.items():
                    if index in rule_data:
                        type_indices = rule_data[index]
                        converted_types = self._convert_type_indices(type_indices)
                        word_types.append({
                            'word': word,
                            'index': index,
                            'types': converted_types,
                            'raw_types': type_indices
                        })
                        break
        
        return word_types
    
    def _convert_type_indices(self, type_indices):
        """转换词性索引为实际的词性枚举值"""
        converted = []
        
        for type_info in type_indices:
            # type_info 格式可以是：{"type": "DefinitionType", "value": 1}
            # 或者直接是数字，需要从上下文中推断类型
            if isinstance(type_info, dict):
                type_class = type_info.get('type')
                value = type_info.get('value')
                
                if type_class and value:
                    type_enum = self.type_mapping.get(type_class)
                    if type_enum:
                        try:
                            converted.append(type_enum(value))
                        except ValueError:
                            # 如果值无效，尝试从字符串转换
                            try:
                                converted.append(type_enum[value])
                            except (KeyError, TypeError):
                                pass
            elif isinstance(type_info, int):
                # 如果是纯数字，需要根据规则推断类型
                # 这里简化处理，实际可能需要更复杂的逻辑
                converted.append(str(type_info))
            else:
                converted.append(str(type_info))
        
        return converted
    
    def _count_matches(self, word_types, rule_types):
        """计算词性和规则词性的匹配数量"""
        match_count = 0
        
        # 获取所有词的词性列表
        word_type_values = []
        for wt in word_types:
            word_type_values.extend(wt['types'])
        
        # 计算匹配
        for rule_type in rule_types:
            if rule_type in word_type_values:
                match_count += 1
        
        return match_count
    
    def _get_matched_words(self, word_types, rule_types):
        """获取匹配了哪些词"""
        matched = []
        
        for wt in word_types:
            matched_types = [t for t in wt['types'] if t in rule_types]
            if matched_types:
                matched.append({
                    'word': wt['word'],
                    'matched_types': matched_types
                })
        
        return matched
    
    def add_grammar_rule(self, rule_name, index, type_list, save=False):
        """添加语法规则
        
        Args:
            rule_name: 规则名称
            index: 索引
            type_list: 词性列表，每个元素可以是枚举值或{"type": "TypeClass", "value": value}
            save: 是否保存
        """
        if rule_name not in self.grammar_dict:
            self.grammar_dict[rule_name] = {}
        
        # 转换词性为可存储格式
        stored_types = []
        for t in type_list:
            if isinstance(t, enum.Enum):
                # 从枚举值获取类型名和值
                type_class = t.__class__.__name__
                stored_types.append({
                    'type': type_class,
                    'value': t.value
                })
            elif isinstance(t, dict):
                # 已经是正确格式
                stored_types.append(t)
            else:
                # 其他格式，直接存储
                stored_types.append(t)
        
        self.grammar_dict[rule_name][index] = stored_types
        
        if save:
            self.save()
        
        return True
    
    def get_rule_by_index(self, rule_name, index):
        """根据规则名和索引获取词性列表"""
        if rule_name in self.grammar_dict:
            if index in self.grammar_dict[rule_name]:
                type_indices = self.grammar_dict[rule_name][index]
                return self._convert_type_indices(type_indices)
        return None
    
    def get_all_rules(self):
        """获取所有规则"""
        return self.grammar_dict
    
    def find_rules_by_type(self, target_type, min_count=1):
        """根据特定词性查找包含该词性的规则
        
        Args:
            target_type: 目标词性（枚举值）
            min_count: 最小出现次数
        """
        results = []
        
        for rule_name, rule_data in self.grammar_dict.items():
            for index, type_indices in rule_data.items():
                converted = self._convert_type_indices(type_indices)
                count = converted.count(target_type)
                
                if count >= min_count:
                    results.append({
                        'rule_name': rule_name,
                        'index': index,
                        'count': count,
                        'types': converted
                    })
        
        return results
    
    def save(self):
        """保存数据到文件"""
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.grammar_dict, f, indent=4, ensure_ascii=False)
    
    def __str__(self):
        """字符串表示"""
        if not self.grammar_dict:
            return "语法表为空"
        
        result = "语法规则：\n"
        for rule_name, rule_data in self.grammar_dict.items():
            result += f"\n[ {rule_name} ]\n"
            for index, types in rule_data.items():
                converted = self._convert_type_indices(types)
                type_names = [str(t) for t in converted]
                result += f"  索引 {index}: {type_names}\n"
        
        return result