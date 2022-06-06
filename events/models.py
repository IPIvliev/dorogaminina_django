from django.db import models
from home.models import User

class Event(models.Model):
  event_name = models.CharField(max_length=100)
  start_date = models.DateField()
  price = models.IntegerField(default=0)
  addition_price = models.IntegerField(default=0)
  description_template = models.BooleanField('Блок описания', default=False)
  statistic_template = models.BooleanField('Блок статистики', default=False)
  about_template = models.BooleanField('Блок О проекте', default=False)
  team_template = models.BooleanField('Блок команды', default=False)
  history_template = models.BooleanField('Блок исторической справки', default=False)
  cost_template = models.BooleanField('Блок стоимости', default=False)
  feedback_template = models.BooleanField('Блок отзывов', default=False)
  blog_template = models.BooleanField('Блок новостей', default=False)
  registration_template = models.BooleanField('Блок регистрации', default=False)
  gallery_template = models.BooleanField('Блок галереи', default=False)
  partners_template = models.BooleanField('Блок партнёров', default=False)
  active = models.BooleanField(default=False)

  class Meta:
      verbose_name = 'Мероприятие'
      verbose_name_plural = 'Мероприятия'

  def __str__(self):
    return u'{0}'.format(self.event_name)

class Partner(models.Model):
  partner_name = models.CharField('Наименование', max_length=100)
  partner_logo = models.FileField('Логотип', upload_to='uploads/partners/')
  partner_link = models.CharField('Ссылка', max_length=100, null=True, blank=True)
  partner_order = models.IntegerField('Порядковый номер', default=0)
  active = models.BooleanField(default=False)

  class Meta:
      verbose_name = 'Партнёр'
      verbose_name_plural = 'Партнёры'

class Place(models.Model):
  place_name = models.CharField(max_length=100)
  place_event = models.ForeignKey(Event, on_delete=models.CASCADE)
  amount = models.IntegerField('Всего мест', default=0)
  busy = models.IntegerField('Занято мест', default=0)
  free = models.IntegerField('Свободно мест', default=0)
  active = models.BooleanField(default=False)

  def save(self, *args, **kwargs):
    self.busy = self.order_set.count()
    self.free = self.amount - self.busy
    super(Place, self).save(*args, **kwargs)

  class Meta:
      verbose_name = 'Звено'
      verbose_name_plural = 'Звенья'

  def __str__(self):
    return u'{0}'.format(self.place_name)

class Merch(models.Model):
  merch_name = models.CharField(max_length=100, null=True, blank=True)
  merch_event = models.ForeignKey(Event, on_delete=models.CASCADE)
  size = models.CharField(max_length=100, null=True, blank=True)
  merch_image = models.FileField(upload_to='uploads/merchs/', null=True, blank=True)
  active = models.BooleanField(default=False)

  class Meta:
      verbose_name = 'Футболка'
      verbose_name_plural = 'Футболки'

  def __str__(self):
    return u'{0}'.format(self.merch_name)

class Order(models.Model):
  order_event = models.ForeignKey(Event, on_delete=models.CASCADE)
  order_user = models.ForeignKey(User, on_delete=models.CASCADE)
  order_place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.PROTECT)
  order_merch = models.ForeignKey(Merch, null=True, blank=True, on_delete=models.PROTECT)
  price = models.IntegerField(default=0)
  comment = models.CharField(max_length=250, null=True, blank=True)
  active = models.BooleanField(default=False)

  class Meta:
      verbose_name = 'Оплата'
      verbose_name_plural = 'Оплаты'