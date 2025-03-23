import django_tables2 as tables
from django_tables2.utils import A
from .models import ente_devedor
from .models import unidade
from .models import validacao
from .models import autuacao
from .models import baixa

class ente_devedor_table(tables.Table):
    nome = tables.LinkColumn("ente_devedor_update_alias", args=[A("pk")])
    uuid = tables.LinkColumn("ente_devedor_update_alias", args=[A("pk")])
    ativo = tables.Column()
    id = tables.LinkColumn("ente_devedor_delete_alias", args=[A("pk")], verbose_name="Excluir")
    class Meta:
        model = ente_devedor
        attrs = {"class": "table thead-light table-striped table-hover"}
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nome', 'uuid', 'ativo')

class unidade_table(tables.Table):
    nome = tables.LinkColumn("unidade_update_alias", args=[A("pk")])
    rhid = tables.LinkColumn("unidade_update_alias", args=[A("pk")])
    ativo = tables.Column()
    id = tables.LinkColumn("unidade_delete_alias", args=[A("pk")], verbose_name="Excluir")
    class Meta:
        model = unidade
        attrs = {"class": "table thead-light table-striped table-hover"}
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nome', 'rhid', 'ativo')

class validacao_table(tables.Table):
    data_da_criacao = tables.LinkColumn("validacao_update_alias", args=[A("pk")])
    tipo_de_pessoa = tables.LinkColumn("validacao_update_alias", args=[A("pk")])
    data_de_nascimento = tables.LinkColumn("validacao_update_alias", args=[A("pk")])
    classificacao_da_doenca = tables.LinkColumn("validacao_update_alias", args=[A("pk")])
    ente_devedor = tables.LinkColumn("validacao_update_alias", args=[A("pk")])
    unidade = tables.LinkColumn("validacao_update_alias", args=[A("pk")])
    valor = tables.LinkColumn("validacao_update_alias", args=[A("pk")])
    data_da_validacao = tables.LinkColumn("validacao_update_alias", args=[A("pk")])
    ativo = tables.Column()
    id = tables.LinkColumn("validacao_delete_alias", args=[A("pk")], verbose_name="Excluir")

    class Meta:
        model = validacao
        attrs = {"class": "table thead-light table-striped table-hover"}
        template_name = "django_tables2/bootstrap4.html"
        fields = ('data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento', 'classificacao_da_doenca'
                  'ente_devedor', 'unidade', 'valor','data_da_validacao', 'ativo')

class autuacao_table(tables.Table):
    data_da_criacao = tables.LinkColumn("autuacao_update_alias", args=[A("pk")])
    tipo_de_pessoa = tables.LinkColumn("autuacao_update_alias", args=[A("pk")])
    data_de_nascimento = tables.LinkColumn("autuacao_update_alias", args=[A("pk")])
    classificacao_da_doenca = tables.LinkColumn("autuacao_update_alias", args=[A("pk")])
    ente_devedor = tables.LinkColumn("autuacao_update_alias", args=[A("pk")])
    unidade = tables.LinkColumn("autuacao_update_alias", args=[A("pk")])
    valor = tables.LinkColumn("autuacao_update_alias", args=[A("pk")])
    data_da_validacao = tables.LinkColumn("autuacao_update_alias", args=[A("pk")])
    ano_de_orcamento = tables.LinkColumn("autuacao_update_alias", args=[A("pk")])
    data_da_autuacao = tables.LinkColumn("autuacao_update_alias", args=[A("pk")])
    ativo = tables.Column()
    id = tables.LinkColumn("autuacao_delete_alias", args=[A("pk")], verbose_name="Excluir")
    class Meta:
        model = autuacao
        attrs = {"class": "table thead-light table-striped table-hover"}
        template_name = "django_tables2/bootstrap4.html"
        fields = ('data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento', 'classificacao_da_doenca'
                  'ente_devedor', 'unidade', 'valor', 'data_da_validacao', 'ano_de_orcamento',
                  'data_da_autuacao', 'ativo')

class baixa_table(tables.Table):
    data_da_criacao = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    tipo_de_pessoa = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    data_de_nascimento = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    classificacao_da_doenca = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    ente_devedor = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    unidade = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    valor = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    data_da_validacao = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    ano_de_orcamento = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    data_da_autuacao = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    data_da_baixa = tables.LinkColumn("baixa_update_alias", args=[A("pk")])
    ativo = tables.Column()
    id = tables.LinkColumn("baixa_delete_alias", args=[A("pk")], verbose_name="Excluir")
    class Meta:
        model = baixa
        attrs = {"class": "table thead-light table-striped table-hover"}
        template_name = "django_tables2/bootstrap4.html"
        fields = ('data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento', 'classificacao_da_doenca'
                  'ente_devedor', 'unidade', 'valor', 'data_da_validacao', 'ano_de_orcamento',
                  'data_da_autuacao', 'data_da_baixa','ativo')