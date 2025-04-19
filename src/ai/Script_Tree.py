import webbrowser

class Node:

    def __init__(self, tag, parent=None):
        self.parent = parent
        self.tag = tag
        self.list_chlidren = []
    
    def is_root(self):
        if not self.parent:
            return True
        else:
            return False

    def is_leaf(self):
        if len(self.list_chlidren) == 0:
            return True
        else:
            return False
    
    def add_children_node(self, node_children):
        node_children.parent = self
        self.list_chlidren.append(node_children)
    
    def add_children_tag(self, tag):
        node_children = Node(tag, self)
        self.list_chlidren.append(node_children)
        return node_children
    
def afficher_arbre_mermaid_aux(Node):
    def echapper(Node_tag):
        if isinstance(Node_tag,tuple) :
            if isinstance(Node_tag[1],str):
                return (Node_tag[0], Node_tag[1].replace("'"," "))
            else :
                return Node_tag
        else:
            return Node_tag.replace("'"," ")

    texte = ""
    identifiant_Node = id(Node)
    for fils in Node.list_chlidren:
        identifiant_fils = id(fils)
        texte += f'    {identifiant_Node}["{echapper(Node.tag)}"] --> {identifiant_fils}["{echapper(fils.tag)}"] ;\n'
        texte += afficher_arbre_mermaid_aux(fils)
    return texte

class Tree:

    def __init__(self, tag):
        self.root = Node(tag)
    
    def afficher_arbre_mermaid(self):
    
        graphe_mermaid = "graph TD;\n"
        graphe_mermaid += afficher_arbre_mermaid_aux(self.root)

        # Préparation du HTML complet avec Mermaid.js
        graphe_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{startOnLoad: true}});
            </script>
        </head>
        <body>
        <div class="mermaid">
        {graphe_mermaid}
        </div>
        </body>
        </html>
        '''

        fichier_html = open('diagramme.html', 'w+', encoding='utf-8')
        fichier_html.write(graphe_html)
        fichier_html.close()

        webbrowser.open('diagramme.html')
