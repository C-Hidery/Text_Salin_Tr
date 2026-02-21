import Models.Parser.ActionTable
import Models.Parser.GrammarTable
import Models.Parser.DefParser
import Models.Parser.DicTable
class SalinModel:
    def __init__(self):
        self.action_table = Models.Parser.ActionTable.ActionTable()
        self.grammar_table = Models.Parser.GrammarTable.GrammarTable()
        self.dic_table = Models.Parser.DicTable.DicTable()
    