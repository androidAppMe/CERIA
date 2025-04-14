import pandas as pd
import networkx as nx
import pysmile
import os
import subprocess
from functools import reduce

def clean_node_name(name):
    # Replace non-alphanumeric characters with underscores
    cleaned_name = ''.join(c if c.isalnum() else '_' for c in name)
    # Ensure the name starts with a letter
    if not cleaned_name[0].isalpha():
        cleaned_name = 'N_' + cleaned_name
    return cleaned_name
def create_cpt_node( net, id, name, outcomes, x_pos, y_pos):
    handle = net.add_node(pysmile.NodeType.CPT, id)
    net.set_node_name(handle, name)
    net.set_node_position(handle, x_pos, y_pos, 85, 55)
    initial_outcome_count = net.get_outcome_count(handle)
    for i in range(0, initial_outcome_count):
         net.set_outcome_id(handle, i, outcomes[i])
    for i in range(initial_outcome_count, len(outcomes)):
          net.add_outcome(handle, outcomes[i])
    return handle
def remove_cycles(df):
    G = nx.from_pandas_edgelist(df, 'Source', 'Target', create_using=nx.DiGraph())
    try:
        # Find cycles
        cycles = list(nx.find_cycle(G, orientation='original'))
        while cycles:
            # Remove the last edge in the cycle
            G.remove_edge(*cycles[-1][:2])
            cycles = list(nx.find_cycle(G, orientation='original'))
    except nx.NetworkXNoCycle:
        # No cycles found
        pass

    # Create a DataFrame from the acyclic graph
    return nx.to_pandas_edgelist(G)

event = "supplier bankruptcy"
csv_file = "YOUR PATH"+event+"/"+event+"/ready_for_app.csv" 
df = pd.read_csv(csv_file)

# Ensure column names are lowercase and handle them correctly
df['Source'] = df['Source'].apply(clean_node_name)
df['Target'] = df['Target'].apply(clean_node_name)

# Remove loops (cycles) from the DataFrame
df = remove_cycles(df)

# Now you can proceed with the rest of your code...
node_positions = {}
x_offset, y_offset = 100, 100
x_step, y_step = 200, 100
unique_nodes = pd.concat([df['source'], df['target']]).unique()

net = pysmile.Network()

# Create a dictionary to store levels of nodes
node_levels = {}

# Determine levels of nodes
def determine_levels(df):
    for index, row in df.iterrows():
        parent, child = row['source'], row['target']
        if parent not in node_levels:
            node_levels[parent] = 0
        node_levels[child] = node_levels[parent] + 1

determine_levels(df)

# Add nodes from the Excel file
unique_nodes = pd.concat([df['source'], df['target']]).unique()
for node in unique_nodes:
    level = node_levels.get(node, 0)
    x_pos = x_offset + (list(node_levels.keys()).index(node) % 2) * x_step
    y_pos = y_offset + level * y_step
    node_positions[node] = (x_pos, y_pos)
    create_cpt_node(net, node, node, ["Low", "Medium", "High"], x_pos, y_pos)

# Add arcs from the Excel file
for index, row in df.iterrows():
    parent, child = row['source'], row['target']
    print("parent: " + parent)
    print("child: " + child)
    net.add_arc(parent, child)

# Set uniform probabilities for root nodes
for node in unique_nodes:
    parents = net.get_parents(node)
    if len(parents) == 0:  # Root node
        probs = [1.0 / 3] * 3
        net.set_node_definition(node, probs)
    else:  # Non-root node
        parent_outcomes = [net.get_outcome_count(p) for p in parents]
        total_outcomes = 3 * reduce(lambda x, y: x * y, parent_outcomes, 1)
        probs = [0] * total_outcomes
        net.set_node_definition(node, probs)

# Save the network to XDSL file
xdsl_file = "YOUR PATH"+event+"/"+event+"/"+event+".xdsl"
net.write_file(xdsl_file)

# Optional: Open the XDSL file with GeNIe
genie_executable = 'C:\Program Files (x86)\GeNIe Academic 4.1/genie.exe'

if os.path.exists("output.xdsl"):
    subprocess.run([genie_executable, "output.xdsl"], check=True)
else:
    print(f"Error: output.xdsl not found. Please ensure the export step was successful.")
