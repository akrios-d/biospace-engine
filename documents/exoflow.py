import graphviz

exo = graphviz.Digraph("ExoLexisFlow", format="png")
exo.attr(rankdir="LR")
exo.attr("node", shape="box", style="filled", fontname="Helvetica")

# Nodes
exo.node("A", "Fetch Scientific\nPublications", fillcolor="#e0f7fa")
exo.node("B", "AI Extraction\n- Abstracts\n- Tags\n- Topics", fillcolor="#ffe0b2")
exo.node("C", "Categorization\n& Tag Suggestion", fillcolor="#dcedc8")
exo.node("D", "Store in DB\n(MongoDB)", fillcolor="#f8bbd0")
exo.node("E", "Search & Filter\nby Keywords, Tags, Category", fillcolor="#c5cae9")
exo.node("F", "Display in Frontend", fillcolor="#e1bee7")

# Edges
exo.edge("A", "B")
exo.edge("B", "C")
exo.edge("C", "D")
exo.edge("D", "E")
exo.edge("E", "F")

# Render diagram
exo.render("exolexis_workflow_diagram", format="png", cleanup=True)
