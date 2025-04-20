import os
import django

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ERP.settings")

# Initialize Django
django.setup()



from django.apps import apps
import matplotlib.pyplot as plt
import networkx as nx

# Function to extract model relationships
def extract_model_relationships():
    relationships = []
    for model in apps.get_models():
        for field in model._meta.get_fields():
            if field.is_relation:
                relationships.append((model.__name__, field.name, field.related_model.__name__))
    return relationships

# Function to visualize relationships with Matplotlib

def visualize_relationships(relationships):
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes and edges
    for relationship in relationships:
        source, _, target = relationship
        G.add_edge(source, target)
    
    # Add data attributes for nodes
    for node in G.nodes():
        G.nodes[node]['subset'] = 0  # Assign a subset value to each node
    
    # Draw the graph with a hierarchical layout
    pos = nx.multipartite_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=20)
    
    # Show the plot
    plt.show()

# Main function
def main():
    relationships = extract_model_relationships()
    visualize_relationships(relationships)

if __name__ == "__main__":
    main()

