import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from events.forms import FinalOrderForm
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
        user.save()
        return user


class PlaceModelTests(TempMediaTestCase):
    def test_save_recalculates_busy_and_free_places(self):
        event = self.create_event()
        user = self.create_user()
        place = Place.objects.create(
            place_name="Group 1",
            place_event=event,
            amount=2,
            active=True,
        )

        self.assertEqual(place.busy, 0)
        self.assertEqual(place.free, 2)

        Order.objects.create(order_event=event, order_user=user, order_place=place)
        place.save()
        place.refresh_from_db()

        self.assertEqual(place.busy, 1)
        self.assertEqual(place.free, 1)


class FinalOrderFormTests(TempMediaTestCase):
    def setUp(self):
        self.event = self.create_event()
        self.user = self.create_user()
        self.order = Order.objects.create(
            order_event=self.event,
            order_user=self.user,
            price=self.event.price,
        )

    def test_filters_merch_by_active_event(self):
        active_merch = Merch.objects.create(
            merch_name="T-shirt",
            merch_event=self.event,
            size="M",
            active=True,
        )
        Merch.objects.create(
            merch_name="Inactive",
            merch_event=self.event,
            size="L",
            active=False,
        )
        other_event = self.create_event(event_name="Other ride", active=False)
        Merch.objects.create(
            merch_name="Other",
            merch_event=other_event,
            size="S",
            active=True,
        )

        form = FinalOrderForm(event=self.event, order=self.order)

        self.assertQuerySetEqual(
            form.fields["order_merch"].queryset,
            [active_merch],
            transform=lambda item: item,
        )

    def test_base_price_filters_available_non_balakhna_places(self):
        available = Place.objects.create(
            place_name="Group 1",
            place_event=self.event,
            amount=3,
            active=True,
        )
        Place.objects.create(
            place_name="\u0411\u0430\u043b\u0430\u0445\u043d\u0430 1",
            place_event=self.event,
            amount=3,
            active=True,
        )
        Place.objects.create(
            place_name="Full group",
            place_event=self.event,
            amount=0,
            active=True,
        )
        Place.objects.create(
            place_name="Inactive group",
            place_event=self.event,
            amount=3,
            active=False,
        )

        form = FinalOrderForm(event=self.event, order=self.order)

        self.assertQuerySetEqual(
            form.fields["order_place"].queryset,
            [available],
            transform=lambda item: item,
        )

    def test_reduced_price_filters_only_balakhna_places(self):
        self.order.price = self.event.price - self.event.addition_price
        self.order.save()
        balakhna = Place.objects.create(
            place_name="\u0411\u0430\u043b\u0430\u0445\u043d\u0430 1",
            place_event=self.event,
            amount=3,
            active=True,
        )
        Place.objects.create(
            place_name="Group 1",
            place_event=self.event,
            amount=3,
            active=True,
        )

        form = FinalOrderForm(event=self.event, order=self.order)

        self.assertQuerySetEqual(
            form.fields["order_place"].queryset,
            [balakhna],
            transform=lambda item: item,
        )
