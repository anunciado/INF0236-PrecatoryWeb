import django_tables2 as tables
from django_tables2.utils import A
from .models import ente_devedor
from .models import unidade

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