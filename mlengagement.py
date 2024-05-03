import pandas as pd

# Load the sample dataset
df = pd.read_csv('sample_dataset.csv')

# Define the list of months
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Function to calculate employee engagement for a specific month
def calculate_employee_engagement(row, month):
    # Calculate employee engagement based on specified feedback attributes for the given month
    team_collaboration = row['Team_Collaboration_' + month]
    work_satisfaction = row['Work_Satisfaction_' + month]
    manager_relationship = row['Manager_Relationship_' + month]
    training_satisfaction = row['Training_Satisfaction_' + month]
    # Define your engagement calculation here
    # For example, you can take an average of the feedback attributes
    employee_engagement = (team_collaboration + work_satisfaction + manager_relationship + training_satisfaction) / 4
    return employee_engagement

# Calculate employee engagement for each employee for each month
for month in months:
    df['Employee_Engagement_' + month] = df.apply(lambda row: calculate_employee_engagement(row, month), axis=1)

# Save the updated dataset with calculated employee engagement
df.to_csv('sample_dataset_with_engagement.csv', index=False)

# Display the first few rows of the updated dataset
print(df.head())
