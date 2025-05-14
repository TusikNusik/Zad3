'''from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from trasy.models import BackgroundImage, Route, Point


class WebAuthTests(TestCase):

    def setUpTestData(cls):
        self.user = User.objects.create_user(username="maslo")
        self.image = BackgroundImage.objects.create(name="map", image="temp.png")
        self.route = PointList.objects.create(user=self.user, backgroundImage=self.image, name="PointList1")

    def test_login_required_redirect(self):
        resp = self.client.get(reverse("routes:route_list"))
        self.assertRedirects(resp, "/accounts/login/?next=/")

    def test_user_sees_only_own_routes(self):
        Route.objects.create(user=self.other, background=self.bg, name="Cudza")
        Route.objects.create(user=self.user, background=self.bg, name="Moja")

        self.client.login(username="john", password="pwd123")
        resp = self.client.get(reverse("routes:route_list"))
        self.assertContains(resp, "Moja")
        self.assertNotContains(resp, "Cudza")

    def test_add_and_delete_point(self):
        self.client.login(username="john", password="pwd123")
        route = Route.objects.create(user=self.user, background=self.bg, name="Test")

        # dodaj punkt przez formularz POST
        add_url = reverse("routes:add_point", args=[route.pk])
        resp = self.client.post(add_url, {"x": 33, "y": 44})
        self.assertRedirects(resp, reverse("routes:route_detail", args=[route.pk]))
        self.assertEqual(route.points.count(), 1)

        # usuń punkt
        point = route.points.first()
        del_url = reverse("routes:point_delete", args=[point.pk])
        resp = self.client.post(del_url)
        self.assertRedirects(resp, reverse("routes:route_detail", args=[route.pk]))
        self.assertEqual(route.points.count(), 0)

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from trasy.models import Point, PointList, BackgroundImage

class ViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testView", password="tus1234")
        cls.image = BackgroundImage.objects.create(name="map", image="temp.png")
        cls.PointList = PointList.objects.create(user=cls.user, backgroundImage=cls.image, name="PointList1")
        cls.point = Point.objects.create(x=10, y=20, included=False)
        cls.PointList.points.add(cls.point)

    def test_login_checked(self):
        
 '''
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from trasy.models import Point, PointList, BackgroundImage

class WebInterfaceTests(TestCase):

    #Setup klienta i jego obiektów.
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='maslo', password='qwerty123')
        self.background = BackgroundImage.objects.create(name="testImage", image="temp.png")
        self.pointList = PointList.objects.create(user=self.user, name="testList", backgroundImage=self.background)
        self.point = Point.objects.create(x=10, y=20, included=True)
        self.pointList.points.add(self.point)

    # Test sprawdzający, czy po zalogowaniu user dalej ma otrzymane wartości.
    def test_user_has_set_values(self):
        self.client.login(username='maslo', password='qwerty123')
        self.assertTrue(PointList.objects.filter(name='testList').exists())
        self.assertTrue(BackgroundImage.objects.filter(name='testImage').exists())
        self.assertEqual(self.pointList.points.get(id=1).x, 10)

    # Dodawanie punktu przez POST i weryfikacja poprawności.
    def test_add_point_to_list(self):
        self.client.login(username='maslo', password='qwerty123')
        response = self.client.post(reverse('addPoint', args=[self.pointList.id]), {'addPoint': 'true', 'X-cord': '30', 'Y-cord': '40'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.pointList.points.count(), 2)

    # Zmienianie uwzględnienie punktu przez POST. (T->F->T) oraz sprawdzenie czy widok strony odzwierciedla zmianę w bazie.
    def test_exclude_points(self):
        self.client.login(username='maslo', password='qwerty123')
        response = self.client.post(reverse('addPoint', args=[self.pointList.id]), { 'save': 'true', f'{self.point.id}': 'excluded' })
        self.point.refresh_from_db()
        self.assertFalse(self.point.included)
        response2 = self.client.post(reverse('addPoint', args=[self.pointList.id]), { 'save': 'true', f'{self.point.id}': 'included' })
        self.point.refresh_from_db()
        self.assertTrue(self.point.included)
        response3 = self.client.get(reverse('addPoint', args=[self.pointList.id]))
        html = response3.content.decode('utf-8')
        expected_input = f'name="{self.point.id}" checked'
        self.assertIn(expected_input, html)

    # Sprawdzanie czy nowy user widzi listy innych użytkowników.
    def test_saved_projects_view_only_own_lists(self):
        other_user = User.objects.create_user(username='otheruser', password='qwerty123')
        other_list = PointList.objects.create(user=other_user, name="otherList", backgroundImage=self.background)
        self.client.login(username='maslo', password='qwerty123')
        response = self.client.get(reverse('savedProjects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testList")
        self.assertNotContains(response, "otherList")
        self.client.logout()
        self.client.login(username='otheruser', password='qwerty123')
        response = self.client.get(reverse('savedProjects'))
        self.assertContains(response, "otherList")
        self.assertNotContains(response, "testList")
    
    # Przekierowywanie do strony logowania, dla niezalogowanych użytkowników.
    def test_add_list_requires_login(self):
        response = self.client.get(reverse('savedProjects'))
        self.assertEqual(response.status_code, 302) 
        self.assertIn('/login?next=/', response.url)