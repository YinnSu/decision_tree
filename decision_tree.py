import sys
import pandas as pd
import numpy as np
import math
import xml.etree.cElementTree as ET

def data_preprocess():
    """
    Read input data.
    Add new header for each columns (att0 ...attn).
    The header for the last column is label, which is the given prediction.
    """
    data = pd.read_csv('car.csv',header= None)
    len_columns = len(data.columns.values)
    columns_list =  data.columns.tolist()
    for i in range(len_columns-1):
        columns_list[i] ="att"+ str(i)
        columns_list[len_columns-1] = "label"
    data.columns = columns_list
    return data, columns_list

data, attrn_list = data_preprocess()
del attrn_list[-1]


 # Return a list which contains all unique category values
def get_attrn_values(data_parent, attrn):
    attrn_values= data_parent[attrn].value_counts().index.tolist()
    return attrn_values


# Return a list which contains the frequency of all unique category values
def get_freq(data_parent, attrn):
    attrn_value_freqs = data_parent[attrn].value_counts().values.tolist()
    return attrn_value_freqs


entropy_base = len(get_attrn_values(data, 'label'))





def get_data_children(data_parent, attrn):   
    data2 = data.set_index(attrn)
    attrn_values = get_attrn_values(data_parent, attrn)
    data_children=[]
    for value in attrn_values:
        data_children.append(data2.loc[value])
    return data_children
 



# Main identification tree class
# There will be one instance of the class per node   
 
class IdenTree:    
    data_parent = data 
    data_children = [data]
    features_list = attrn_list    # The orginal list of attributes
    feature= 'label'         # The feature which is selected in terms of the highest IG
    level = 1
    entropy = None
    label = None   # The prediction of the node with 0 entropy
    
    
    
    def __init__(self, data_parent):
        self.data_parent = data_parent
        
    
        
    def Entropy(self):
        entropy = 0.0
        for child in self.data_children:
            if len(get_attrn_values(child,'label')) == 1: 
                #if in label column of child dataset only left one label value
                #set entropy = 0
                entropy = 0
            else:
                freqs = get_freq(child,'label')
                sum_freqs = sum(freqs)
                for freq in freqs :
                    prob = freq/sum_freqs
                    entropy +=(-prob)*math.log(prob, entropy_base)
        self.entropy = entropy
        return entropy


    def info_gain(self, attrn):
        freq = get_freq(self.data_parent, attrn)
        

#            
        
#        data2 = get_data2(data, attrn)
#        attrn_values,attrn_value_freqs = get_count_list(data_parent, attrn)
#        sum_freq=sum(attrn_value_freqs)
#        attrn_dict = dict(zip(attrn_values,attrn_value_freqs))
#    #    print(attrn_dict)
#        EA=0.0
#        data_children = []
#        for attrn_value, attrn_value_freqs in attrn_dict.items():
#            data_child = get_data_child(data2,attrn_value)
#    #        print(data_child['label'])
#            entropy_child = entropy(data, data_child, 'label') 
#            print(entropy_child)
#            prob_child = attrn_value_freqs /sum_freq
#    #        print(prob_child)
#            EA += prob_child * entropy_child
#    ##        print(EA)
#        info_gain = entropy_parent - EA
#    #    print(info_gain)
#        return info_gain, data_children
##

#    def choose_best_attrn(self, data_parent):
#        attrn_list = data.columns.tolist()
#        del attrn_list[-1]
#        best_gain = float('-inf')
#        for attrn in attrn_list:
#            gain = info_gain(data_parent, attrn)
#            if gain > best_gain:
#                best_gain = gain
#                best_attrn = attrn
#        self.feature = best_attrn
#        
#    def get_data_children(self):
#        attrn_values,attrn_value_freqs = get_count_list(self.data_parent, self.feature)
#        attrn_dict = dict(zip(attrn_values,attrn_value_freqs))
#        data2 = get_data2(self.data_parent, self.feature)
#        data_children = []
#        for attrn_value, attrn_value_freqs in attrn_dict.items():
#            data_child = get_data_child(data2,attrn_value)
#            data_children.append(data_child)
#        return data_children
#        
        
       

root = IdenTree(data)
root.Entropy()
root.entropy

    
def output_xml():
    parent = ET.Element("tree",attrib = {"entropy":str(root.entropy)})
    child_attribs = {"entropy":"","feature":"", "value":""}
    child = ET.SubElement(parent, "node", attrib = child_attribs).text="attrn_value"
    tree = ET.ElementTree(parent)
    tree.write("solution.xml")  
    
    
output_xml()   
    
    
    
    
    
    
    
    
    
    
    
    