import networkx as nx
from bokeh.io import output_notebook, show
from bokeh.models import Circle, ColumnDataSource, LabelSet, MultiLine
from bokeh.plotting import figure, from_networkx
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph

# Make sure your notebook displays bokeh plots inline
output_notebook()


def plot(g, label_property=None) -> figure:
    # Convert the RDF Graph to a NetworkX MultiDiGraph
    G = rdflib_to_networkx_multidigraph(g)
    plt = figure(title="RDF Graph Visualization with Bokeh")

    # Convert the networkx graph to a Bokeh graph renderer using the computed layout
    graph_renderer = from_networkx(G, nx.circular_layout, scale=1, center=(0, 0))
    graph_renderer.node_renderer.glyph = Circle(radius=0.06, fill_color="fill_color")
    graph_renderer.edge_renderer.glyph = MultiLine(
        line_color="gray", line_alpha=0.8, line_width=1
    )
    plt.renderers.append(graph_renderer)

    # Add labels
    x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
    node_labels = [
        str(
            (
                g.value(subject=node, predicate=label_property)
                if label_property
                else node
            )
            or node
        )
        for node in G.nodes()
    ]
    graph_renderer.node_renderer.data_source.data["node_label"] = node_labels
    source = ColumnDataSource(
        {"x": x, "y": y, "node_label": [node_labels[i] for i in range(len(x))]}
    )

    labels = LabelSet(
        x="x",
        y="y",
        text="node_label",
        source=source,
        text_font_size="8pt",
        text_align="center",
    )
    plt.renderers.append(labels)

    # Display the plot in the notebook
    show(plt)
    return plt
