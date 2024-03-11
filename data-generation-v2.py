import json, yaml, pdb
from uuid import uuid4
import fastavro
from fastavro import writer,reader, json_writer, parse_schema
import random, string, ipaddress, time
from enum import Enum
import pdb

MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES  # 2 ** 32 - 1

outputjson = {}

# Reading the input.yaml to infer the relations and properties
with open("/home/ubuntu-user/glbr/jsonator/output.yaml") as yf:
    yaml_data = yaml.safe_load(yf)

pdb.set_trace()
graph = yaml_data.get('Relations')
properties = yaml_data.get('Properties')
customers_list = graph.get('root_node')

print(f"graph is {graph}")


contentMap = {}

def get_parent(child_node):
    for parent_node, child_nodes in graph.items():
        if child_node in child_nodes:
            return parent_node
    return None

def get_property_key(value):
    for parent_node, child_nodes in properties.items():
        if value in child_nodes:
            return parent_node
    return None

def find_key(node):
    value_to_find = node
    # Find key(s) corresponding to the value
    keys_for_value = [key for key, value_list in properties.items() if value_to_find in value_list]
    # Check if any key(s) were found
    if keys_for_value:
        # If found, print the corresponding key(s)
        print("Key(s) corresponding to value '{}' is/are: {}".format(value_to_find, keys_for_value))
        return(keys_for_value[0])
    else:
        # If the value is not found in the dictionary
        print("Value '{}' not found in the dictionary values.".format(value_to_find))

class Dict2Class(object):
      
    def __init__(self, my_dict):
          
        for key in my_dict:
            setattr(self, key, my_dict[key])
            
class outputClass:
    def __init__(self, my_list,node,value=None):   
        print(f"my_list is {my_list} and node is {node}") 
        for item in my_list:
            name = item["name"]
            generator = item["generator"]
            tag = generator["function"]
            if tag =="distribution":
                result = generateDistribution(item)
            elif tag == "array":
                result_list =[]
                try: 
                    pdb.set_trace()
                    constraint = generator["constraints"]
                    len = constraint.get("total")
                    field = item["type"]["items"]["fields"]
                    while(len>0):
                        substruct = {}
                        for subitem in field:
                        #for nested structure
                            name1 = subitem["name"]
                            generatorsubfield = subitem["generator"]
                            pdb.set_trace()
                            temp = generateFields(self,generatorsubfield,node,value) 
                            substruct[name1] = temp 
                        result_list.append(substruct) 
                        len = len -1
                    result =  result_list  
                        
                except: #handling empty array scenario
                    result = ""              
            else:
                result = generateFields(self,generator,node,value)
            setattr(self, name, result)

def generateDistribution(item):
    
    try: 
        minValue = 0
        maxValue = 0
        intervalMin = 0
        result_list =[]
        rateOfChange = 0
        generator = item["generator"]
        constraint = generator["constraints"]
        len = constraint.get("total") #size of array
        
        #rateOfChange":10, "intervalMin":2,
        
        field = item["type"]["items"]["fields"]
        start_time =  int(round(time.time() * 1000)) #taking current time , can futher be taken as input
        #Getting field inputs
        for subitem in field:
            #for nested structure
                generatorFiled = subitem["generator"]
                constraintField = generatorFiled["constraints"]
                name = subitem["name"]
                if name == "timestamp":
                    intervalMin = constraintField.get("intervalMin")
                else:
                    rangeList = constraintField.get("range")
                    minValue = rangeList[0]
                    #maxValue = rangeList[1]
                    rateOfChange = constraintField.get("rateOfChange")
        value = minValue                             
        while(len>0):
            substruct = {}
            for subitem in field:
            #for nested structure
                generatorFiled = subitem["generator"]
                name = subitem["name"] 
                if name == "timestamp":
                    start_time = start_time + (intervalMin*60)
                    substruct[name] = start_time
                else:
                    value = value + ((rateOfChange/100)*value)
                    substruct[name] = value
            result_list.append(substruct)
            len = len -1      
        result =  result_list  
                      
    except: #handling empty array scenario
        print("exception")  
        result = ""
    return result    
    
def generateFields(self, generator,node,value):
    print(f" from generateFields func and node value is {node} and value is {value}")
    res = ""
    constraint = generator["constraints"]
    tag = generator.get("function")
    match tag:
        case "randomString":
            prefix = constraint.get("prefix")
            length = constraint.get("length")
            if length is None:
                length = 10
            res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) 
            if prefix is not None:
                res = prefix + res 
            return res      
        case "randomNumber": 
            if "range" in constraint:
                rangeList = constraint.get("range")
                age = random.randint(rangeList[0],rangeList[1])
            else: 
                age = random.randint(25,60)
            return age
        case "IpAddress":
            return ipaddress.IPv4Address._string_from_ip_int(random.randint(0, MAX_IPV4))
        case "oneOf":
            optionList = constraint.get("oneOf")
            return random.choice(optionList)
        case "allowedVMOps":
            suOps = ["VIRTUAL_MACHINE_POWER_ON", "VIRTUAL_MACHINE_POWER_OFF", "VIRTUAL_MACHINE_RESET", "VIRTUAL_MACHINE_SHUTDOWN_GUEST_OS", "VIRTUAL_MACHINE_RESTART_GUEST_OS", "VIRTUAL_MACHINE_DELETE"]
            ouOps = ["VIRTUAL_MACHINE_BACKUP_CREATE", "VIRTUAL_MACHINE_BACKUP_UPDATE", "VIRTUAL_MACHINE_BACKUP_DELETE", "VIRTUAL_MACHINE_SNAPSHOT_CREATE", "VIRTUAL_MACHINE_SNAPSHOT_UPDATE", "VIRTUAL_MACHINE_SNAPSHOT_DELETE", "VIRTUAL_MACHINE_RESTORE", "VIRTUAL_MACHINE_DISKS_RESTORE"]
            vmPrivilegeLevel = constraint.get("vmlvl")
            if vmPrivilegeLevel == 0:
                opsList = suOps + ouOps
            else:
                opsList = ouOps
            return opsList
        case "generateUUID":
            uuid = str(uuid4())
            return uuid
        case "generateMORefID":
            prefix = constraint.get("prefix")
            if prefix == "datacenter":
                morefID = prefix + "-" + str(random.randint(0, 9))
            elif prefix == "vm":
                morefID = prefix + "-" + str(random.randint(0, 999))
            elif prefix == "resourcepool":
                morefID = prefix + "-" + str(random.randint(0, 99))
            return morefID
        case "generateDisplayName":
            prefix = constraint.get("prefix")
            if prefix == "datastore":
                displayName = prefix + "-MAS-" + str(random.randint(0, 9))
            else:
                displayName = prefix
            return displayName
        case "generateName":
            prefix = constraint.get("prefix")
            if prefix == "datacenter":
                objName = "Datacenter-" + str(random.randint(0, 9))
            elif prefix == "vm":
                objName = prefix + "-" + str(random.randint(0, 999))
            elif prefix == "datastore":
                objName = prefix + "-" + str(random.randint(0, 999))
            elif prefix == "resourcepool":
                objName = prefix + "-" + str(random.randint(0, 99))
            return objName
        case "generateResURI":
            apiURL = "/api/v1"
            prefix = constraint.get("prefix")
            field =constraint.get("from")
            resID = getattr(self,field)
            if prefix == "datacenter":
                resURI = apiURL + "/datacenter/" + resID
            elif prefix == "vm":
                resURI = apiURL + "/virtual-machines/" + resID
            elif prefix == "datastore":
                resURI = apiURL + "/datastores/" + resID
            elif prefix == "volumes":
                resURI = apiURL + "/volumes/" + resID
            elif prefix == "resourcepool":
                resURI = apiURL + "/resourcepool/" + resID
            elif prefix == "storagepool":
                resURI = apiURL + "/storage-pools/" + resID
            elif prefix == "storagesystem":
                resURI = apiURL + "/storage-systems/" + resID
            elif prefix == "volumeset":
                resURI = apiURL + "/volumeset/" + resID
            elif prefix == "virtualdisks":
                resURI = apiURL + "/virtualdisks/" + resID
            elif prefix == "cluster":
                resURI = apiURL + "/cluster/" + resID
            elif prefix == "folder":
                resURI = apiURL + "/folders/" + resID
            elif prefix == "storagefolder":
                resURI = apiURL + "/storage-folder/" + resID
            elif prefix == "host":
                resURI = apiURL + "/hosts/" + resID
            elif prefix == "hypervisormanager":
                resURI = apiURL + "/hypervisor-manager/" + resID
            elif prefix == "protectionjob":
                resURI = apiURL + "/protection-jobs/" + resID
            elif prefix == "protectionpolicy":
                resURI = apiURL + "/protection-policy/" + resID
            return resURI
        case "generateResType":
            prefix = constraint.get("prefix")
            if prefix == "vm":
                optionList = constraint.get("oneOf")
                resType = random.choice(optionList)
            elif prefix == "app":
                resType = "VMWARE"
            else:
                resType = prefix
            return resType
        case "generateVersion":
            prefix = constraint.get("prefix")
            return prefix
        case "generateCapacity":
            unit = constraint.get("unit")
            sizesInGibiBytes = (20, 30, 40, 50)
            size = random.choice(sizesInGibiBytes)
            if unit == "bytes":
                sizeinUnit = size * (1024 ** 3)
            return sizeinUnit
        case "dependentOnSelf": # depends on its own field
            #need to get value of the key and it has to traverse like parent['key'] inorder to get value
            parentnode = get_parent(node)
            field =constraint.get("from")
            if field == "node":
                if parentnode:
                    value1 = graph[parentnode][node]
                    return value1
                else:
                    value1 = graph[node]
                    return value1
            else:
                return getattr(self,field) #fqdn system
        case "dependentOnParent":
            # there are 2cases here
            #pdb.set_trace()
            parentnode = get_parent(node)
            field =constraint.get("from")
            if field == "parentId":  #customerId
                return customers_list[parentnode]
            else:
                #print(field)
                #targetMap[get_parent(node)]
                #print(node,parentnode)
                if parentnode is not None:
                   value1=contentMap[parentnode][0][field]
                   #print(value)
                   return value1
                return ""   # to do exact , how to exact that field from parent as we are not storing parent details in dag
        case "dependentOnProperty":  #systemcapacity (systemid) dependends on system (id)
            pdb.set_trace()
            dependentfield =constraint.get("from")
            #node is coming as system-capacity
            #parentnode = get_property_key(node)
            #parentnode = find_key(node)
            #parentnode = find_key(value)
            if value:
                parentnode = value
            print(f"parentnode is {parentnode}")
            if parentnode is not None:
                print(f"contentMap is {contentMap}")
                value1=contentMap[parentnode][0][dependentfield]
                return value1
            else:
                return ""
        case "indirectDependency": #volume usedSizeMiB depend on system-capacity  x percent of "capacityByTier.totalUsed"
               print(f"value is {value} and node is {node}")
               dependentfield =constraint.get("from")
               print(f"dependent field is {dependentfield}")
               pdb.set_trace()
               percent =constraint.get("percent")   
               if value != "None":
                   parentnode = value
               else:
                   parentnode = get_parent(node)
               print(f"parentnode is {parentnode}")
               #get property of parentnode
               propertiesnode = find_key(parentnode)
               if propertiesnode :
                #propertiesNode = properties[parentnode][0] 
                #propertiesNode = find_key(parentnode)
                #value = contentMap[propertiesNode][0][dependentfield]
                print(f"contentmap value is {contentMap[propertiesnode][0]['capacityByTier.totalUsed']}")
                value1 = contentMap[propertiesnode][0][dependentfield]
                return (percent/100)*value1
               else:
                   print(f"no need to generate property for this entity {node}")
                   return ""
        case "timeinms":
               tnow = int(round(time.time() * 1000))
               return tnow
        case _:
            return ""
        
def generate(node,value="None"):
    print(f"Entering generate() function with {node}")
    #node is system-capacity and value=systems0-0
    #pdb.set_trace()
    if "capacity" in node:
        schemafile = "system-capacity.avsc"
    elif "system" in node:
        schemafile = "get_ss.avsc"
    elif "-io" in node:
        schemafile = "volume-io.avsc"    
    elif "volume" in node:
        schemafile = "volume.avsc"
    elif "VM" in node:
        schemafile = "vms.avsc"
    elif "backups" in node:
        schemafile = "vm-backups.avsc"
    elif "Snaps" in node:
        schemafile = "vm-snapshots.avsc"
    else:
        print(f"Exiting generate() function")
        return
    print(f"Schemafile is {schemafile}")
    with open(schemafile, "r") as f:
        output_sc = f.read()
    output_schema = fastavro.parse_schema(json.loads(output_sc))
    schemaObj = Dict2Class(output_schema)
    print(f"Schema obj is {schemaObj}")
    fields = getattr(schemaObj,"fields")
    print(f"Fields are ...")
    for field in fields:
        print(field)
    generator = getattr(schemaObj,"generator")
    print(f"Generators are {generator}")
    items = generator["noOfitems"]
    print(f"Items are {items}")
    if value != "None":
        outputfile =generator["filePath"] + node + value +".json"
    else:
        outputfile =generator["filePath"] + node +".json"
    print(f"Output file is {outputfile}")
    result = []
    for i in range(items):
        resultObj = outputClass(fields, node, value)
        #converting object to dictionary
        j_data = json.loads(json.dumps(resultObj.__dict__)) 
        result.append(j_data) 
    #print(result)
    contentMap[node] = result
    outputjson["items"]=result
    outputjson["total"]= items
    outputjson["pageLimit"]= 500
    outputjson["pageOffset"]= 0
    outputjson["requestUri"]= "https://atlaspoc2-app.qa.cds.hpe.com/api/v1/storage-systems"
    #with open("backup.avsc", "r") as f:
    #   schema = f.read()
    #writer(open('output.avro', "wb"), output_schema, result)
    # targetmap[node] =outputjson
    with open(outputfile, "w") as outfile:
        outfile.write(json.dumps(outputjson, indent=2))

def dfs(graph, node, id, visited=None):
    print(f"************** ITERATION ********************")
    if visited is None:
        visited = set()
    visited.add(node)
    #print(f"Graph is {graph}")
    print(f"node is {node}")
    print(f"uuid is {id}")
    print(f"visited is {visited}")
    generate(node)
    flatlist_entity_prop = [item for sublist in properties.values() for item in sublist]
    if node in flatlist_entity_prop:
        print(f"{node} has properties.")
        value = node
        print(f"value is {value}")
        property = find_key(node)
        if property:
            generate(property,value)
        else:
            print(f"entity {node} not associated with property {property}")
        """
        for property in properties[node]:
            print(f"Property {property} to be generated.")
            generate(property,value)
        """
    for neighbor in graph.get(node, []):
        #pdb.set_trace()
        print(f"Neighbor is {neighbor}.")
        #id = neighbor
        if neighbor not in visited:
            dfs(graph, neighbor, id, visited)

for key, value in customers_list.items():
    print(f"key, value is {key}, {value}")
    dfs(graph, key, value)
