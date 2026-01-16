from ..shared.model import Node, Scalar


class Handler():
    def search_node_by_name(self, node: Node, node_name: Node):
        if node.name == node_name:
            return node
        
        named_node = Node()
        for child in node.children:
            if child.name == node_name:
                named_node = child
            else: self.search_node_by_name(child)
        
    def transform(self, node: Node):
        if node.name == "transform":
            code = ''
            for child in node.children:
                code += self.match(child)
            return code
        else: 
            raise(f'expected transform, but found - {node.name}')

    def match(self, node: Node):
        if node.name == "match":
            code = ''
            if (node.children == None) or (node.children == []):
                print("1")
                code += self.match_leaf(node)
            else:
                print("2")
                code += self.match_parent(node)
            return code
        else: 
            raise(f'expected match, but found - {node.name}')

    def match_leaf(self, node: Node):
        tag = node.attrs["tag"] if node.attrs["tag"] != None else ''
        value = node.attrs["value"]
        if tag != '': 
            code = f'<{tag}>{value}</{tag}>\n'
        else: 
            code = f'{value}\n'
        return code

    def match_parent(self, node: Node):
        with_tag = False
        code = ''
        if node.attrs["tag"] != None:
            tag = node.attrs["tag"] 
            with_tag = True

        if with_tag: code += f'<{tag}>\n'
        for child in node.children:
            code += match(child)
        if with_tag: code += f'</{tag}>\n'
        return code



# являются ли имена уникальными? думаю да (нет, я передумал, они только в словаре что-то значат)
# university: Node = Node(name="University")

# students: Node = Node(name="Students")
# student_1 = Node(name="Ivan", attrs={"age": Scalar(30)}, scalar=Scalar("Tired"))
# student_2 = Node(name="Maria", attrs={"age": Scalar(20)}, scalar=Scalar("Fresh"))
# students.add_child(student_1, student_2)

# library: Node = Node(name="Library")
# book_1 = Node(name="book1", attrs={"title": Scalar("War & Peace"), "author": Scalar("Tolstoy")})
# book_2 = Node(name="book2", attrs={"title": Scalar("Lolita"),      "author": Scalar("Nabokov")})
# library.add_child(book_1, book_2)

# university.add_child(students, library)



# в скаляре будет строка в духе "<h2>{value}</h2>, надо добавить вариативность для добавлления условий"
command: Node = Node(name="transform")
match1: Node = Node(name="match", attrs={"name": "book", "tag": Scalar("div")})
match2: Node = Node(name="match", attrs={"name": "title", "tag": Scalar("h1"), "value": Scalar("War & Peace")})
match3: Node = Node(name="match", attrs={"name": "author", "tag": Scalar("p"), "value": Scalar("Tolstoy")})
command.add_child(match1, match2, match3)

handler = Handler()
html = handler.transform(command)
print(html)
print(command.children)

# (transform
#   (match "book"
#     "<div>{children}</div>")
#   (match "title"
#     "<h1>{value}</h1>")
#   (match "author"
#     "<p>{value}</p>"))