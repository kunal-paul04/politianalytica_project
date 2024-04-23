from django.shortcuts import render
from .excelsheet import get_excel_data
import pandas as pd
from django.shortcuts import render
from django.conf import settings
import os

def contesting_parties_view(request):
    data = get_excel_data()
    for row in data:
        ls_percentage = (row[4] / 543) * 100  # Calculate the percentage
        row.append(ls_percentage)  # Append the percentage to the row
        rs_percentage = (row[5] / 245) * 100  # Calculate the percentage
        row.append(rs_percentage)  # Append the percentage to the row
    return render(request, 'contesting_parties.html', {'data': data})

def manifesto_view(request, party_name):
    # Construct the file path to the Excel file in the media folder
    file_path = os.path.join(settings.MEDIA_ROOT, 'data.xlsx')
    # Load the Excel file
    try:
        df = pd.read_excel(file_path, sheet_name=party_name)
    except Exception as e:
        # Handle the case where the specified sheet name doesn't exist
        return render(request, 'error.html', {'error_message': f"Sheet '{party_name}' not found in the Excel file."})
    # Convert DataFrame to list of dictionaries for easy access in the template
    data = df.to_dict(orient='records')
    print(data)
    # Pass party name and data to the template
    return render(request, 'manifesto.html', {'party_name': party_name, 'data': data})