# Generated by Django 3.1.7 on 2021-11-16 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Analytic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('gain', models.FloatField(blank=True, default=0, null=True)),
                ('all_bets', models.IntegerField(blank=True, default=1, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CashStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('give_away', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='give_away')),
                ('to_keep', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='to_keep')),
            ],
        ),
        migrations.CreateModel(
            name='DaruWheelSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('return_val', models.FloatField(blank=True, default=0, null=True)),
                ('min_redeem_refer_credit', models.FloatField(blank=True, default=1000, null=True)),
                ('refer_per', models.FloatField(blank=True, default=0, null=True)),
                ('per_to_keep', models.FloatField(blank=True, default=5, null=True)),
                ('closed_at', models.FloatField(blank=True, default=4.7, help_text='sensitive settings value.Dont edit', null=True)),
                ('results_at', models.FloatField(blank=True, default=4.8, help_text='sensitive settings value.Dont edit', null=True)),
                ('wheelspin_id', models.IntegerField(blank=True, default=1, help_text='super critical setting value.DONT EDIT!', null=True)),
                ('curr_unit', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('min_bet', models.DecimalField(blank=True, decimal_places=2, default=45.9, max_digits=5, null=True)),
                ('win_algo', models.IntegerField(blank=True, default=1, help_text='1=Random win_RECO,2=Using i win rate  Algo,3=Sure win_to_impress_', null=True)),
                ('trial_algo', models.IntegerField(blank=True, default=1, help_text='1=Normal win_RECO,2=Super win_to_impress,others=Use_win_algo_above', null=True)),
                ('big_win_multiplier', models.FloatField(blank=True, default=10, null=True)),
            ],
            options={
                'db_table': 'd_daruwheel_setup',
            },
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('odds', models.FloatField(blank=True, max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WheelSpin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('open_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('results_at', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('per_retun', models.FloatField(blank=True, default=0, null=True)),
                ('receive_results', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'db_table': 'd_wheel_markets',
            },
        ),
        migrations.CreateModel(
            name='Stake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=50, max_digits=12, verbose_name='amount')),
                ('current_bal', models.FloatField(default=0, max_length=10)),
                ('stake_placed', models.BooleanField(blank=True, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
                ('has_market', models.BooleanField(blank=True, default=False, null=True)),
                ('bet_on_real_account', models.BooleanField(default=False)),
                ('outcome_received', models.BooleanField(blank=True, default=False, null=True)),
                ('spinned', models.BooleanField(blank=True, default=False, null=True)),
                ('market', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='market_instnces', to='daru_wheel.wheelspin')),
                ('marketselection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imarketselections', to='daru_wheel.selection')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_wp_istakes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutCome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('result', models.IntegerField(blank=True, null=True)),
                ('pointer', models.IntegerField(blank=True, null=True)),
                ('closed', models.BooleanField(blank=True, default=False, null=True)),
                ('return_per', models.FloatField(blank=True, null=True)),
                ('gain', models.DecimalField(blank=True, decimal_places=5, max_digits=100, null=True, verbose_name='gain')),
                ('active', models.BooleanField(blank=True, null=True)),
                ('cashstore', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cashstores', to='daru_wheel.cashstore')),
                ('cumgain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gains', to='daru_wheel.analytic')),
                ('market', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marketoutcomess', to='daru_wheel.wheelspin')),
                ('stake', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='istakes', to='daru_wheel.stake')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
