from datetime import date, timedelta, datetime
from django.shortcuts import render
from rest_framework import viewsets,status
from .models import User, PatientInfo, Medication, Appointment
from .serializers import UserSerializer, PatientInfoSerializer, MedicationSerializer, AppointmentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view



from openai import OpenAI
import json


# Create your views here.
def dashboard(request):
    # Your logic to gather data for the dashboard goes here
    # For now, let's assume you have some dummy data
    data = {
        'user_count': 100,  # Example: Total number of users
        'active_users': 75,  # Example: Number of active users
        'inactive_users': 25,  # Example: Number of inactive users
        # Add more data as needed for your dashboard
    }
    return render(request, 'dashboard.html', {'data': data})


def home(request):
    return render(request, 'home.html')







class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ResponseGPT(viewsets.ModelViewSet):
    def response(self,request,*args,**kwargs):
        print(request)
        request=request.data
        client = OpenAI(api_key = "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")
        result = function_calling(client, request['message'])
        return Response({"result": result}, status=status.HTTP_200_OK)
        # return(request)
    
# class Conversation(viewsets.ModelViewSet):


class PatientInfoViewSet(viewsets.ModelViewSet):
    queryset = PatientInfo.objects.all()
    serializer_class = PatientInfoSerializer

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer



def get_user_info(curr_user_id:str="1234567890"):
    """Gets the information regarding a user from the User table in the database"""
    user = User.objects.filter(user_id = curr_user_id).values()
    user_list = list(user)
    return json.dumps(user_list)


def get_curr_appointments(curr_user_id:str="1234567890"):
    """
    Gets the schedule/appointments for the user for today from the Appointment table
    """
    appts = list(Appointment.objects.filter(patient_id=curr_user_id, date = date.today()).values())
    appts = list(map(str,appts))
    return json.dumps(appts)

def get_next_appointments(num_days:int,curr_user_id:str="1234567890"):
    """
    Takes in the number of days for which we want the user's schedule/appointments. Returns the schedule/appointments for the next num_days days for the user.
    """
    appts = []
    for i in range(num_days):
        temp = list(Appointment.objects.filter(patient_id=curr_user_id, date = date.today() + timedelta(days = i)).values())
        temp = list(map(str,temp))
        appts.append(temp)
    return json.dumps(appts)

def get_today_medicines(curr_user_id:str="1234567890"):
    """Gets today's medicinal plan or medications for a user from the Medication table"""
    meds = list(Medication.objects.filter(patient_id=curr_user_id, day = date.today().strftime('%A').lower()).values())
    meds = list(map(str,meds))
    return json.dumps(meds)

def get_next_days_medicines(num_days:int,curr_user_id:str="1234567890"):
    """
    Takes in the number of days for which we want the user's medicinal plan/medications. Returns the medicinal plan/medications for the next num_days days for the user.
    """
    meds = []
    for i in range(num_days):
        day = date.today() + timedelta(days=i)
        temp = list(Medication.objects.filter(patient_id=curr_user_id, day = day.strftime('%A').lower()).values())
        temp = list(map(str,temp))
        meds.append(temp)
    return json.dumps(meds)


def function_calling(client,message:str):
    """Function calling for accessing/adding data"""
    # Step 1: send the conversation and available functions to the model[
    messages = [{"role": "user", "content": message}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_user_info",
                "description": "Gets the information regarding a user from the User table in the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "curr_user_id": {
                            "type": "string",
                            "description": "User's unique 10 digit ID - its the primary key for our database",
                        },
                    },
                    "required": ["curr_user_id"],
                },
            },
        },

        {
            "type": "function",
            "function": {
                "name": "get_curr_appointments",
                "description": "Gets the schedule/appointments for the user for today from the Appointment table",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "curr_user_id": {
                            "type": "string",
                            "description": "User's unique 10 digit ID - its the primary key for our database",
                        },
                    },
                    "required": ["curr_user_id"],
                },
            },
        },

        {
            "type": "function",
            "function": {
                "name": "get_next_appointments",
                "description": "Takes in the user ID and number of days for which we want the user's schedule or appointments. Returns the schedule or appointments for the next num_days days for the user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "curr_user_id": {
                            "type": "string",
                            "description": "User's unique 10 digit ID - its the primary key for our database",
                        },

                        "num_days": {
                            "type":"integer",
                            "description": "Number of days for which we want the schedule/appointments",
                        }
                    },
                    "required": ["curr_user_id","num_days"],
                },
            },
        },

        {
            "type": "function",
            "function": {
                "name": "get_today_medicines",
                "description": "Gets today's medicinal plan or medications for a user from the Medication table",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "curr_user_id": {
                            "type": "string",
                            "description": "User's unique 10 digit ID - its the primary key for our database",
                        },
                    },
                    "required": ["curr_user_id"],
                },
            },
        },

        {
            "type": "function",
            "function": {
                "name": "get_next_days_medicines",
                "description": "Takes in user ID and the number of days for which we want the user's medicinal plan or medications. Returns the medicinal plan or medications for the next num_days days for the user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "curr_user_id": {
                            "type": "string",
                            "description": "User's unique 10 digit ID - its the primary key for our database",
                        },

                        "num_days": {
                            "type":"integer",
                            "description": "Number of days for which we want the medicinal plan",
                        }
                    },
                    "required": ["curr_user_id","num_days"],
                },
            },
        }

    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_user_info": get_user_info,
            "get_curr_appointments": get_curr_appointments,
            "get_next_appointments": get_next_appointments,
            "get_today_medicines": get_today_medicines,
            "get_next_days_medicines":get_next_days_medicines,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            print(function_to_call)
            function_args = json.loads(tool_call.function.arguments)
            function_response = ""
            print(str(function_to_call))
            if(str(function_to_call).split()[1] == "get_user_info" or str(function_to_call).split()[1] == "get_curr_appointments" or str(function_to_call).split()[1] == "get_today_medicines"):
                function_response = function_to_call(
                    curr_user_id=function_args.get("curr_user_id"),
                    )
            # elif(function_to_call == "basic_interaction"):
            #     function_response = function_to_call(
            #         input = function_args.get("input"),
            #     )
                
            elif(str(function_to_call).split()[1] == "get_next_appointments" or str(function_to_call).split()[1] == "get_next_days_medicines"):
                function_response = function_to_call(
                    curr_user_id=function_args.get("curr_user_id"),
                    num_days = function_args.get("num_days"),
                )
                    
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content.strip()






def build_schedule(request):

    
    try:


        user_id = request.data.get('user_id', None)
        
        if not user_id:
            return Response({'error': 'User ID is required'}, status=400)

        # Query appointments based on user ID
        appointments = Appointment.objects.filter(patient_id=user_id)
        
        # Serialize the appointments data
        serializer = AppointmentSerializer(appointments, many=True)
        
        return Response(serializer.data, status=200)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    


