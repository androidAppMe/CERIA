#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[ ]:





# In[10]:


from IPython.display import display, clear_output, IFrame
import ipywidgets as widgets
from ipywidgets import Button, Text, VBox, HBox, Dropdown, Output, Label
import networkx as nx
from pyvis.network import Network
import pandas as pd
import ctypes

event = "decrease_in_supply"
output = Output()
def create_graph_from_excel(file_path):
    # Read the Excel file
    data = pd.read_csv(file_path)
    
    # Create a directed graph from the dataframe
    model = nx.DiGraph()
    edge_list = list(zip(data['Source'], data['Target']))
    model.add_edges_from(edge_list)
    return model

file_path = "YOUR PATH"+"decrease in supply" 
model = create_graph_from_excel(file_path+"\\"+event+"_user_defined_version.csv")

output = Output()

def draw_network(model, output_widget):
    net = Network(notebook=True, directed=True, height="500px", width="100%", cdn_resources='in_line')
    net.from_nx(model)
    
    net.toggle_physics(False)
    for edge in net.edges:
        edge["smooth"] = False
    html_output = net.generate_html()
    file_path = "bayesian_network.html"
    with open(file_path, "w", encoding='utf-8') as html_file:
        html_file.write(html_output)
    with output_widget:
        clear_output(wait=True)
        display(IFrame(src=file_path, width="100%", height="500px"))
def update_menues():
    node_rename_selector.options = list(model.nodes())
    node_selector.options = list(model.nodes())
    leads_to_dropdown.options = list(model.nodes())
    leads_from_dropdown.options= list(model.nodes())
    delete_source_dropdown.options= list(model.nodes())
    delete_target_dropdown.options= list(model.nodes())
    source_node_dropdown.options= list(model.nodes())
    target_node_dropdown.options= list(model.nodes())
   
    
def add_edge(source, target):
    if source and target and source != target:
        if not model.has_edge(source, target):
            model.add_edge(source, target)
            draw_network(model, output)
            print(f"Edge added between {source} and {target}")
        else:
            print("Edge already exists.")
    else:
        print("Invalid node selection or same node selected.")
              
def add_node_and_edges(node_name, leads_to, leads_from):
    with output:
        if node_name not in model.nodes():
            model.add_node(node_name)
            if leads_to != 'None':  # Only add edge if 'None' is not selected
                model.add_edge(node_name, leads_to)
            if leads_from != 'None':  # Only add edge if 'None' is not selected
                model.add_edge(leads_from, node_name)
            draw_network(model, output)
            print(f"Added node {node_name} with edges from {leads_from} to {leads_to}")
        else:
            print("Node already exists.")

              
def on_add_node_button_clicked(b):
    node_name = new_node_name.value.strip()
    leads_to = leads_to_dropdown.value
    leads_from = leads_from_dropdown.value
    if node_name:
        add_node_and_edges(node_name, leads_to, leads_from)
        new_node_name.value = ''
        # Update dropdown options to include new node and retain 'None' option
        update_menues() 
              
def delete_node(node):
    if node in model:
        model.remove_node(node)
        draw_network(model, output)
        update_menues()
              
def on_delete_button_clicked(b):
    delete_node(node_selector.value)               

              
def rename_node(b):
    old_name = node_rename_selector.value
    new_name = new_name_input.value.strip()
    
    if new_name and old_name in model.nodes():
        mapping = {old_name: new_name}
        nx.relabel_nodes(model, mapping, copy=False)
       
        draw_network(model, output)  # Redraw the network in the output widget
        new_name_input.value = ''  # Reset text field
    update_menues()    
    
def add_edge(source, target):
    if source and target and source != target:
        if not model.has_edge(source, target):
            model.add_edge(source, target)
            draw_network(model, output)
            print(f"Edge added between {source} and {target}")
        else:
            print("Edge already exists.")
    else:
        print("Invalid node selection or same node selected."  )            
source_node_dropdown = Dropdown(options=list(model.nodes()), description='Source Node:')
target_node_dropdown = Dropdown(options=list(model.nodes()), description='Target Node:')
add_edge_button = Button(description='Add Edge',button_style='success')

# Event handler for the button
def on_add_edge_button_clicked(b):
    add_edge(source_node_dropdown.value, target_node_dropdown.value)
def delete_edge(source, target):
    if source and target and model.has_edge(source, target):
        model.remove_edge(source, target)
        draw_network(model, output)
        print(f"Edge removed between {source} and {target}")
    else:
        print("Edge does not exist or invalid node selection.")

# Dropdowns for selecting the source and target nodes of the edge to delete
delete_source_dropdown = Dropdown(options=list(model.nodes()), description='Source Node:')
delete_target_dropdown = Dropdown(options=list(model.nodes()), description='Target Node:')
delete_edge_button = Button(description='Delete Edge',button_style='success')

# Event handler for the delete edge button
def on_delete_edge_button_clicked(b):
    delete_edge(delete_source_dropdown.value, delete_target_dropdown.value)

def save_graph_to_csv(b):
    edges = list(model.edges())
    df = pd.DataFrame(edges, columns=['Source', 'Target'])
    save_path = file_path + "\\ready_for_app.csv"
    df.to_csv(save_path, index=False)
    print(f"Graph saved to {save_path}")    
    
new_node_name = Text(description="New Node:")
leads_to_dropdown = Dropdown(options=['None'] + list(model.nodes()), description='Causes:')
leads_from_dropdown = Dropdown(options=['None'] + list(model.nodes()), description='Caused from:')
add_node_button = Button(description="Add Node",button_style='success')

node_input_ui = VBox([new_node_name, HBox([leads_from_dropdown, leads_to_dropdown]), add_node_button])
display(node_input_ui)    
    
    

add_edge_button.on_click(on_add_edge_button_clicked)
# Layout the widgets for adding edges
edge_addition_ui = VBox([HBox([source_node_dropdown, target_node_dropdown]), add_edge_button])

# Display the new UI components
display(edge_addition_ui)
              
              

       
        
node_rename_selector = widgets.Dropdown(options=list(model.nodes()), description='Select Node:')
new_name_input = widgets.Text(value='', placeholder='Enter new node name', description='New Name:')
rename_button = widgets.Button(description='Rename Node',button_style='success')
output = widgets.Output()


rename_button.on_click(rename_node)

display(widgets.VBox([node_rename_selector, new_name_input, rename_button]))
add_node_button.on_click(on_add_node_button_clicked)



node_selector = widgets.Dropdown(options=list(model.nodes()), description='Select Node:')
delete_button = widgets.Button(description='Delete Node',button_style='success')

delete_button.on_click(on_delete_button_clicked)
ui = widgets.VBox([node_selector, delete_button])
display(ui)


delete_edge_button.on_click(on_delete_edge_button_clicked)
# Layout the widgets for deleting edges
edge_deletion_ui = VBox([HBox([delete_source_dropdown, delete_target_dropdown]), delete_edge_button])

# Display the new UI components for edge deletion
display(edge_deletion_ui)

save_button = Button(description="Save Graph", button_style='success')
save_button.on_click(save_graph_to_csv)
display(save_button)

display(output)
draw_network(model, output)



# In[ ]:





# In[ ]:




