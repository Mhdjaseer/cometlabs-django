from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework import status
from .serializers import LoginSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Question,TestCase
from .serializers import QuestionSerializer,TestCaseSerializer
import requests

class SignupView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Encrypt the password before saving the user
        password = request.data.get('password')
        serializer.validated_data['password'] = make_password(password)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Generate JWT access token and refresh token
        user = serializer.instance
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'email': user.email, 'access_token': access_token}, status=status.HTTP_201_CREATED, headers=headers)



class LoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = UserProfile.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = TokenObtainPairSerializer().get_token(user)
            access_token = str(refresh.access_token)

            # Set the user's role in the request object
            request.is_admin = user.role == 'admin'

            return Response({'email': user.email, 'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class TestCaseListCreateView(generics.ListCreateAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

class TestCaseRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer



class SolutionCheckView(APIView):
    SPHERE_ENGINE_ENDPOINT = "https://<customer_id>.problems.sphere-engine.com/api/v4/test"
    ACCESS_TOKEN = "<access_token>"

    def post(self, request, format=None):
        question_id = request.data.get('question_id')
        user_solution = request.data.get('solution')

        # Make a request to the Sphere Engine API to check the solution
        response = self.check_solution_with_sphere_engine(question_id, user_solution)

        # Process the response and determine the solution status
        solution_status = self.get_solution_status(response)

        return Response({'status': solution_status}, status=status.HTTP_200_OK)

    def check_solution_with_sphere_engine(self, question_id, user_solution):
        # Make the necessary HTTP request to the Sphere Engine API for solution checking
        url = f"{self.SPHERE_ENGINE_ENDPOINT}?access_token={self.ACCESS_TOKEN}"

        # Prepare the payload with the question ID and user solution
        payload = {
            'question_id': question_id,
            'solution': user_solution,
        }

        # Send the POST request to the Sphere Engine API
        response = requests.post(url, json=payload)

        return response

    def get_solution_status(self, response):
        # Process the response from the Sphere Engine API and determine the solution status
        # Extract the relevant information from the response and return the status accordingly
        # You can customize this logic based on the structure of the Sphere Engine API response

        # Example logic to determine the solution status based on the response
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('result') == 'success':
                return 'success'
            else:
                return 'wrong'
        else:
            return 'error'