'''
function for Jack to work on 

plan for function:
load in the csv files in datasets one at a time.
for any given mapping function, def an empty df which will 
store target values (these are the names of the csvs, without 
the preceeding 'v'), and the value each mapping function takes 
these to.

write this csv to the folder `fitted_function_values`, as a csv with the file 
name the same as the function name. 

'''

import pandas as pd
from mappings import Mappings, MappingRegistry

# we run for an example file for now 
file_name = 'v8.4806.csv'
df = pd.read_csv(f'datasets/{file_name}')

# to make my life easier, i have all of the calls and puts in the same csv. Hence, to map
# to a scalar value you will have to separate them like this 
df_calls = df.loc[df['call_or_put'] == 'C']
df_puts = df.loc[df['call_or_put'] == 'P']

# init our colleciton of maps, label them as you want
registry = MappingRegistry()
registry.register_mapping('first_attempt', Mappings.different_scaling)

# Apply a mapping
scalar_value_calls = registry.apply_mapping('first_attempt', df_calls)
scalar_value_puts = registry.apply_mapping('first_attempt', df_puts)

# to show shes working 
print(scalar_value_calls - scalar_value_puts)
