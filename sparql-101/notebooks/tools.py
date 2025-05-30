import re

import networkx as nx
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.models import Circle, ColumnDataSource, HoverTool, LabelSet, MultiLine
from bokeh.plotting import figure, from_networkx
from rdflib import RDF, RDFS, Graph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph

# Make sure your notebook displays bokeh plots inline
output_notebook()
from bokeh.models import (
    BoxSelectTool,
    Circle,
    HoverTool,
    MultiLine,
    NodesAndLinkedEdges,
    TapTool,
)
from bokeh.palettes import Spectral4


def default_layout(G):
    df = pd.DataFrame(index=G.nodes(), columns=G.nodes())
    for row, data in nx.shortest_path_length(G):
        for col, dist in data.items():
            df.loc[row, col] = dist

    df = df.fillna(df.max().max())

    return nx.kamada_kawai_layout(G, dist=df.to_dict())


def plot_graph(
    g,
    label_property=None,
    layout=None,
    limit: int = 0,
    pattern=None,
    line_color="gray",
    fig=None,
) -> figure:
    # Convert the RDF Graph to a NetworkX MultiDiGraph
    filtered_graph = Graph()
    count = 0
    pattern = re.compile(pattern) if pattern else None
    for x in g:
        if pattern and not pattern.match(str(x[2])):
            continue
        if x[1] == label_property:
            continue
        filtered_graph.add(x)
        count += 1
        if limit and count > limit:
            break
    if not count:
        raise ValueError("No triples found matching the pattern.")

    # print(filtered_graph.serialize(format="turtle"))
    G = rdflib_to_networkx_multidigraph(filtered_graph)
    fig = fig or figure(title="RDF Graph Visualization with Bokeh")
    fig.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())

    # Generate a customized layout if not provided.
    if not layout:
        layout = default_layout(G)

    # Calculate node degrees
    degrees = dict(G.degree())
    max_degree = max(degrees.values()) if degrees else 1

    # Convert the networkx graph to a Bokeh graph renderer using the computed layout
    graph_renderer = from_networkx(G, layout, scale=1, center=(0, 0))

    # Normalize node sizes based on degree
    node_sizes = {
        node: 0.01 + (degree / max_degree) * 0.05 for node, degree in degrees.items()
    }
    graph_renderer.node_renderer.data_source.data["node_size"] = [
        node_sizes[node] for node in G.nodes()
    ]

    # Add edge styles for rdfs:subClassOf
    edge_attrs = []
    for start_node, end_node, edge_data, _ in G.edges(data=True, keys=True):
        # print(edge_data)
        if str(edge_data) in (
            str(RDF.type),
            str(RDFS.subClassOf),
            str(RDFS.subPropertyOf),
        ):
            edge_attrs.append("dashed")
        else:
            edge_attrs.append("solid")
    graph_renderer.edge_renderer.data_source.data["line_dash"] = edge_attrs

    graph_renderer.node_renderer.glyph = Circle(
        radius="node_size", fill_color="fill_color"
    )
    graph_renderer.node_renderer.selection_glyph = Circle(
        radius="node_size", fill_color=Spectral4[2]
    )
    graph_renderer.node_renderer.hover_glyph = Circle(
        radius="node_size", fill_color=Spectral4[1]
    )

    graph_renderer.edge_renderer.glyph = MultiLine(
        line_color=line_color, line_alpha=0.8, line_width=1, line_dash="line_dash"
    )
    graph_renderer.edge_renderer.selection_glyph = MultiLine(
        line_color="red", line_width=5
    )
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color="red", line_width=5)
    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()

    fig.renderers.append(graph_renderer)

    def _node_label(node):
        return node_label(g, node, label_property)

    # Add labels
    x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
    node_labels = [_node_label(node) for node in G.nodes()]
    graph_renderer.node_renderer.data_source.data["node_label"] = node_labels
    source = ColumnDataSource(
        {"x": x, "y": y, "node_label": [node_labels[i] for i in range(len(x))]}
    )

    labels = LabelSet(
        x="x",
        y="y",
        text="node_label",
        source=source,
        #   text_font_size="8pt",
        text_align="center",
    )
    fig.renderers.append(labels)

    # Display the plot in the notebook
    show(fig)
    return fig


def node_label(g, node, label_property=None):
    try:
        if ret := g.value(subject=node, predicate=label_property):
            return str(ret)
    except Exception:
        pass
    return re.split(r"[/:#]", str(node))[-1]


from rdflib import URIRef
from rdflib.namespace import RDFS


def test_node_label():
    g = Graph()
    g.parse("https://dbpedia.org/data/Tortelloni.n3", format="n3")
    node = URIRef("http://dbpedia.org/resource/Broth")
    assert node_label(g, node, RDFS.label) == "Broth"


def test_inputsource():
    g = Graph()
    g.parse("https://dbpedia.org/data/Tortelloni.n3", format="n3")
