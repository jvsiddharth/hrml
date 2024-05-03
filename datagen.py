import pandas as pd
import numpy as np
from faker import Faker

# Set random seed for reproducibility
np.random.seed(42)

# Initialize Faker generator with Indian locale
fake = Faker('en_IN')

# Define the number of employees
num_employees = 100

# Generate synthetic data for employee feedback attributes for each month
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Create an empty list to store dataframes for each month
dfs = []

for month in months:
    data = {
        'Employee_ID': range(1, num_employees + 1),
        'Name': [fake.name() for _ in range(num_employees)],
        'Department': np.random.choice(['Sales', 'Marketing', 'Engineering'], size=num_employees),
        'Team_Collaboration_' + month: np.random.randint(6, 11, size=num_employees),  # Team collaboration score on a scale of 1 to 10 (higher is better)
        'Work_Satisfaction_' + month: np.random.randint(6, 11, size=num_employees),  # Work satisfaction score on a scale of 1 to 10 (higher is better)
        'Manager_Relationship_' + month: np.random.randint(6, 11, size=num_employees),  # Manager relationship score on a scale of 1 to 10 (higher is better)
        'Training_Satisfaction_' + month: np.random.randint(6, 11, size=num_employees)  # Training satisfaction score on a scale of 1 to 10 (higher is better)
    }
    
    # Create DataFrame for the current month
    df_month = pd.DataFrame(data)
    
    # Append the dataframe to the list
    dfs.append(df_month)

# Concatenate dataframes for all months into a single dataframe
df = pd.concat(dfs, axis=1)

# Save the dataset to a CSV file
df.to_csv('sample_dataset.csv', index=False)

# Display the first few rows of the dataset
print(df.head())
