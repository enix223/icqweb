from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string
from django.utils.timezone import now, timedelta
from dateutil.relativedelta import relativedelta

class Package(models.Model):
    """
    @brief  SS Package
    @desc   limit base on unit MB, time_unit is base on day
    """
    upload_path='media/images'
    TIME_UNIT = (('D', 'Day'), ('M', 'Month'), ('Y', 'Year'))
    package_name = models.CharField('Package name', max_length=20)
    flow_limit = models.BigIntegerField('Network flow limit')
    time_limit = models.IntegerField('Package time limit')
    time_unit = models.CharField('Package time unit', max_length=1,
                                 choices=TIME_UNIT)
    icon = models.CharField('Package icon', max_length=50)
    package_ad_img = models.ImageField('Ad image', upload_to=upload_path)
    package_price = models.DecimalField('Package price', max_digits=7, decimal_places=2)
    package_desc = models.TextField('Package desc')

    def get_expired_date(self):
        '''Get the expired date'''
        if self.time_unit == 'D':
            return now() + relativedelta(days=self.time_limit)
        elif self.time_unit == 'M':
            return now() + relativedelta(months=self.time_limit)
        elif self.time_unit == 'Y':
            return now() + relativedelta(years=self.time_limit)
        else:
            return now()

    def __unicode__(self):
        return self.package_name


class UserPackageRel(models.Model):
    """
    @brief  User package
    @desc   upload/download base on unit MB
    """
    user = models.OneToOneField(User)
    package = models.ForeignKey(Package)
    register_date = models.DateTimeField('User package register date',
                                         auto_now_add=True)
    upload = models.IntegerField('User uplaod used')
    download = models.IntegerField('User download used')
    expired_date = models.DateTimeField('Expired date')

    def is_valid(self):
        """
        @biref    Check with the user measures to find out if he/she still
                  valid.
        @retval1  True  - user still valid
        @retval2  False - user is not valid
        """
        if self.expired_date < now():
            return False
        else:
            if self.upload + self.download < self.package.flow_limit:
                return True
            else:
                return False

    def __unicode__(self):
        return u"user:{}, package:{}".format(
            self.user.username, self.package.package_name)


class UserProfile(models.Model):
    """ Extends SS features with Django Users """
    user = models.OneToOneField(User)
    passwd = models.CharField('SS Password', max_length=10,
                              default=get_random_string(length=6))

    def __unicode__(self):
        return "{}'s profile".format(self.user)


class Order(models.Model):
    """Order table"""
    ORDER_STATUS = ((0, 'Created'), (1, 'paid'))
    id = models.AutoField('order id', primary_key=True)
    user = models.ForeignKey(User)
    package = models.ForeignKey(Package)
    order_status = models.SmallIntegerField('order status', choices=ORDER_STATUS, default=0)
    created = models.DateTimeField('order create time', auto_now_add=True, editable=False)
    updated = models.DateTimeField('order update time', auto_now=True, editable=False)

    def __unicode__(self):
        return self.id


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        pkg = Package.objects.get(pk=1)
        UserPackageRel.objects.get_or_create(
            user=instance, package=pkg, upload=0,
            download=0, expired_date=pkg.get_expired_date())


post_save.connect(create_user_profile, sender=User)
