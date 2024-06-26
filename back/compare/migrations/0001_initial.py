# Generated by Django 4.2.13 on 2024-05-23 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dcls_month', models.DateField()),
                ('fin_co_no', models.CharField(max_length=100)),
                ('kor_co_nm', models.CharField(max_length=100)),
                ('fin_prdt_cd', models.CharField(max_length=100)),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('join_way', models.CharField(max_length=100)),
                ('mtrt_int', models.TextField(blank=True, null=True)),
                ('spcl_cnd', models.TextField(blank=True, null=True)),
                ('join_deny', models.IntegerField(blank=True, null=True)),
                ('join_member', models.TextField(blank=True, null=True)),
                ('etc_note', models.TextField(blank=True, null=True)),
                ('max_limit', models.IntegerField(blank=True, null=True)),
                ('dcls_strt_day', models.CharField(max_length=100)),
                ('dcls_end_day', models.CharField(blank=True, max_length=100, null=True)),
                ('fin_co_subm_day', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Saving',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dcls_month', models.DateField()),
                ('fin_co_no', models.CharField(max_length=100)),
                ('kor_co_nm', models.CharField(max_length=100)),
                ('fin_prdt_cd', models.CharField(max_length=100)),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('join_way', models.CharField(max_length=100)),
                ('mtrt_int', models.TextField(blank=True, null=True)),
                ('spcl_cnd', models.TextField(blank=True, null=True)),
                ('join_deny', models.IntegerField(blank=True, null=True)),
                ('join_member', models.TextField(blank=True, null=True)),
                ('etc_note', models.TextField(blank=True, null=True)),
                ('max_limit', models.IntegerField(blank=True, null=True)),
                ('dcls_strt_day', models.CharField(max_length=100)),
                ('dcls_end_day', models.CharField(blank=True, max_length=100, null=True)),
                ('fin_co_subm_day', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SavingOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr_rate_type', models.CharField(max_length=1)),
                ('intr_rate_type_nm', models.CharField(max_length=2)),
                ('rsrv_type', models.CharField(max_length=1)),
                ('rsrv_type_nm', models.CharField(max_length=5)),
                ('save_trm', models.CharField(max_length=3)),
                ('intr_rate', models.FloatField(null=True)),
                ('intr_rate2', models.FloatField(null=True)),
                ('saving', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='compare.saving')),
            ],
        ),
        migrations.CreateModel(
            name='DepositOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr_rate_type', models.CharField(max_length=1)),
                ('intr_rate_type_nm', models.CharField(max_length=2)),
                ('save_trm', models.CharField(max_length=3)),
                ('intr_rate', models.FloatField(null=True)),
                ('intr_rate2', models.FloatField(null=True)),
                ('deposit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='compare.deposit')),
            ],
        ),
    ]
