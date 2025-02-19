import pandas as pd
import os
from mappings import Mappings, MappingRegistry

def processAllDatasets():
    # Get the directory containing this script
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    
    # Create fitted_function_values directory if it doesn't exist
    outputDir = os.path.join(scriptDir, '..', 'fitted_function_values')
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Get list of all CSV files in datasets directory
    datasetsDir = os.path.join(scriptDir, '..', 'datasets')
    datasetFiles = [f for f in os.listdir(datasetsDir) if f.endswith('.csv')]
        
    # Initialize registry and get all mapping functions
    # This needs updating when new functions are added
    registry = MappingRegistry()
    registry.register_mapping('first_ever_attempt', Mappings.first_ever_attempt)
    registry.register_mapping('different_scaling', Mappings.different_scaling)

    # For each mapping function
    for mappingName, mappingFunc in registry.mappings.items():
        # Create empty df
        resultsDF = pd.DataFrame(columns=['target', 'callsValue', 'putsValue'])
        
        # Process each CSV file
        for fileName in datasetFiles:
            # Extract target value 
            target = float(fileName[1:-4])
            
            # Read and process the CSV
            csvPath = os.path.join(datasetsDir, fileName)
            df = pd.read_csv(csvPath)
            
            # Split into calls and puts
            dfCalls = df.loc[df['call_or_put'] == 'C']
            dfPuts = df.loc[df['call_or_put'] == 'P']
            
            # Apply mapping function 
            callsValue = registry.apply_mapping(mappingName, dfCalls)
            putsValue = registry.apply_mapping(mappingName, dfPuts)
            
            # Add results to df
            resultsDF.loc[len(resultsDF)] = {
                'target': target,
                'callsValue': callsValue,
                'putsValue': putsValue
            }
        
        # Save results to CSV
        # Converts df to CSV
        outputPath = os.path.join(outputDir, f'{mappingName}.csv')
        resultsDF.to_csv(outputPath, index=False)
        print(f"Saved results for {mappingName} to {outputPath}")

if __name__ == "__main__":
    processAllDatasets()