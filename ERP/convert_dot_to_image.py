import pydot

# Load the DOT file
dot_file = 'models.dot'
graph = pydot.graph_from_dot_file(dot_file)

# Convert the graph to an image
image_file = 'models.png'
graph[0].write_png(image_file)
