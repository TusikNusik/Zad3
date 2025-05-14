from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from trasy.models import PointList, Point, BackgroundImage
from api import views, urls

class RoutePointAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='apiUser', password='qwerty123')
        self.token = Token.objects.create(user=self.user)
        self.background = BackgroundImage.objects.create(name="testImage", image="temp.png")
        self.pointList = PointList.objects.create(user=self.user, name="testList", backgroundImage=self.background)
        self.point = Point.objects.create(x=10, y=20, included=True)
        self.pointList.points.add(self.point)

        self.other_user = User.objects.create_user(username='other', password='qwerty123')
        self.other_route = PointList.objects.create(user=self.other_user, name="otherList", backgroundImage=self.background)
        #self.pointList = PointList.objects.create(user=self.user, name="testList", backgroundImage=self.background)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_authentication_required(self):
        self.client.credentials()  # Usunięcie tokenu
        url = reverse('point-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
    
    # Sprawdzenie POST oraz assertJSON
    def test_create_route_and_return_json(self):
        url = reverse('point-list-create')
        data = {'name': 'Moja trasa', 'backgroundImage': 1, 'user': 1, 'points': [1]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'id': response.data['id'], 'name': 'Moja trasa',  'user': 1, 'backgroundImage': 1, 'points': [1]}
        )
    
    # Próbujemy nieskutecznie dostać pointListę usera: 'other_user'
    def test_access_to_other_user_list(self):
        url = reverse('pointlist-detail-delete', kwargs={'pk': self.other_route.id})
        response = self.client.delete(url)
        self.assertIn(response.status_code, [403, 404])

    # Otrzymywanie list przez get, GET z ('point-list-create') prowadzi do widoku, który wyświetla aktualne listy.
    def test_get_routes_and_delete(self):
        trasa1 = PointList.objects.create(name='Trasa1', user=self.user, backgroundImage=self.background)
        PointList.objects.create(name='Trasa2', user=self.user, backgroundImage=self.background)

        url = reverse('point-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3) # Ponieważ wcześniej dodaliśmy w inicjacji listę początkową.

        # Usuwanie trasy1.
        delete_url = reverse('pointlist-detail-delete', kwargs={'pk': trasa1.id})
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, 204) 

        response_after_delete = self.client.get(url)
        self.assertEqual(response_after_delete.status_code, 200)
        self.assertEqual(len(response_after_delete.data), 2)
    
    def test_input_validation(self):
        url = reverse('point-list-create')
        data = {'name': ''}  # Błędna wartość
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)

    
    def test_add_and_delete_point(self):
        route = PointList.objects.create(name='pointsFinally', user=self.user, backgroundImage=self.background)

        # Dodanie punktu
        create_url = reverse('point-create', kwargs={'route_id': route.id})
        point_data = {'x': 30, 'y': 20}
        create_response = self.client.post(create_url, point_data, format='json')
        self.assertEqual(create_response.status_code, 201)
        point_id = create_response.data['id']

        # Usunięcie punktu
        delete_url = reverse('point-delete', kwargs={'route_id': route.id, 'point_id': point_id})
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, 204)
        