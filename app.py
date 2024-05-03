from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

# Load sample dataset with employee engagement
engagement_data = pd.read_csv('sample_dataset_with_engagement.csv')
performance_data = pd.read_csv('sample_dataset_with_probabilities.csv')

# Define months
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

@app.route('/employee-details', methods=['POST'])
def employee_details():
    try:
        employee_id = int(request.form['employee_id'])

        # Retrieve employee details from engagement data based on employee ID
        employee_details = engagement_data.loc[engagement_data['Employee_ID'] == employee_id].to_dict(orient='records')
        if not employee_details:
            return "Employee not found."

        # Extracting employee details from the first record (assuming unique employee IDs)
        employee_details = employee_details[0]

        # Example: Assuming these are the columns in the engagement dataset
        name = employee_details['Name']
        department = employee_details['Department']
        # You can extract more details as needed

        return render_template('index.html', name=name, department=department)
    
    except Exception as e:
        return str(e)
    
@app.route('/')
def home():
    # Extract unique departments from the dataset
    departments = engagement_data['Department'].unique().tolist()
    employees = engagement_data.to_dict(orient='records')
    # Pass an empty dictionary or a default value for employee_details
    default_employee_details = {'Name': 'N/A', 'Employee_ID': 'N/A'}
    return render_template('index.html', employees=employees, departments=departments, employee_details=default_employee_details)

@app.route('/performance-graph', methods=['POST'])
def performance_graph():
    try:
        department = request.form['department']
        employee_id = int(request.form['employee_id'])

        if department == "":
            employee_engagement_data = engagement_data.iloc[employee_id]
            employee_performance_data = performance_data.iloc[employee_id]
        else:
            filtered_engagement_data = engagement_data[engagement_data['Department'] == department]
            filtered_performance_data = performance_data[performance_data['Department'] == department]
            if employee_id >= len(filtered_engagement_data) or employee_id >= len(filtered_performance_data):
                return "Employee index out of bounds for the selected department."
            employee_engagement_data = filtered_engagement_data.iloc[employee_id]
            employee_performance_data = filtered_performance_data.iloc[employee_id]

        if employee_engagement_data.empty or employee_engagement_data is None:
            # Handle the case where employee_data is None or an empty DataFrame
            return "No data available for this employee."

        # Extract employee engagement for each month
        employee_engagement = [employee_engagement_data[f'Employee_Engagement_{month}'] for month in months]
        # Extract performance shifts for each month
        performance_shifts = [employee_performance_data[f'Performance_Score_{month}'] for month in months]
        # Extract promotion probabilities for each month
        promotion_probabilities = [employee_performance_data[f'Promotion_Probability_{month}'] for month in months]
        # Extract firing probabilities for each month
        firing_probabilities = [employee_performance_data[f'Firing_Probability_{month}'] for month in months]
        # Extract leaving probabilities for each month
        leaving_probabilities = [employee_performance_data[f'Leaving_Probability_{month}'] for month in months]

        # Calculate average employee engagement
        avg_employee_engagement = sum(employee_engagement) / len(employee_engagement)
        # Calculate average performance shift
        avg_performance_shift = sum(performance_shifts) / len(performance_shifts)
        # Calculate average probabilities
        avg_promotion_probability = sum(promotion_probabilities) / len(promotion_probabilities)
        avg_firing_probability = sum(firing_probabilities) / len(firing_probabilities)
        avg_leaving_probability = sum(leaving_probabilities) / len(leaving_probabilities)

        # Create a plotly graph object for engagement
        engagement_graph = go.Figure()
        engagement_graph.add_trace(go.Scatter(x=months, y=employee_engagement, mode='lines+markers', name='Employee Engagement'))
        engagement_graph.update_layout(title='Monthly Employee Engagement', xaxis_title='Month', yaxis_title='Engagement')
        engagement_graph_html = pio.to_html(engagement_graph, full_html=False) or ''

        # Create a plotly graph object for performance
        performance_graph = go.Figure()
        performance_graph.add_trace(go.Scatter(x=months, y=performance_shifts, mode='lines+markers', name='Performance Shifts'))
        performance_graph.add_trace(go.Scatter(x=months, y=promotion_probabilities, mode='lines', name='Promotion Probabilities'))
        performance_graph.add_trace(go.Scatter(x=months, y=firing_probabilities, mode='lines', name='Firing Probabilities'))
        performance_graph.add_trace(go.Scatter(x=months, y=leaving_probabilities, mode='lines', name='Leaving Probabilities'))
        performance_graph.update_layout(title='Monthly Performance and Probabilities', xaxis_title='Month', yaxis_title='Value')
        performance_graph_html = pio.to_html(performance_graph, full_html=False) or ''

        # Extract employee details
        employee_details = {
            'Name': employee_engagement_data['Name'],
            'Employee_ID': employee_engagement_data['Employee_ID'],
            'Avg_Employee_Engagement': avg_employee_engagement,
            'Avg_Performance_Shift': avg_performance_shift,
            'Avg_Promotion_Probability': avg_promotion_probability,
            'Avg_Firing_Probability': avg_firing_probability,
            'Avg_Leaving_Probability': avg_leaving_probability
        }

        return render_template('dashboard.html', engagement_graph_html=engagement_graph_html, performance_graph_html=performance_graph_html, employee_details=employee_details)

    except IndexError:
        # Handle IndexError here
        return "IndexError: Employee index out of bounds."

    except Exception as e:
        # Handle other exceptions
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
