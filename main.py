import re
from tkinter import *
from tkinter import messagebox

lineIndex = 0
i = 0
List = []
myTokens = []

class PythonGUIForLexer:

    def cutOneLineTokens(self, line):
        global lineIndex
        global i

        string = self.sourceInputBox.get('1.0', 'end').split('\n')
        List.append(string[i])
        print(List)

        for line in List:
            l = len(line)
            result = l

            while result > 0:

                keyword = re.match(r'(^if|^else|^int|^float)', line)
                identifier = re.match(r'^[A-Z]+[0-9]+|^[a-z]+[0-9]+', line)
                operator = re.match(r'^(=|\*|>|\+)', line)
                separators = re.match(r'^(\(|\)|\:|\"|\;)', line)
                int_literal = re.match(r'^\d+', line)
                float_literal = re.match(r'^\d+\.\d+', line)
                string_literal = re.match(r'[A-Z\s]+[a-z\s]+|[a-z\s]+', line)
                space = re.match(r'\s+', line)
                
                if space is not None:
                    line = line[space.end():]
                    result = len(line)

                elif keyword is not None:
                    self.lexicalAnalyzerBox.insert('end', "<keyword," + keyword.group(0) + ">" + '\n')
                    myTokens.append("keyword")
                    myTokens.append(keyword.group(0))
                    line = line[keyword.end():]
                    result = len(line)

                elif identifier is not None:
                    self.lexicalAnalyzerBox.insert('end', "<identifier," + identifier.group(0) + ">" + '\n')
                    myTokens.append("identifier")
                    myTokens.append(identifier.group(0))
                    line = line[identifier.end():]
                    result = len(line)

                elif operator is not None:
                    self.lexicalAnalyzerBox.insert('end', "<operator," + operator.group(0) + ">" + '\n')
                    line = line[operator.end():]
                    myTokens.append("operator")
                    myTokens.append(operator.group(0))
                    result = len(line)

                elif separators is not None:
                    self.lexicalAnalyzerBox.insert('end', "<seperator," + separators.group(0) + ">" + '\n')
                    line = line[separators.end():]
                    myTokens.append("seperator")
                    myTokens.append(separators.group(0))
                    result = len(line)

                elif float_literal is not None:
                    self.lexicalAnalyzerBox.insert('end', "<float_lit," + float_literal.group(0) + ">" + '\n')
                    line = line[float_literal.end():]
                    myTokens.append("float_lit")
                    myTokens.append(float_literal.group(0))
                    result = len(line)

                elif int_literal is not None:
                    self.lexicalAnalyzerBox.insert('end', "<int_lit," + int_literal.group(0) + ">" + '\n')
                    line = line[int_literal.end():]
                    myTokens.append("int_lit")
                    myTokens.append(int_literal.group(0))
                    result = len(line)

                elif string_literal is not None:
                    self.lexicalAnalyzerBox.insert('end', "<string_lit," + string_literal.group(0) + ">" + '\n')
                    line = line[string_literal.end():]
                    myTokens.append("string_lit")
                    myTokens.append(string_literal.group(0))
                    result = len(line)

            self.parser()
            List.pop(0)
            break

        self.currProcessLine.configure(state="normal")
        self.currProcessLine.delete(0, 'end')
        self.currProcessLine.insert(INSERT, lineIndex + 1)
        lineIndex += 1
        i += 1
        self.currProcessLine.configure(state="disabled")

    def nextLine(self):
        text = self.sourceInputBox.get('1.0', 'end-1c').split('\n')
        if self.currLineIndex.get() >= len(text):
            messagebox.showerror("ERROR", "There are no more lines to show.")
            self.currLineIndex.set(self.currLineIndex.get() - 1)
        else:
            element = text[self.currLineIndex.get()]
            self.currLineIndex.set(self.currLineIndex.get() + 1)
            self.lexicalAnalyzerBox.insert('end', self.cutOneLineTokens(element))

    def quit(self):
        self.master.quit()

    def accept_token(self):
        self.parseTreeInputBox.insert('end', "     accept token from the list: " + myTokens[1] + '\n')
        myTokens.pop(0)
        myTokens.pop(0)

    def multi(self):
        self.parseTreeInputBox.insert('end', "\n----parent node multi, finding children nodes:" + '\n')

        if myTokens[0] == "float_lit":
            self.parseTreeInputBox.insert('end', "child node (internal): float" + '\n')
            self.parseTreeInputBox.insert('end', "   float has child node (token): " + myTokens[1] + '\n')
            self.accept_token()
        elif myTokens[0] == "int_lit":
            self.parseTreeInputBox.insert('end', "child node (internal): int" + '\n')
            self.parseTreeInputBox.insert('end', "   int has child node (token): " + myTokens[1] + '\n')
            self.accept_token()

            if myTokens[1] == "*":
                self.parseTreeInputBox.insert('end', "child node (token): " + myTokens[1] + '\n')
                self.accept_token()
                self.multi()

    def math(self):
        self.parseTreeInputBox.insert('end', "\n----parent node math, finding children nodes:" + '\n')

        self.multi()
        if myTokens[1] == "+":
            self.parseTreeInputBox.insert('end', "child node (internal): +" + '\n')
            self.accept_token()

            self.multi()

    def if_exp(self):
        self.parseTreeInputBox.insert('end', "\n----parent node if exp, finding children nodes:" + '\n')

        if myTokens[1] == "if":
            self.parseTreeInputBox.insert('end', "child node (token): " + myTokens[1] + '\n')
            self.accept_token()
        if myTokens[1] == "(":
            self.parseTreeInputBox.insert('end', "child node (token): " + myTokens[1] + '\n')
            self.accept_token()
            self.parseTreeInputBox.insert('end', "Child node (internal): comparisons_exp" + '\n')
            self.comparison_exp()
        if myTokens[1] == ")":
            self.parseTreeInputBox.insert('end', "child node (token): " + myTokens[1] + '\n')
            self.accept_token()

        if myTokens[0] == "string_lit":
            self.parseTreeInputBox.insert('end', "child node (token): " + myTokens[1] + '\n')
            self.accept_token()

            if myTokens[1] == "(":
                self.parseTreeInputBox.insert('end', "child node (token): " + myTokens[1] + '\n')
                self.accept_token()
            if myTokens[0] == "sep":
                self.parseTreeInputBox.insert('end', "child node (token): " + myTokens[1] + '\n')
                self.accept_token()
            self.if_exp()

    def comparison_exp(self):

        self.parseTreeInputBox.insert('end', "\n----parent node if comparisons exp, finding children nodes:" + '\n')
        if myTokens[0] == "identifier":
            self.parseTreeInputBox.insert('end', "child node (internal): identifer" + '\n')
            self.parseTreeInputBox.insert('end', "   identifer has child node (token): " + myTokens[1] + '\n')
            self.accept_token()

        if myTokens[1] == ">":
            self.parseTreeInputBox.insert('end', "child node (token): " + myTokens[1] + '\n')
            self.accept_token()

        if myTokens[0] == "identifier":
            self.parseTreeInputBox.insert('end', "child node (internal): identifer" + '\n')
            self.parseTreeInputBox.insert('end', "   identifer has child node (token): " + myTokens[1] + '\n')
            self.accept_token()

    def exp(self):
        self.parseTreeInputBox.insert('end', "\n----parent node exp, finding children nodes:" + '\n')

        if myTokens[0] == "keyword":
            self.parseTreeInputBox.insert('end', "child node (internal): keyword" + '\n')
            self.parseTreeInputBox.insert('end', "   keyword has child node (token): " + myTokens[1] + '\n')
            self.accept_token()
        else:
            self.parseTreeInputBox.insert('end', "expect keyword as the first element of the expression!\n" + '\n')
            return

        if myTokens[0] == "identifier":
            self.parseTreeInputBox.insert('end', "child node (internal): identifer" + '\n')
            self.parseTreeInputBox.insert('end', "   identifer has child node (token): " + myTokens[1] + '\n')
            self.accept_token()
        else:
            self.parseTreeInputBox.insert('end', "expect id as the second element of the expression!" + '\n')
            return

        if myTokens[1] == "=":
            self.parseTreeInputBox.insert('end', "child node (token): " + myTokens[1] + '\n')
            self.accept_token()
        else:
            self.parseTreeInputBox.insert('end', "expect = as the third element of the expression!" + '\n')
            return

        self.parseTreeInputBox.insert('end', "Child node (internal): math" + '\n')
        self.math()

    def parser(self):
        global lineIndex
        print(lineIndex + 1)
        self.parseTreeInputBox.insert('end', "\n\n####Parse tree for line " + str(lineIndex + 1) + "#### \n")
        self.if_exp()
        if myTokens[1] == ":":
            self.parseTreeInputBox.insert('end', "child node (token):" + myTokens[1] + '\n')
            self.accept_token()
            self.parseTreeInputBox.insert('end', "\nparse tree building success!" + '\n')
        elif myTokens[1] == ";":
            self.parseTreeInputBox.insert('end', "child node (token):" + myTokens[1] + '\n')
            self.accept_token()

            self.parseTreeInputBox.insert('end', "\nparse tree building success!" + '\n')
        else:
            self.exp()
            if myTokens[1] == ";":
                self.parseTreeInputBox.insert('end', "child node (token):" + myTokens[1] + '\n')
                self.accept_token()
                self.parseTreeInputBox.insert('end', "\nparse tree building success!" + "\n")
        return

    def quit(self):
        self.quit()

    def __init__(self, root):
        self.myTokens = []
        self.inToken = ("empty", "empty")
        self.master = root
        self.master.title("Lexical Analyzer For TinyPie")
        root.geometry("1300x450")

        self.currLineIndex = IntVar()

        self.sourceInputTitle = Label(self.master, text="Source Code Input: ")
        self.sourceInputTitle.place(x=160, y=15)

        self.sourceInputBox = Text(self.master, width=50, height=20)
        self.sourceInputBox.place(x=20, y=40)

        self.lexicalAnalyzerTitle = Label(self.master, text="Lexical Analyzer Result: ")
        self.lexicalAnalyzerTitle.place(x=580, y=15)

        self.lexicalAnalyzerBox = Text(self.master, width=50, height=20)
        self.lexicalAnalyzerBox.place(x=445, y=40)

        self.parseTreeTitle = Label(self.master, text="Parse Tree: ")
        self.parseTreeTitle.place(x=1035, y=15)

        self.parseTreeInputBox = Text(self.master, width=50, height=20)
        self.parseTreeInputBox.place(x=870, y=40)

        self.currProcessLineLabel = Label(self.master, text="Current Processing Line: ")
        self.currProcessLineLabel.place(x=180, y=380)

        self.currProcessLine = Entry(self.master, width=10)
        self.currProcessLine.place(x=360, y=380)
        # self.currProcessLine['state'] = 'disabled'

        self.nextButton = Button(self.master, text="Next Line", width=10, command=self.nextLine)
        self.nextButton.place(x=344, y=405)

        self.quitButton = Button(self.master, text="Quit", command=quit)
        self.quitButton.place(x=1240, y=380)


if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = PythonGUIForLexer(myTkRoot)
    myTkRoot.mainloop()
