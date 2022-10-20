# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import LazyMenuSerializer






import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

import json

from food_extractor.food_model import FoodModel
model = FoodModel("chambliss/distilbert-for-food-extraction")







class LazyMenuListApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated] #COMMENTED

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Todo.objects.filter(user = request.user.id)
        serializer = LazyMenuSerializer(todos, many=True)

        #return Response(serializer.data, status=status.HTTP_200_OK)


        list_received = request.GET['list_param']

        list_received = json.loads(list_received)

        input_array = list_received

        #input_array = ["Appetizers","Soup of the day","Baked fingerling potatoes (v)","Crispy fried cheese (v)","House Salad (v)","Salads","Caesar salad","Feta salad (v)","DINNER MENU","Restaurant Name","This is a printable dinner menu template from EDIT.org","Marinated salmon salad","Vegan Kale salad (v)","Pastas","Vegan lasagna (v)","Spaghetti pomodoro (v)","Macaroni carbonara","Farfale with shrimp and zucchini","Lunch: 12 PM-3 PM","Dinner: 5:30 PM - 10 PM","$20","$20","$20","$20","$20","$20","$20","$20","$20","$20","$20","$20","20","YOUR","LOGO","Specialties","Crispy chicken with mango sauce","Fresh grilled beef","Tofu butternut curry (v)","Poached eggs in avocado toasts (v)","Sides: choose from salad, french fried, sweet","potato fries, or rice","Desserts","Red fruits cheesecake","Tiramisu","Triple chocolate cake","Bowl of ice-cream","BOOKINGS (610) 888-1111","The above prices are subject to change","We adapt the menu to different allergies and","intolerances","$20","$20","$20","$20","$20","$20","$20","$20","1111 C St, San Diego, CA 92103","www.yourwebpagehere.com"]
        excluded_texts = ['california'"appetizers","soup","salad","beef","chicken","pork","lamb","entree","side","dish","bread","coffee","tea","wine","beer",
        "soft",
        "drink","cocktail",
        "martini","mixed","shots","liqueurs","non-alcoholic","mineral","water","juices",
        "appetizers",
        "salads",
        "pastas",
        "specialties",
        "desserts",
        "dessert",
        "starter",
        "starters",
        "main",
        "menu",
        "menu",
        "food",
        "dessert",
        "desserts",
        "entrees",
        "vegetables", "dinner menu" ,'california']

        text = f''

        for inp in input_array:
            text += f'{inp.lower()} '

        text = text[:-1]

        print(text)

        output_text = model.extract_foods(text)

        print("---**********----")
        print(output_text)

        parsed_items = []
        for out in output_text:
            ingredients = out['Ingredient']
            for ing in ingredients:
                text = ing['text']
                
                array_text = text.split(" ")
                
                for input in input_array:            
                    for ingredient2 in array_text:
                        if ingredient2 in input.lower() and ingredient2 not in excluded_texts and any(char.isdigit() for char in input) == False:
                            parsed_items.append(input)

        parsed_items = list(dict.fromkeys(parsed_items))

        data = {'Input': input_array, 'Output': parsed_items}
        print("------")

        #print(request.query_params['list_param']) # http://127.0.0.1:8000/todos/api?list_param=[%22hola%22,%20%22hey%22]
        #print(parsed_items)

        return Response({
            'food': data
        }, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = LazyMenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)