from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import pickle

model = pickle.load(open("c1_flight_rf.pkl", "rb"))

def index(request):
    return render(request, "index.html")

def predict(request):
    if request.method == "POST":
        date_dep = request.POST["Dep_Time"]
        journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
        dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        date_arr = request.POST["Arrival_Time"]
        arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        Duration_hour = abs(arrival_hour - dep_hour)
        Duration_mins = abs(arrival_min - dep_min)

        Total_Stops = int(request.POST["stops"])

        airline = request.POST['airline']
        if airline == 'Jet Airways':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 1
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline == 'IndiGo':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 1
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline == 'Air India':
            Airline_AirIndia = 1
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline == 'Multiple carriers':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 1
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline == 'SpiceJet':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 1
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline == 'Vistara':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 1
            Airline_Other = 0
        elif airline == 'GoAir':
            Airline_AirIndia = 0
            Airline_GoAir = 1
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
        else:
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 1

        Source = request.POST["Source"]
        if Source == 'Delhi':
            Source_Delhi = 1
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0
        elif Source == 'Kolkata':
            Source_Delhi = 0
            Source_Kolkata = 1
            Source_Mumbai = 0
            Source_Chennai = 0
        elif Source == 'Mumbai':
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 1
            Source_Chennai = 0
        elif Source == 'Chennai':
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 1
        else:
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0

        Destination = request.POST["Destination"]
        if Destination == 'Cochin':
            Destination_Cochin = 1
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
        elif Destination == 'Delhi':
            Destination_Cochin = 0
            Destination_Delhi = 1
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
        elif Destination == 'Hyderabad':
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 1
            Destination_Kolkata = 0
        elif Destination == 'Kolkata':
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 1
        else:
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0

        prediction = model.predict([[
            Total_Stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min,
            Duration_hour,
            Duration_mins,
            Airline_AirIndia,
            Airline_GoAir,
            Airline_IndiGo,
            Airline_JetAirways,
            Airline_MultipleCarriers,
            Airline_Other,
            Airline_SpiceJet,
            Airline_Vistara,
            Source_Chennai,
            Source_Kolkata,
            Source_Mumbai,
            Destination_Cochin,
            Destination_Delhi,
            Destination_Hyderabad,
            Destination_Kolkata,
        ]])

        output = round(prediction[0], 2)

        return render(request, 'index.html', {'prediction_text': "Your Flight price is Rs. {}".format(output)})

    return render(request, "index.html")
