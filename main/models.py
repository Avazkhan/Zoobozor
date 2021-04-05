from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True)
    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Nomi')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Tartibi')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Bosh bo`lim')

class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):
    objects = SuperRubricManager()
    
    def __str__(self):
        return self.name
    
    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Bosh bo`lim'
        verbose_name_plural = 'Bosh bo`limlar'

class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)

class SubRubric(Rubric):
    objects = SubRubricManager()
    
    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)
    
    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Bo`limcha'
        verbose_name_plural = 'Bo`limchalar'

class Bb(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Bo`lim')
    title = models.CharField(max_length=40, verbose_name='Jonivor')
    content = models.TextField(verbose_name='Ma`lumot')
    price = models.FloatField(default=0, verbose_name='Narxi')
    contacts = models.TextField(verbose_name='Aloqa')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Fotosurat')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='E`lon muallifi')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Ro`yxatga qo`shishish kerakmi?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Chop etilgan')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'E`lonlar'
        verbose_name = 'E`lon'
        ordering = ['-created_at']

class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='E`lon')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Fotosurat')

    class Meta:
        verbose_name_plural = 'Qo`shimcha fotosuratlar'
        verbose_name = 'Qo`shimcha fotosurat'

class Comment(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='E`lon')
    author = models.CharField(max_length=30, verbose_name='Muallif')
    content = models.TextField(verbose_name='Mazmuni')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Ekranga chiqarish kerakmi?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Chop etilgan')
    
    class Meta:
        verbose_name_plural = 'Izohlar'
        verbose_name = 'Izoh'
        ordering = ['created_at']


