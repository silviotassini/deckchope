# Generated by Django 3.2.12 on 2023-01-26 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
        ('produtos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data Criação')),
                ('data_pedido', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data Pedido')),
                ('data_entrega', models.DateField(blank=True, null=True, verbose_name='Data Entrega')),
                ('forma_pgto', models.CharField(blank=True, choices=[('1', 'Boleto'), ('2', 'Cartão Crédito'), ('3', 'Cartão Débito'), ('4', 'Dinheiro'), ('5', 'PIX')], default='4', max_length=1, null=True, verbose_name='Forma de Pagto')),
                ('data_pgto', models.DateField(blank=True, null=True, verbose_name='Data Pgto')),
                ('status', models.CharField(blank=True, choices=[('1', 'Pendente'), ('2', 'Entregue'), ('3', 'Pago')], default='1', max_length=1, null=True, verbose_name='Status')),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
                ('usuario', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-data_pedido'],
            },
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),
                ('quantidade', models.PositiveIntegerField(verbose_name='Qtd')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produto')),
            ],
            options={
                'verbose_name': 'Item do pedido',
                'verbose_name_plural': 'Itens do pedido',
            },
        ),
    ]
