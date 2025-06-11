import plotly.graph_objects as go
import json

# Parse the data
data = {"layers": [{"name": "Presentation Layer", "color": "#2196F3", "components": ["MainScreen", "SalesScreen", "InventoryScreen", "AnalyticsScreen", "CustomAppBar", "NavigationRail", "ProductGrid", "CartWidget"]}, {"name": "Domain Layer", "color": "#4CAF50", "components": ["SalesProvider", "InventoryProvider", "AnalyticsProvider", "Business Logic", "State Management"]}, {"name": "Data Layer", "color": "#FF9800", "components": ["DatabaseHelper", "Product Model", "Sale Model", "SaleItem Model", "SQLite Database"]}]}

# Create figure
fig = go.Figure()

# Define layer positions and settings
layers_info = [
    {"name": "Presentation Layer", "y": 4, "color": "#2196F3"},
    {"name": "Domain Layer", "y": 2.5, "color": "#4CAF50"}, 
    {"name": "Data Layer", "y": 1, "color": "#FF9800"}
]

# Process each layer
for idx, layer in enumerate(data["layers"]):
    layer_info = layers_info[idx]
    layer_name = layer["name"]
    y_center = layer_info["y"]
    components = layer["components"]
    color = layer_info["color"]
    
    # Add large layer background rectangle
    fig.add_shape(
        type="rect",
        x0=0.5, y0=y_center-0.6, x1=11.5, y1=y_center+0.6,
        fillcolor=color,
        opacity=0.15,
        line=dict(color=color, width=3)
    )
    
    # Add layer title on the left with larger font
    fig.add_trace(go.Scatter(
        x=[0.2], y=[y_center],
        text=[layer_name],
        mode="text",
        textfont=dict(color=color, size=16, family="Arial Black"),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Arrange components horizontally
    num_components = len(components)
    x_start = 1.5
    x_spacing = 1.3
    
    for i, component in enumerate(components):
        x_pos = x_start + i * x_spacing
        
        # Truncate component name to fit in box
        comp_name = component[:12] if len(component) > 12 else component
        
        # Add component box with white background for better text visibility
        fig.add_shape(
            type="rect",
            x0=x_pos-0.6, y0=y_center-0.25, x1=x_pos+0.6, y1=y_center+0.25,
            fillcolor="white",
            opacity=0.9,
            line=dict(color=color, width=2)
        )
        
        # Add component text in black for better visibility
        fig.add_trace(go.Scatter(
            x=[x_pos], y=[y_center],
            text=[comp_name],
            mode="text",
            textfont=dict(color="black", size=10, family="Arial"),
            showlegend=False,
            hoverinfo='skip'
        ))

# Add clear data flow arrows between layers
# Presentation to Domain (requests)
fig.add_annotation(
    x=6, y=3.2,
    ax=6, ay=3.8,
    arrowhead=3,
    arrowsize=2,
    arrowwidth=4,
    arrowcolor="#1FB8CD",
    showarrow=True,
    text=""
)

# Domain to Presentation (responses)
fig.add_annotation(
    x=7, y=3.8,
    ax=7, ay=3.2,
    arrowhead=3,
    arrowsize=2,
    arrowwidth=4,
    arrowcolor="#1FB8CD",
    showarrow=True,
    text=""
)

# Domain to Data (queries)
fig.add_annotation(
    x=6, y=1.9,
    ax=6, ay=3.1,
    arrowhead=3,
    arrowsize=2,
    arrowwidth=4,
    arrowcolor="#1FB8CD",
    showarrow=True,
    text=""
)

# Data to Domain (results)
fig.add_annotation(
    x=7, y=3.1,
    ax=7, ay=1.9,
    arrowhead=3,
    arrowsize=2,
    arrowwidth=4,
    arrowcolor="#1FB8CD",
    showarrow=True,
    text=""
)

# Add data flow labels
fig.add_trace(go.Scatter(
    x=[8.5], y=[3.5],
    text=["User Actions"],
    mode="text",
    textfont=dict(color="#666666", size=11),
    showlegend=False,
    hoverinfo='skip'
))

fig.add_trace(go.Scatter(
    x=[8.5], y=[2.2],
    text=["Data Queries"],
    mode="text",
    textfont=dict(color="#666666", size=11),
    showlegend=False,
    hoverinfo='skip'
))

# Add connection lines to show layer relationships
fig.add_shape(
    type="line",
    x0=6.5, y0=3.6, x1=6.5, y1=3.4,
    line=dict(color="#999999", width=2, dash="dot")
)

fig.add_shape(
    type="line",
    x0=6.5, y0=3.1, x1=6.5, y1=1.9,
    line=dict(color="#999999", width=2, dash="dot")
)

# Update layout with better spacing
fig.update_layout(
    title="Flutter POS System Architecture",
    xaxis=dict(
        range=[-0.5, 12],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[0.2, 5],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    plot_bgcolor="white",
    showlegend=False
)

# Save the chart
fig.write_image("flutter_pos_architecture.png")