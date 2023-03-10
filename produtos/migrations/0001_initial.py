# Generated by Django 3.2 on 2023-01-26 13:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filial', models.SmallIntegerField(blank=True, choices=[(1, 'Unidade 01'), (2, 'Unidade 02')], default=1, null=True)),
                ('nome', models.CharField(max_length=200, verbose_name='Produto')),
                ('descricao', models.CharField(blank=True, max_length=200, verbose_name='Descrição')),
                ('unidade', models.SmallIntegerField(choices=[(0, 'Unidade'), (1, 'Litro'), (2, 'Kilo')])),
                ('codigo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Código')),
                ('preco_custo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Preço de custo')),
                ('preco_delivery', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Preço Delivery')),
                ('preco_venda', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Preço PDV')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='produto_imagens/')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('tipo', models.SmallIntegerField(choices=[(0, 'Bens de consumo'), (1, 'Material')])),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='ProdutoEstoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estoque', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Estoque atual')),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produto')),
            ],
            options={
                'ordering': ('-data',),
            },
        ),
    ]
