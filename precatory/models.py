from django.db import models

class pessoa(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome')
    email = models.CharField(max_length=50, null=False, blank=False, verbose_name='eMail')
    celular = models.CharField(max_length=20, null=True, blank=True, verbose_name='celular')
    funcao = models.CharField(max_length=30, null=True, blank=True, verbose_name='Funcao')
    nascimento = models.DateField(null=True, blank=True, verbose_name='Nascimento')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome', 'funcao']
        
class procedimento(models.Model):
    descricao = models.CharField(max_length=50, null=False, blank=False, verbose_name='Descricao')
    cid = models.CharField(max_length=20, null=False, blank=False, verbose_name='CID')
    valor = models.FloatField(null=True, blank=True, default=None, verbose_name='Valor')

    def __str__(self): 
        return self.descricao + str(self.valor)

    class Meta:
        ordering = ['descricao']
        
class procedimento_executado(models.Model):
    pessoa = models.ForeignKey(pessoa, on_delete=models.CASCADE)
    procedimento = models.ForeignKey(procedimento, on_delete=models.CASCADE)
    obs = models.CharField(max_length=50, null=False, blank=False, verbose_name='Obs')
    quantidade = models.FloatField(null=True, blank=True, default=None, verbose_name='Quantidade')

    def __str__(self): 
        return self.pessoa.nome + " - " + self.procedimento.descricao + " - " + self.obs

    class Meta:
        ordering = ['pessoa', 'procedimento']
        
class exame(models.Model):
    valor = models.FloatField(null=True, blank=True, default=None, verbose_name='Valor')

    def __str__(self):
        return self.valor

class ente_devedor(models.Model):
    uuid = models.CharField(max_length=36, unique=True, null=False, blank=False, verbose_name='UUID')
    nome = models.CharField(max_length=100, null=False, blank=False, verbose_name='Nome')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

class unidade(models.Model):
    rhid = models.IntegerField(unique=True, null=False, verbose_name='RHID')
    nome = models.CharField(max_length=200, null=False, blank=False, verbose_name='Nome')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


class base_registro(models.Model):
    data_da_criacao = models.DateTimeField(verbose_name='Data da Criação')
    tipo_de_pessoa = models.CharField(
        max_length=2, choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], verbose_name='Tipo de Pessoa'
    )
    data_de_nascimento = models.DateField(verbose_name='Data de Nascimento')
    classificacao_da_doenca = models.CharField(max_length=50, verbose_name='Classificação da Doença')
    ente_devedor = models.ForeignKey('ente_devedor', on_delete=models.CASCADE, verbose_name='Ente Devedor')
    unidade = models.ForeignKey('unidade', on_delete=models.CASCADE, verbose_name='Unidade')
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Valor')

    class Meta:
        abstract = True


class validacao(base_registro):
    data_da_validacao = models.DateTimeField(verbose_name='Data da Validação')

    class Meta:
        ordering = ['data_da_validacao']

    def __str__(self):
        return f"Validação {self.data_da_validacao} - {self.ente_devedor.nome} - {self.unidade.nome}"


class autuacao(validacao):
    ano_de_orcamento = models.IntegerField(verbose_name='Ano de Orçamento')
    data_da_autuacao = models.DateTimeField(verbose_name='Data da Autuação')

    class Meta:
        ordering = ['data_da_autuacao']

    def __str__(self):
        return f"Autuação {self.data_da_autuacao} - {self.ente_devedor.nome} - {self.unidade.nome}"


class baixa(autuacao):
    data_da_baixa = models.DateField(verbose_name='Data da Baixa', null=True, blank=True)

    class Meta:
        ordering = ['data_da_baixa']

    def __str__(self):
        return f"Baixa {self.data_da_baixa} - {self.ente_devedor.nome} - {self.unidade.nome}"