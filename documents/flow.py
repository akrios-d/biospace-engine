import graphviz

diagram = graphviz.Digraph("ResearchPipeline", format="svg")
diagram.attr(rankdir="LR", size="8")

# Define nodes with labels and styles
diagram.node("1", "Scrape Publications\nfrom Public Repositories", shape="box", style="filled", fillcolor="#e0f7fa")
diagram.node("2", "Extract Abstracts\n& Detect Corrections", shape="box", style="filled", fillcolor="#ffe0b2")
diagram.node("3", "Categorize & Tag\nUsing LLaMA AI", shape="box", style="filled", fillcolor="#dcedc8")
diagram.node("4", "Store in MongoDB\n(Fast Querying)", shape="box", style="filled", fillcolor="#f8bbd0")
diagram.node("5", "Display in Frontend\n(Interactive Search & Filter)", shape="box", style="filled", fillcolor="#c5cae9")

# Define arrows
diagram.edge("1", "2")
diagram.edge("2", "3")
diagram.edge("3", "4")
diagram.edge("4", "5")

# Output as SVG
svg_content = diagram.pipe().decode("utf-8")

# Save to file
with open("./research_pipeline_diagram.svg", "w") as f:
    f.write(svg_content)

print("Diagram saved as research_pipeline_diagram.svg")
