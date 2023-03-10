# Generated by Django 3.2.12 on 2023-03-07 15:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
        ('produtos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='tipo',
            field=models.SmallIntegerField(choices=[(0, 'Venda'), (1, 'Empréstimo')]),
        ),
        migrations.CreateModel(
            name='ProdutoEmprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datainicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('datafim', models.DateTimeField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produto')),
            ],
            options={
                'verbose_name': 'Emprestimos',
            },
        ),
    ]