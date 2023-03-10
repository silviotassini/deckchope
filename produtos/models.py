import os
import random
import string

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image


ID_UNIT = (
    (1, "Unidade 01"),
    (2, "Unidade 02"),
)

PROD_UNIT = (
            (0, "Unidade"),
            (1, "Litro"),
            (2, "Kilo"),
)

PROD_TIPO = (
            (0, "Venda"),
            (1, "Empréstimo"),
)


class Produto(models.Model):
    filial = models.SmallIntegerField(
        choices=ID_UNIT, blank=True, null=True, default=1)
    nome = models.CharField(max_length=200, verbose_name="Produto")
    descricao = models.CharField(
        max_length=200, blank=True, verbose_name="Descrição")
    unidade = models.SmallIntegerField(choices=PROD_UNIT)
    codigo = models.CharField(
        max_length=100,  blank=True, null=True, verbose_name="Código")
    preco_custo = models.DecimalField(
        max_digits=10, blank=True, null=True, decimal_places=2, verbose_name='Preço de custo')
    preco_delivery = models.DecimalField(
        max_digits=10, blank=True, null=True, decimal_places=2, verbose_name='Preço Delivery')
    preco_venda = models.DecimalField(
        max_digits=10, blank=True, null=True, decimal_places=2, verbose_name='Preço PDV')
    imagem = models.ImageField(
        upload_to='produto_imagens/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    tipo = models.SmallIntegerField(choices=PROD_TIPO)
    data_criacao = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.nome)
            random_string = ''.join(random.choices(
                string.ascii_lowercase + string.digits, k=3))
            self.slug = f'{slug}-{random_string}'

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class ProdutoEmprestimo(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    datainicio = models.DateTimeField(default=timezone.now)
    datafim = models.DateTimeField(blank=True, null=True)

    @staticmethod
    def devolver(id_emprestimo):
        emprestimo = ProdutoEmprestimo.objects.get(id=id_emprestimo)

        emprestimo.datafim = timezone.now()
        emprestimo.save()

    class Meta:
        verbose_name = "Emprestimos"

    def __str__(self):
        return self.cliente.nome + "  " + str(self.datainicio)


class ProdutoEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    estoque = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Estoque atual')
    data = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-data',)

    def __str__(self):
        return self.produto.nome + " : " + str(self.estoque)
