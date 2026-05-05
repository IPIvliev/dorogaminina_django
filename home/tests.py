import shutil
import tempfile
from unittest.mock import patch

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from events.models import Event, Merch, Order, Place
from home.models import User


def uploaded_file(name="file.txt"):
    return SimpleUploadedFile(name, b"test file content")


class TempMediaTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._media_root = tempfile.mkdtemp()
        cls._settings_override = override_settings(MEDIA_ROOT=cls._media_root)
        cls._settings_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        try:
            super().tearDownClass()
        finally:
            cls._settings_override.disable()
            shutil.rmtree(cls._media_root, ignore_errors=True)

    def create_event(self, **kwargs):
        defaults = {
            "event_name": "Test ride",
            "start_date": "2026-06-01",
            "price": 1500,
            "addition_price": 600,
            "agreement": uploaded_file("agreement.docx"),
            "position_1": uploaded_file("position-1.jpg"),
            "position_2": uploaded_file("position-2.jpg"),
            "active": True,
        }
        defaults.update(kwargs)
        return Event.objects.create(**defaults)

    def create_user(self, phone="+7(900) 000-0000"):
        user = User.objects.create(
            username="Ivan",
            lastname="Ivanov",
            middlename="Ivanovich",
            phone=phone,
            is_active=True,
        )
        user.set_password("secret")
        user.more = "secret"
        user.save()
        return user


class RegistrationFlowTests(TempMediaTestCase):
    @override_settings(PASSWORD_DELIVERY_METHOD="sms")
    @patch("home.password_delivery.SmsRuApi")
    def test_registration_creates_user_sends_sms_and_logs_in(self, sms_api):
        self.create_event()

        response = self.client.post(
            "/index.html",
            {
                "lastname": "Ivanov",
                "username": "Ivan",
                "middlename": "Ivanovich",
                "email": "ivan@example.com",
                "phone": "+7(900) 111-2233",
            },
        )

        user = User.objects.get(phone="+7(900) 111-2233")
        self.assertRedirects(response, "/profile.html", fetch_redirect_response=False)
        self.assertTrue(user.check_password(user.more))
        self.assertEqual(user.email, "ivan@example.com")
        self.assertEqual(self.client.session["_auth_user_id"], str(user.id))
        sms_api.return_value.send_one_sms.assert_called_once()

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_registration_can_send_password_by_email(self):
        self.create_event()

        response = self.client.post(
            "/index.html",
            {
                "lastname": "Ivanov",
                "username": "Ivan",
                "middlename": "Ivanovich",
                "email": "ivan@example.com",
                "phone": "+7(900) 111-2233",
            },
        )

        user = User.objects.get(phone="+7(900) 111-2233")
        self.assertRedirects(response, "/profile.html", fetch_redirect_response=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["ivan@example.com"])
        self.assertIn(user.more, mail.outbox[0].body)

    @patch("home.password_delivery.SmsRuApi")
    def test_registration_requires_email(self, sms_api):
        self.create_event()

        response = self.client.post(
            "/index.html",
            {
                "lastname": "Ivanov",
                "username": "Ivan",
                "middlename": "Ivanovich",
                "phone": "+7(900) 111-2233",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.context["registrationform"].errors)
        self.assertFalse(User.objects.filter(phone="+7(900) 111-2233").exists())
        sms_api.return_value.send_one_sms.assert_not_called()

    @patch("home.views.send_registration_password", side_effect=Exception("SMTP error"))
    def test_registration_rolls_back_user_when_password_delivery_fails(self, send_password):
        self.create_event()

        response = self.client.post(
            "/index.html",
            {
                "lastname": "Ivanov",
                "username": "Ivan",
                "middlename": "Ivanovich",
                "email": "ivan@example.com",
                "phone": "+7(900) 111-2233",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["registrationform"].non_field_errors())
        self.assertFalse(User.objects.filter(phone="+7(900) 111-2233").exists())
        send_password.assert_called_once()

    def test_login_accepts_phone_and_sms_password(self):
        self.create_event()
        user = self.create_user(phone="+7(900) 111-2233")

        response = self.client.post(
            "/login.html",
            {
                "phone": user.phone,
                "password": "secret",
            },
        )

        self.assertRedirects(response, "/profile.html", fetch_redirect_response=False)
        self.assertEqual(self.client.session["_auth_user_id"], str(user.id))


class ProfileTests(TempMediaTestCase):
    def setUp(self):
        self.event = self.create_event()
        self.user = self.create_user()
        self.client.force_login(self.user)

    def test_profile_creates_single_order_for_active_event(self):
        self.client.get("/profile.html")
        self.client.get("/profile.html")

        orders = Order.objects.filter(order_event=self.event, order_user=self.user)
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders.get().price, self.event.price)

    def test_delivery_query_sets_reduced_price_until_order_is_paid(self):
        self.client.get("/profile.html?delivery=true")

        order = Order.objects.get(order_event=self.event, order_user=self.user)
        self.assertEqual(order.price, self.event.price - self.event.addition_price)

    def test_paid_order_price_is_not_recalculated_from_delivery_query(self):
        order = Order.objects.create(
            order_event=self.event,
            order_user=self.user,
            price=111,
            active=True,
        )

        self.client.get("/profile.html?delivery=true")
        order.refresh_from_db()

        self.assertEqual(order.price, 111)

    def test_profile_post_rejects_place_from_another_event(self):
        order = Order.objects.create(
            order_event=self.event,
            order_user=self.user,
            price=self.event.price,
            active=True,
        )
        merch = Merch.objects.create(
            merch_name="T-shirt",
            merch_event=self.event,
            size="M",
            active=True,
        )
        other_event = self.create_event(event_name="Other ride", active=False)
        other_place = Place.objects.create(
            place_name="Other event group",
            place_event=other_event,
            amount=3,
            active=True,
        )

        self.client.post(
            "/profile.html",
            {
                "order_merch": merch.id,
                "order_place": other_place.id,
                "comment": "",
            },
        )
        order.refresh_from_db()

        self.assertIsNone(order.order_place)
        self.assertIsNone(order.order_merch)


class PaymentCallbackTests(TempMediaTestCase):
    def setUp(self):
        self.event = self.create_event()
        self.user = self.create_user()
        self.order = Order.objects.create(
            order_event=self.event,
            order_user=self.user,
            price=self.event.price,
            active=False,
        )

    def test_success_callback_activates_order(self):
        response = self.client.get(f"/robokassa/success?InvId={3000 + self.order.id}")

        self.order.refresh_from_db()
        self.assertTrue(self.order.active)
        self.assertRedirects(response, "/profile.html", fetch_redirect_response=False)

    def test_paid_callback_activates_order(self):
        response = self.client.post(f"/robokassa/paid", {"InvId": 3000 + self.order.id})

        self.order.refresh_from_db()
        self.assertTrue(self.order.active)
        self.assertEqual(response.content.decode(), f"OK{3000 + self.order.id}")
