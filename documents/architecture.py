import graphviz

# Create the architecture diagram
arch = graphviz.Digraph("SystemArchitecture", format="png")
arch.attr(rankdir="LR")
arch.attr("node", shape="box", style="filled", fontname="Helvetica")

# Backend cluster
with arch.subgraph(name="cluster_backend") as backend:
    backend.attr(label="Backend", color="#c5cae9", style="filled", fillcolor="#e8eaf6")
    backend.node("python", "Python\n(Scraper + AI Classifier)", fillcolor="#ffecb3")
    backend.node("java", "Java\n(API / Business Logic)", fillcolor="#ffe0b2")
    backend.node("mongo", "MongoDB\n(Database)", fillcolor="#dcedc8")

# AI cluster
with arch.subgraph(name="cluster_ai") as ai:
    ai.attr(label="AI", color="#f8bbd0", style="filled", fillcolor="#fce4ec")
    ai.node("ollama", "Ollama\n(Local LLM)", fillcolor="#f48fb1")

# Frontend cluster
with arch.subgraph(name="cluster_frontend") as frontend:
    frontend.attr(label="Frontend", color="#b2ebf2", style="filled", fillcolor="#e0f7fa")
    frontend.node("angular", "Angular 20\n(TypeScript)", fillcolor="#80deea")
    frontend.node("http", "HTTP Client", fillcolor="#4dd0e1")

# Connections
arch.edge("python", "ollama", label="Local AI calls")
arch.edge("python", "mongo", label="Insert documents")
arch.edge("java", "mongo", label="Query / Serve data")
arch.edge("angular", "http", label="API calls")
arch.edge("http", "java", label="REST API")

# Render to PNG
arch.render("system_architecture_diagram", format="png", cleanup=True)
