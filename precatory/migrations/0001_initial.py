# Generated by Django 4.2.17 on 2025-03-09 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ente_devedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=36, unique=True, verbose_name='UUID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='unidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rhid', models.IntegerField(unique=True, verbose_name='RHID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='validacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_da_criacao', models.DateTimeField(verbose_name='Data da Criação')),
                ('tipo_de_pessoa', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, verbose_name='Tipo de Pessoa')),
                ('data_de_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('classificacao_da_doenca', models.CharField(max_length=50, verbose_name='Classificação da Doença')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor')),
                ('data_da_validacao', models.DateTimeField(verbose_name='Data da Validação')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('ente_devedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='precatory.ente_devedor', verbose_name='Ente Devedor')),
                ('unidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='precatory.unidade', verbose_name='Unidade')),
            ],
            options={
                'ordering': ['data_da_validacao'],
            },
        ),
        migrations.CreateModel(
            name='baixa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_da_criacao', models.DateTimeField(verbose_name='Data da Criação')),
                ('tipo_de_pessoa', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, verbose_name='Tipo de Pessoa')),
                ('data_de_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('classificacao_da_doenca', models.CharField(max_length=50, verbose_name='Classificação da Doença')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor')),
                ('data_da_validacao', models.DateTimeField(verbose_name='Data da Validação')),
                ('ano_de_orcamento', models.IntegerField(verbose_name='Ano de Orçamento')),
                ('data_da_autuacao', models.DateTimeField(verbose_name='Data da Autuação')),
                ('data_da_baixa', models.DateField(blank=True, null=True, verbose_name='Data da Baixa')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('ente_devedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='precatory.ente_devedor', verbose_name='Ente Devedor')),
                ('unidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='precatory.unidade', verbose_name='Unidade')),
            ],
            options={
                'ordering': ['data_da_baixa'],
            },
        ),
        migrations.CreateModel(
            name='autuacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_da_criacao', models.DateTimeField(verbose_name='Data da Criação')),
                ('tipo_de_pessoa', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, verbose_name='Tipo de Pessoa')),
                ('data_de_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('classificacao_da_doenca', models.CharField(max_length=50, verbose_name='Classificação da Doença')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor')),
                ('data_da_validacao', models.DateTimeField(verbose_name='Data da Validação')),
                ('ano_de_orcamento', models.IntegerField(verbose_name='Ano de Orçamento')),
                ('data_da_autuacao', models.DateTimeField(verbose_name='Data da Autuação')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('ente_devedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='precatory.ente_devedor', verbose_name='Ente Devedor')),
                ('unidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='precatory.unidade', verbose_name='Unidade')),
            ],
            options={
                'ordering': ['data_da_autuacao'],
            },
        ),
    ]
