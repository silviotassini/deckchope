from django.db import models
from produtos.models import Produto


ID_UNIT = (
            (1, "Unidade 01"),
            (2, "Unidade 02"),
             )

TYPE_PERSON = (
            (0, "Pessoa Física"),
            (1, "Pessoa Jurídica"),
             )

UF_CHOICES = (
    ('AC', 'Acre'), 
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranão'),
    ('MG', 'Minas Gerais'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PE', 'Pernanbuco'),
    ('PI', 'Piauí'),
    ('PR', 'Paraná'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('RS', 'Rio Grande do Sul'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins')
)

class Cliente(models.Model):
    filial = models.SmallIntegerField(choices=ID_UNIT, blank=True)
    nome = models.CharField(max_length=200, verbose_name="Cliente")    
    razaosocial = models.CharField(max_length=200, blank=True, verbose_name="Razão Social")
    tipo = models.SmallIntegerField(choices=TYPE_PERSON)
    cpfcnpj = models.CharField(max_length=18, verbose_name="CPF/CNPJ")
    rgie = models.CharField(max_length=14, blank=True, null=True, verbose_name="Insc.Estadual")
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=150, blank=True, null=True)
    numero = models.CharField(max_length=6, blank=True, null=True)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name="CEP")
    cidade = models.CharField(max_length=250, default='Belo Horizonte')
    uf = models.CharField(max_length=2, default='MG', choices=UF_CHOICES, verbose_name="UF")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    phone1 = models.CharField(max_length=15, verbose_name="Telefone")
    phone2 = models.CharField(max_length=15, blank=True, verbose_name="Telefone")
    obs = models.TextField(blank=True, verbose_name="Observações")
    delivery = models.BooleanField(default=False, verbose_name="Delivery")
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    @property
    def nomeCliente(self):
        tmp = self.nome.strip()        
        if self.delivery:
            tmp = tmp + " ( Delivery )"
        return tmp

class ClienteTabela(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Preço')

    def __str__(self):
        return self.produto.nome + " " + str(self.preco)

    def datacsv(self):
        return str(self.id) + ";" + self.cliente.nome + ";" + self.produto.nome + ";" + str(self.preco)

    class Meta:
        verbose_name = "tabela"