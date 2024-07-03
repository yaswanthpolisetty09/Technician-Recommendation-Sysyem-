import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from geopy.distance import geodesic

technicians_df = pd.read_csv('our_dataset.csv')

from django.shortcuts import render,HttpResponse
def home(request):
	return render(request,"location.html",{'d':[]})

def calculate_distance(user_lat, user_lon, tech_lat, tech_lon):
    user_location = (user_lat, user_lon)
    tech_location = (tech_lat, tech_lon)
    return geodesic(user_location, tech_location).kilometers

# Function to recommend t
def recommend_technicians(user_lat, user_lon, user_field, k=10):
    # Filter technicians based on the user's field
    filtered_technicians = technicians_df[technicians_df['Technician Field'] == user_field]
    
    # Calculate distances for each technician
    filtered_technicians['distance_km'] = filtered_technicians.apply(
        lambda row: calculate_distance(user_lat, user_lon, row['Latitude'], row['Longitude']), axis=1)
    
    if filtered_technicians.empty:
        return "No technicians found in the specified field."
    
    # Prepare data for KNN
    X = filtered_technicians[['Latitude', 'Longitude', 'Skill Rating']]  # Include Skill Rating
    
    # Fit KNN model
    knn = NearestNeighbors(n_neighbors=k, metric='euclidean')
    knn.fit(X)
    
    # Find k-nearest neighbors
    user_data = [[user_lat, user_lon, 5.0]]  # Assuming the user has a fixed skill rating of 5.0 (You can adjust this according to your system)
    _, indices = knn.kneighbors(user_data)
    
    # Get recommended technicians
    recommended_technicians = filtered_technicians.iloc[indices[0]]
    
    return recommended_technicians[['Technician Name', 'Technician Field', 'Technician Location', 'Latitude', 'Longitude', 'distance_km', 'Phone Number','Skill Rating']]  # Include Skill Rating

def find_technician(request):
    if request.method=="POST":
     d=recommend_technicians(10.963521,79.38609,request.POST.get('fields'))
     l=[]
     for i in range(len(d)):
      r=[]
      r.append(list(d['Technician Name'])[i])
      r.append(list(d['Technician Field'])[i])
      r.append(list(d['Technician Location'])[i])
      r.append(list(d['Latitude'])[i])
      r.append(list(d['Longitude'])[i])
      r.append(list(d['distance_km'])[i])
      r.append(list(d['Phone Number'])[i])
      r.append(list(d['Skill Rating'])[i])
      l.append(r)
     return render(request,"location.html",{'d':l})
     		
# Create your views here.
