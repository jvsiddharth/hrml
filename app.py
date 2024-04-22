from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

# Load sample dataset
data = pd.read_csv('sample_dataset_with_probabilities.csv')

# Define months
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

@app.route('/')
def home():
    # Extract unique departments from the dataset
    departments = data['Department'].unique().tolist()
    employees = data.to_dict(orient='records')
    return render_template('index.html', employees=employees, departments=departments)

@app.route('/get-employee-details/<int:id>')
def get_employee_details(id):
    employee = data.iloc[id].to_dict()
    return jsonify(employee)

@app.route('/performance-graph', methods=['POST'])
def performance_graph():
    try:
        department = request.form['department']
        employee_id = int(request.form['employee_id'])

        if department == "":
            employee_data = data.iloc[employee_id]
        else:
            filtered_data = data[data['Department'] == department]
            if employee_id >= len(filtered_data):
                return "Employee index out of bounds for the selected department."
            employee_data = filtered_data.iloc[employee_id]
        
        print("Employee data:", employee_data)


        if employee_data.empty or employee_data is None:
            # Handle the case where employee_data is None or an empty DataFrame
            return "No data available for this employee."

        # Extract performance shifts for each month
        performance_shifts = [employee_data[f'Performance_Score_{month}'] for month in months]

        # Extract promotion probabilities for each month
        promotion_probabilities = [employee_data[f'Promotion_Probability_{month}'] for month in months]

        # Extract firing probabilities for each month
        firing_probabilities = [employee_data[f'Firing_Probability_{month}'] for month in months]

        # Extract leaving probabilities for each month
        leaving_probabilities = [employee_data[f'Leaving_Probability_{month}'] for month in months]

        # Calculate average performance shift
        avg_performance_shift = sum(performance_shifts) / len(performance_shifts)

        # Calculate average probabilities
        avg_promotion_probability = sum(promotion_probabilities) / len(promotion_probabilities)
        avg_firing_probability = sum(firing_probabilities) / len(firing_probabilities)
        avg_leaving_probability = sum(leaving_probabilities) / len(leaving_probabilities)

        # Create a plotly graph object
        performance_graph = go.Figure()
        performance_graph.add_trace(go.Scatter(x=months, y=performance_shifts, mode='lines+markers', name='Performance Shifts'))
        performance_graph.add_trace(go.Scatter(x=months, y=promotion_probabilities, mode='lines', name='Promotion Probabilities'))
        performance_graph.add_trace(go.Scatter(x=months, y=firing_probabilities, mode='lines', name='Firing Probabilities'))
        performance_graph.add_trace(go.Scatter(x=months, y=leaving_probabilities, mode='lines', name='Leaving Probabilities'))

        # Update graph layout
        performance_graph.update_layout(title='Monthly Performance and Probabilities', xaxis_title='Month', yaxis_title='Value')

        # Convert the graph to HTML
        performance_graph_html = pio.to_html(performance_graph, full_html=False) or ''

        # Extract employee details
        employee_details = {
            'Name': employee_data['Name'],
            'Employee_ID': employee_data['Employee_ID'],
            'Avg_Performance_Shift': avg_performance_shift,
            'Avg_Promotion_Probability': avg_promotion_probability,
            'Avg_Firing_Probability': avg_firing_probability,
            'Avg_Leaving_Probability': avg_leaving_probability
        }

        return render_template('performance_graph.html', performance_graph_html=performance_graph_html, employee_details=employee_details)

    except IndexError:
        # Handle IndexError here
        return "IndexError: Employee index out of bounds."

    except Exception as e:
        # Handle other exceptions
        return str(e)

