from src.shared.model import Node, Scalar


class Transformer():
    """трансформирует данные в HTML.
    >>> pre_order() - входная точка
    >>> visit_name() - создает отдельный блок текста с именем в первой строчке, весь смежный текст вложен в этот блок
    >>> visit_attrs_and_scalar() - создает список с атрибутами и скалярным значением в конце списка
    >>> visit_children() - для рекурсивного прохода по дочерним элементам (заново проходит через visit_name() и 
    visit_attrs_and_scalar() для дочернего элемента)
    """
    indent = 4
    def pre_order(self, node: Node, depth=0) -> str:
        code = "<!DOCTYPE html>\n"
        code += self.visit_name(node, depth)
        return code
        
    def visit_name(self, node, depth):
        code = f'{depth * ' '}<div> {node.name}\n'
        depth += self.indent
        code += self.visit_attrs_and_scalar(node, depth)
        code += self.visit_children(node, depth)
        depth -= self.indent
        return code
    
    def visit_attrs_and_scalar(self, node, depth):
        code = ''
        if (node.attrs != None and node.attrs != {}) or (node.scalar != None):
            code += f'{depth * ' '}<ul>\n'
            depth += self.indent
            
            if node.attrs != None and node.attrs != {}:
                for key in node.attrs.keys():
                    code += f'{depth * ' '}<li>{key}: {node.attrs[key]}</li>\n'

            if node.scalar != None:
                code += f'{depth * ' '}<li>Scalar: {node.scalar}</li>\n'
            depth -= self.indent
            code += f'{depth * ' '}</ul>\n'
        return code

    def visit_children(self, node, depth):
        code = ''
        if node.children != None: 
            for child in node.children:
                # print(child.name)
                code += self.visit_name(child, depth)
            depth -= self.indent
            code += f'{depth * ' '}</div>\n'
        return code

# Тестовые входные данные
# root_document: Node = Node(name="Students")
# student_1 = Node(name="Ivan", attrs={"age": Scalar(30)}, scalar=Scalar("Tired"))
# student_2 = Node(name="Maria", attrs={"age": Scalar(20)}, scalar=Scalar("Fresh"))
# root_document.add_child(student_1, student_2)

# transformator = Transformer()
# text = transformator.pre_order(root_document)
# print(text)

# результат программы:
# <!DOCTYPE html>
# <div> Students
#     <div> Ivan
#         <ul>
#             <li>age: 30</li>
#             <li>Scalar: Tired</li>
#         </ul>
#     </div>
#     <div> Maria
#         <ul>
#             <li>age: 20</li>
#             <li>Scalar: Fresh</li>
#         </ul>
#     </div>
# </div>