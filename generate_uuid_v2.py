import yaml, uuid, pdb
"""
nodes:
  customers: 1
  vcenter: 2
  systems: 2 #total count of systems for this customer
  volumes: 2 #total count of volumes for all the systems
  snapshots: 1 #total count of snapshots for all the volumes
  clones: 1 #total count of clones for all snapshots

edges:
  customers:
    - systems #systems are associated entity of customers
    - vcenter #vcenter is also associated to entity of customer
  systems: 
    - volumes #volumes are associated entity for systems
  volumes: 
    - snapshots #snapshots are associated entity for volumes
  snapshots: 
    - clones #clones are associated entity for snapshots

"""

class Getgrandparent():

    def __init__(self,parent):
        self.parent = parent
    
    def check_grandparent(parent):
        gparent = [key for key, value in data['edges'].items() if parent in value]
        print(f"parent for {parent} is {gparent}")
        return(gparent)
    
    def generatedate(child,parent):
        new_value = []
        for i in range(data['nodes'][child]):
              new_value.append(child+str(i))
        associations[parent] = new_value
    
    def chk_property(entity):
        if entity in data['properties'].keys():
            return(data['properties'][entity])
    
    def remove_rootnode(parent_list):
        return(parent_list.pop())
    

with open('cfg.yaml', 'r') as yaml_file:
    data = yaml.safe_load(yaml_file)

# Dictionary to represent associations between entities
associations = {}

child_list = []
[child_list.extend(item) if isinstance(item, list) else child_list.append(item) for item in data['edges'].values()]
print(f"edges_list is {child_list}")


def check_grandparent(parent):
    gparent = [key for key, value in data['edges'].items() if parent in value]
    print(f"parent for {parent} is {gparent}")
    return(gparent)

# Associate entities based on edges specified in the configuration
#pdb.set_trace()


for parent, child in data['edges'].items():
    print(f"parent,child values are {parent}, {child}")

for k1,v1 in data['nodes'].items():
    print(f"parent and child of nodes are {k1}, {v1}")

for k2,v2 in data['properties'].items():
    print(f"entities which have properties are {k2} and {v2}")



associations = {}
     
     
def generatedata(child,parent):
    #new_values = {}
    print(f"parent inside generatedata func is {parent}")
    print(f"child inside generatedata func is {child}")
    #starting from -1 in parent reach till length of parent and create new_value and add to associations dict
    if len(child) == 1 and len(parent) == 1:
        new_values = {}
        if root_node in parent:
            associations[parent[-1]] = child
            for i in range(data['nodes'][child[0]]):
                sub_key = child[0]+str(i)
                new_value = str(uuid.uuid4())
                new_values[sub_key] = new_value
                associations[parent[-1]] = new_values  
    if len(child) > 1 and len(parent) == 1:
            #new_key = parent[0]
            for p in range(data['nodes'][parent[0]]):
                new_values = {}
                for c in child:
                    for i in range(data['nodes'][c]):
                        sub_key = c+str(i)+"-"+str(p)
                        new_value = str(uuid.uuid4())
                        #new_values.append(c+str(i)+"-"+str(p))
                        new_values[sub_key] = new_value
                associations[parent[0]+str(p)] = new_values
            print(f"associations are {associations}")
    elif len(child) > 1 and len(parent) == 2:
            #new_key = parent[0]
            new_values = {}
            
            for p in range(data['nodes'][parent[-2]]):
                new_values = {}
                for c in child:
                    for i in range(data['nodes'][c]):
                        sub_key = c+str(i)+"-"+str(p)
                        new_value = str(uuid.uuid4())
                        #new_values.append(c+str(i)+"-"+str(p))
                        new_values[sub_key] = new_value
                        new_key = parent[-2]+str(p)
                    if new_key in associations:
                        break
                    else:
                        associations[new_key] = new_values          
            print(f"associations are {associations}")
    elif len(child) == 1 and len(parent) == 2:
        print(f"parent is {parent}")
        for i in range(data['nodes'][parent[-1]]):
            for j in range(data['nodes'][parent[-2]]):
                new_values = {}
                for k in range(data['nodes'][child[0]]):
                    sub_key = child[0]+str(k)+"-"+str(j)+"-"+str(i)
                    new_value = str(uuid.uuid4())
                    new_values[sub_key] = new_value
                    print(f"new values are {new_values}")
                    new_key = parent[0]+str(j)+"-"+str(i)
                    if new_key in associations:
                        break
                    else:
                        associations[new_key] = new_values
    elif len(parent) == 3:
        print(f"parent is {parent}")
        for i in range(data['nodes'][parent[-1]]):
            for j in range(data['nodes'][parent[-2]]):
                for k in range(data['nodes'][parent[-3]]):
                    new_values = {}
                    for l in range(data['nodes'][child[0]]):
                        sub_key = child[0]+str(l)+"-"+str(k)+"-"+str(j)+"-"+str(i)
                        new_value = str(uuid.uuid4())
                        new_values[sub_key] = new_value
                    new_key = parent[0]+str(k)+"-"+str(j)+"-"+str(i)
                    if new_key in associations:
                        break
                    else:
                        associations[new_key] = new_values
    elif len(parent) == 4:
        print(f"parent is {parent}")
        for i in range(data['nodes'][parent[-1]]):
            for j in range(data['nodes'][parent[-2]]):
                for k in range(data['nodes'][parent[-3]]):
                    for l in range(data['nodes'][parent[-4]]):
                        new_values = {}
                        for m in range(data['nodes'][child[0]]):
                            sub_key = child[0]+str(m)+"-"+str(l)+"-"+str(k)+"-"+str(j)+"-"+str(i)
                            new_value = str(uuid.uuid4())
                            new_values[sub_key] = new_value
                        new_key = parent[0]+str(l)+"-"+str(k)+"-"+str(j)+"-"+str(i)
                        if new_key in associations:
                            break
                        else:
                            associations[new_key] = new_values
    elif len(parent) == 5:
        print(f"parent is {parent}")
        for i in range(data['nodes'][parent[-1]]):
            for j in range(data['nodes'][parent[-2]]):
                for k in range(data['nodes'][parent[-3]]):
                    for l in range(data['nodes'][parent[-4]]):
                        for m in range(data['nodes'][parent[-5]]):
                            new_values = {}
                            for n in range(data['nodes'][child[0]]):
                                sub_key = child[0]+str(n)+"-"+str(m)+"-"+str(l)+"-"+str(k)+"-"+str(j)+"-"+str(i)
                                new_value = str(uuid.uuid4())
                                new_values[sub_key] = new_value
                            new_key = parent[0]+str(l)+"-"+str(k)+"-"+str(j)+"-"+str(i)
                            if new_key in associations:
                                break
                            else:
                                associations[new_key] = new_values
                    
        #print(f"associations are {associations}")

"""
def associateproperties(associations):
    associations['properties'] = {}
    entities = list(associations.keys())
    print(f"entities are {entities}")
    #entities are dict_keys(['customers0', 'systems0-0', 'systems1-0', 'volumes0-0-0', 'volumes1-0-0', 'volumes0-1-0', 'volumes1-1-0', 'snapshots0-0-0-0', 'snapshots1-0-0-0', 'snapshots0-1-0-0', 'snapshots1-1-0-0', 'snapshots0-0-1-0', 'snapshots1-0-1-0', 'snapshots0-1-1-0', 'snapshots1-1-1-0']
    entities_with_properties = list(data['properties'].keys())
    print(f"entities which have properties are {entities_with_properties}")
    for item in entities:
        sub_item = ''.join(char for char in item if char.isalpha())
        if sub_item in entities_with_properties:
            new_key = item
            new_value = data['properties'][sub_item]
            associations['properties'][new_key] = new_value
    
    print(associations)

if you want to create cfg for properties as below:
properties:
  system-capacity:
    - systems0-0
  volume-io:
    - volumes0-0-0
"""
def associateproperties(associations):
    pdb.set_trace
    associations['properties'] = {}
    entities = list(associations.keys())
    pdb.set_trace()
    entities_with_properties = list(data['properties'].values())
    flatlist_entity_prop = [item for sublist in data['properties'].values() for item in sublist]
    new_value_system = []
    new_value_volumeio = []
    for item in entities:
        print(f"item is {item}")    
        if item in flatlist_entity_prop:
            if 'system' in item:
                new_key = "system-capacity"
                new_value_system.append(item)
                associations['properties'][new_key] = new_value_system
            elif 'volume' in item:
                new_key = "volume-io"
                new_value_volumeio.append(item)
                associations['properties'][new_key] = new_value_volumeio
    print(associations)
 
for parent,child in data['edges'].items():
    print(f"parent and child are {parent},{child}")
    parent_list = []
    if parent not in child_list:
        print(f"its a root node")
        root_node = parent
        parent_list.append(parent)
        generatedata(child,parent_list)
    if parent in child_list:
        #need to check if this parent is child of any entity and get its gparent
        #repeat above rule till parent is not child of any entity
        parent_list.append(parent)
        gparent = Getgrandparent.check_grandparent(parent)
        parent_list.append(gparent[0])
        #print(f"grand parent is {gparent}")
        while gparent[0] and gparent[0] in child_list and gparent[0] != root_node:
                #print(f"am inside while loop")
                gparent = Getgrandparent.check_grandparent(gparent[0])
                parent_list.append(gparent[0])
        print(f"parents list is {parent_list}")
        #remove root_node from parent_list
        parent_list = parent_list[0:-1]
        #print(f"length of parent list is {len(parent_list)}")
        #parent_list =[[parent] for parent in parent_list]
        #depending upon length of parent_list we need to have those many for loops
        generatedata(child,parent_list)
        associateproperties(associations)

"""

properties = associations.pop('properties')
relationships = associations

relationships_yaml = yaml.dump(relationships, default_flow_style=False)
properties_yaml = yaml.dump(properties, default_flow_style=False)

relationships_heading = "Relations"
properties_heading = "properties"
combined_yaml = f"{relationships_heading}\n{relationships_yaml}\n{properties_heading}\n{properties_yaml}"
# Concatenate the YAML strings
combined_yaml = relationships_yaml + properties_yaml

# Print the combined YAML output
with open('output.yaml','w') as file:
    op_data = yaml.safe_load(combined_yaml)
    yaml.dump(op_data,file,default_flow_style=False)

print(op_data)


properties = associations.pop('properties')
relations = associations

relations_yaml = yaml.dump(relations, default_flow_style=False)
properties_yaml = yaml.dump(properties, default_flow_style=False)

relations_heading = "Relations"
properties_heading = "properties"
combined_yaml = f"{relations_heading}\n{relations_yaml}\n{properties_heading}\n{properties_yaml}"
# Concatenate the YAML strings
combined_yaml = relations_yaml + properties_yaml

with open('output.yaml','w') as file:
    op_data = yaml.safe_load(combined_yaml)
    yaml.dump(op_data,file,default_flow_style=False)

yaml_output = yaml.dump(associations, default_flow_style=False)
print(yaml_output)

"""

properties = associations.pop('properties')
print(f"properties are {properties}")
relations = associations
print(f"relations between entities are {relations}")
relation_dict = dict()
properties_dict = dict()
relations_yaml = yaml.dump(relations, default_flow_style=False)
properties_yaml = yaml.dump(properties, default_flow_style=False)
relationships_heading = "Relations"
properties_heading = "Properties"
read_relations_yaml = yaml.safe_load(relations_yaml)
read_properties_yaml = yaml.safe_load(properties_yaml)
relation_dict[relationships_heading] = read_relations_yaml
properties_dict[properties_heading] = read_properties_yaml
relationship = yaml.dump(relation_dict, default_flow_style=False)
properties = yaml.dump(properties_dict, default_flow_style=False)
combined_yaml = relationship + properties

with open('output.yaml','w') as file:
    op_data = yaml.safe_load(combined_yaml)
    yaml.dump(op_data,file, default_flow_style=False,sort_keys=False)
