from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django_tables2 import SingleTableView
import plotly.graph_objs as go
from plotly.offline import plot
import os
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from .models import ente_devedor
from .tables import ente_devedor_table
from .models import unidade
from .tables import unidade_table
import csv
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import baixa
from .tables import baixa_table
from .models import autuacao
from .tables import autuacao_table
from .models import validacao
from .tables import validacao_table

def index(request):
    usuario = request.POST.get('username')
    senha = request.POST.get('password')
    user = authenticate(username=usuario, password=senha)
    if (user is not None):
        login(request, user)
        request.session['username'] = usuario
        request.session['password'] = senha
        request.session['usernamefull'] = user.get_full_name()
        print(request.session['username'])
        print(request.session['password'])
        print(request.session['usernamefull'])
        return redirect('ente_devedor_menu_alias')
    else:
        data = {}
        if (usuario):
            data['msg'] = "Usuário ou Senha Incorretos " + usuario
        return render(request, 'index.html', data)

def grafico(request):
    exame_tmp = exame.objects.all()
    eixo_x = []
    eixo_y = []
    i = 0
    for e in exame_tmp:
        i += 1
        eixo_x.append(i)
        eixo_y.append(e.valor)
    figura = go.Figure()
    figura.add_trace(go.Scatter(x=eixo_x, y=eixo_y, mode='lines',
                                line_color='rgb(0, 0, 255)'))
    figura.update_layout(title="Dados de Exame", title_x=0.5,
                         xaxis_title='Tempo', yaxis_title='Batimento Cardíaco')
    plot_div = plot(figura, output_type='div')
    dicionario = {}
    dicionario['grafico'] = plot_div
    return render(request, 'grafico.html', dicionario)

class ente_devedor_menu(SingleTableView):
    model = ente_devedor
    table_class = ente_devedor_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'precatory/ente_devedor_list.html'

def ente_devedor_em_lote_create(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"].read().decode("utf-8").splitlines()
            reader = csv.DictReader(file)
            for row in reader:
                ente_devedor.objects.create(
                    uuid=row["enteDevedorId"],
                    nome=row["enteDevedorNome"]
                )
            return redirect("ente_devedor_menu_alias")
    else:
        form = CSVUploadForm()
    return render(request, "precatory/ente_devedor_upload.html", {"form": form})

class ente_devedor_create(CreateView):
    model = ente_devedor
    fields = ['nome', 'uuid', 'ativo']

    def get_success_url(self):
        return reverse_lazy('ente_devedor_menu_alias')


class ente_devedor_list(ListView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm("precatory.view_ente_devedor"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Sem permissão para listar ente_devedors")

    model = ente_devedor
    queryset = ente_devedor.objects.filter(ativo=True)


class ente_devedor_update(UpdateView):
    model = ente_devedor
    fields = ['nome', 'uuid', 'ativo']

    def get_success_url(self):
        return reverse_lazy('ente_devedor_menu_alias')


class ente_devedor_delete(DeleteView):
    model = ente_devedor
    fields = ['nome', 'uuid', 'ativo']
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse_lazy('ente_devedor_menu_alias')

def ente_devedor_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entesDevedores.csv"'

    writer = csv.writer(response)
    writer.writerow(['nome','uuid', 'ativo'])

    users = ente_devedor.objects.all().values_list('nome','uuid', 'ativo')
    for user in users:
        writer.writerow(user)

    return response

class unidade_menu(SingleTableView):
    model = unidade
    table_class = unidade_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'precatory/unidade_list.html'

def unidade_em_lote_create(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"].read().decode("utf-8").splitlines()
            reader = csv.DictReader(file)
            for row in reader:
                unidade.objects.create(
                    rhid=row["unidadeId"],
                    nome=row["unidadeNome"]
                )
            return redirect("unidade_menu_alias")
    else:
        form = CSVUploadForm()
    return render(request, "precatory/unidade_upload.html", {"form": form})

class unidade_create(CreateView):
    model = unidade
    fields = ['nome', 'uuid', 'ativo']

    def get_success_url(self):
        return reverse_lazy('unidade_menu_alias')


class unidade_list(ListView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm("precatory.view_unidade"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Sem permissão para listar unidades")

    model = unidade
    queryset = unidade.objects.filter(ativo=True)


class unidade_update(UpdateView):
    model = unidade
    fields = ['nome', 'uuid', 'ativo']

    def get_success_url(self):
        return reverse_lazy('unidade_menu_alias')


class unidade_delete(DeleteView):
    model = unidade
    fields = ['nome', 'uuid', 'ativo']
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse_lazy('unidade_menu_alias')

def unidade_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="unidades.csv"'

    writer = csv.writer(response)
    writer.writerow(['nome','rhid', 'ativo'])

    users = unidade.objects.all().values_list('nome','rhid', 'ativo')
    for user in users:
        writer.writerow(user)

    return response

class validacao_menu(SingleTableView):
    model = validacao
    table_class = validacao_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'precatory/validacao_list.html'

def validacao_em_lote_create(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"].read().decode("utf-8").splitlines()
            reader = csv.DictReader(file)
            for row in reader:
                validacao.objects.create(
                    data_da_criacao=row["dataDaCriacao"],
                    tipo_de_pessoa=row["tipoDePessoa"],
                    data_de_nascimento=row["dataDeNascimento"],
                    classificacao_da_doenca=row["classificacaoDaDoenca"],
                    ente_devedor=ente_devedor.objects.get(uuid=row["enteDevedorId"]),
                    unidade=unidade.objects.get(rhid=row["unidadeId"]),
                    valor=row["valor"],
                    data_da_validacao=row["dataDaValidacao"],
                )
            return redirect("validacao_menu_alias")
    else:
        form = CSVUploadForm()
    return render(request, "precatory/validacao_upload.html", {"form": form})

class validacao_create(CreateView):
    model = validacao
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ativo']

    def get_success_url(self):
        return reverse_lazy('validacao_menu_alias')


class validacao_list(ListView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm("precatory.view_validacao"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Sem permissão para listar validacaos")

    model = validacao
    queryset = validacao.objects.filter(ativo=True)


class validacao_update(UpdateView):
    model = validacao
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ativo']

    def get_success_url(self):
        return reverse_lazy('validacao_menu_alias')


class validacao_delete(DeleteView):
    model = validacao
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ativo']
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse_lazy('validacao_menu_alias')

def validacao_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="validacaos.csv"'

    writer = csv.writer(response)
    writer.writerow(['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ativo'])

    users = validacao.objects.all().values_list('data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ativo')
    for user in users:
        writer.writerow(user)

    return response

class autuacao_menu(SingleTableView):
    model = autuacao
    table_class = autuacao_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'precatory/autuacao_list.html'

def autuacao_em_lote_create(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"].read().decode("utf-8").splitlines()
            reader = csv.DictReader(file)
            for row in reader:
                autuacao.objects.create(
                    data_da_criacao=row["dataDaCriacao"],
                    tipo_de_pessoa=row["tipoDePessoa"],
                    data_de_nascimento=row["dataDeNascimento"],
                    classificacao_da_doenca=row["classificacaoDaDoenca"],
                    ente_devedor=ente_devedor.objects.get(uuid=row["enteDevedorId"]),
                    unidade=unidade.objects.get(rhid=row["unidadeId"]),
                    valor=row["valor"],
                    data_da_validacao=row["dataDaValidacao"],
                    ano_de_orcamento=row["anoDeOrcamento"],
                    data_da_autuacao=row["dataDaAutuacao"]
                )
            return redirect("autuacao_menu_alias")
    else:
        form = CSVUploadForm()
    return render(request, "precatory/autuacao_upload.html", {"form": form})

class autuacao_create(CreateView):
    model = autuacao
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao','ativo']

    def get_success_url(self):
        return reverse_lazy('autuacao_menu_alias')


class autuacao_list(ListView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm("precatory.view_autuacao"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Sem permissão para listar autuacaos")

    model = autuacao
    queryset = autuacao.objects.filter(ativo=True)


class autuacao_update(UpdateView):
    model = autuacao
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao','ativo']

    def get_success_url(self):
        return reverse_lazy('autuacao_menu_alias')


class autuacao_delete(DeleteView):
    model = autuacao
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao','ativo']
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse_lazy('autuacao_menu_alias')

def autuacao_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="autuacaos.csv"'

    writer = csv.writer(response)
    writer.writerow(['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao','ativo'])

    users = autuacao.objects.all().values_list('data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao','ativo')
    for user in users:
        writer.writerow(user)

    return response

class baixa_menu(SingleTableView):
    model = baixa
    table_class = baixa_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'precatory/baixa_list.html'

def baixa_em_lote_create(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"].read().decode("utf-8").splitlines()
            reader = csv.DictReader(file)
            for row in reader:
                baixa.objects.create(
                    data_da_criacao=row["dataDaCriacao"],
                    tipo_de_pessoa=row["tipoDePessoa"],
                    data_de_nascimento=row["dataDeNascimento"],
                    classificacao_da_doenca=row["classificacaoDaDoenca"],
                    ente_devedor=ente_devedor.objects.get(uuid=row["enteDevedorId"]),
                    unidade=unidade.objects.get(rhid=row["unidadeId"]),
                    valor=row["valor"],
                    data_da_validacao=row["dataDaValidacao"],
                    ano_de_orcamento=row["anoDeOrcamento"],
                    data_da_autuacao=row["dataDaAutuacao"],
                    data_da_baixa=row["dataDaBaixa"],
                )
            return redirect("baixa_menu_alias")
    else:
        form = CSVUploadForm()
    return render(request, "precatory/baixa_upload.html", {"form": form})

class baixa_create(CreateView):
    model = baixa
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao',
                                            'data_da_baixa','ativo']

    def get_success_url(self):
        return reverse_lazy('baixa_menu_alias')


class baixa_list(ListView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm("precatory.view_baixa"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Sem permissão para listar baixas")

    model = baixa
    queryset = baixa.objects.filter(ativo=True)


class baixa_update(UpdateView):
    model = baixa
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao',
                                            'data_da_baixa','ativo']

    def get_success_url(self):
        return reverse_lazy('baixa_menu_alias')


class baixa_delete(DeleteView):
    model = baixa
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao',
                                            'data_da_baixa','ativo']
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse_lazy('baixa_menu_alias')

def baixa_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="baixas.csv"'

    writer = csv.writer(response)
    writer.writerow(['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao',
                                            'data_da_baixa','ativo'])

    users = baixa.objects.all().values_list('data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao',
                                            'data_da_baixa','ativo')
    for user in users:
        writer.writerow(user)

    return response