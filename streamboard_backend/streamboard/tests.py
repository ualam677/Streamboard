from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from streamboard.models import Streamboard
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now, timedelta
import json
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from PIL import Image

User = get_user_model()


def get_temporary_image():
    image = Image.new("RGB", (100, 100), color=(255, 0, 0))
    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file, format='JPEG')
    tmp_file.seek(0)
    return SimpleUploadedFile(name='test.jpg', content=tmp_file.read(), content_type='image/jpeg')


class StreamboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        refresh = RefreshToken.for_user(self.user)
        self.auth_headers = {
            'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'
        }

    def test_create_streamboard(self):
        image_file = get_temporary_image()
        data = {
            'title': 'Board 1',
            'layout_json': '{"a": 1}',
            'background_image': image_file
        }
        response = self.client.post(
            '/api/streamboard/',
            data,
            format='multipart',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 201)

    def test_list_user_streamboards(self):
        Streamboard.objects.create(
            user=self.user, title='My Board', layout_json={"x": 1})
        response = self.client.get(
            '/api/streamboard/list/', **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_streamboard_detail(self):
        board = Streamboard.objects.create(
            user=self.user, title='Detail View Test', layout_json={"x": 1})
        url = f'/api/streamboard/{board.id}/retrieve/'
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Detail View Test')

    def test_latest_streamboard(self):
        Streamboard.objects.create(user=self.user, title='Latest', last_view=now(
        ) - timedelta(days=1), layout_json={"x": 1})
        response = self.client.get(
            '/api/streamboard/latest/', **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Latest')

    def test_update_streamboard(self):
        board = Streamboard.objects.create(
            user=self.user, title='Old Title', layout_json={"x": 1})
        url = f'/api/streamboard/{board.id}/'
        data = {'title': 'New Title'}
        response = self.client.patch(url, json.dumps(
            data), content_type='application/json', **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'New Title')

    def test_recent_viewed_streamboards(self):
        Streamboard.objects.create(user=self.user, title='One', layout_json={
                                   "x": 1}, last_view=now() - timedelta(days=3))
        Streamboard.objects.create(user=self.user, title='Two', layout_json={
                                   "x": 1}, last_view=now() - timedelta(days=2))
        Streamboard.objects.create(user=self.user, title='Three', layout_json={
                                   "x": 1}, last_view=now() - timedelta(days=1))
        Streamboard.objects.create(user=self.user, title='Four', layout_json={
                                   "x": 1}, last_view=now())

        response = self.client.get(
            '/api/streamboard/recent-viewed/', **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
