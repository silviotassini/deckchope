from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from clientes.models import Cliente
from produtos.models import Produto

CH_PGTO=(            
        ('1', 'Boleto'),
        ('2', 'Cartão Crédito'),
        ('3', 'Cartão Débito'),
        ('4', 'Dinheiro'),
        ('5', 'PIX'),            
    )
CH_STATUS=(            
        ('1', 'Pendente'), #pendente entrega e pgto
        ('2', 'Entregue'), # pendente pgto
        ('3', 'Pago'), # pendente entrega
        #('4', 'Finalizado'), # Entregue e pago
    )

class Pedido(models.Model):
    usuario = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data Criação")   
    data_pedido  = models.DateTimeField(default=timezone.now, verbose_name="Data Pedido")   
    data_entrega = models.DateField(blank=True, null=True, verbose_name="Data Entrega")
    forma_pgto = models.CharField(blank=True, null=True, max_length=1, default='4', choices=CH_PGTO, verbose_name="Forma de Pagto")
    data_pgto = models.DateField(blank=True, null=True, verbose_name="Data Pgto")
    status = models.CharField(max_length=1, default='1', blank=True, null=True, choices=CH_STATUS, verbose_name="Status")    
    obs = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        ordering  = ['-data_pedido',]
 
    def __str__(self):
        return f'Pedido N. {self.pk}'
 

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    quantidade = models.PositiveIntegerField(verbose_name="Qtd")
    #obs = models.TextField(blank=True, null=True, verbose_name="Observações")

    def __str__(self):
        return f'{self.pedido} - [{self.produto.nome}]'

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'
