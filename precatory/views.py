import csv
import os

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django_tables2 import SingleTableView
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from datetime import datetime

from .forms import CSVUploadForm
from .models import autuacao
from .models import baixa
from .models import ente_devedor
from .models import unidade
from .models import validacao
from .tables import autuacao_table
from .tables import baixa_table
from .tables import ente_devedor_table
from .tables import unidade_table
from .tables import validacao_table


def index(request):
    usuario = request.POST.get('username')
    senha = request.POST.get('password')
    user = authenticate(username=usuario, password=senha)
    if (user is not None):
        login(request, user)
        return redirect('home')
    else:
        data = {}
        if (usuario):
            data['msg'] = "Usuário ou Senha Incorretos " + usuario
        return render(request, 'index.html', data)


def home(request):
    return render(request, 'home.html')


def ia_menu(request):
    return render(request, 'precatory/menu_ia.html')


def validacao_modelo_create(request):
    return render(request, 'precatory/validacao/validacao_modelo_create.html')


def autuacao_modelo_create(request):
    return render(request, 'precatory/autuacao/autuacao_modelo_create.html')


def baixa_modelo_create(request):
    return render(request, 'precatory/baixa/baixa_modelo_create.html')


class ente_devedor_menu(SingleTableView):
    model = ente_devedor
    table_class = ente_devedor_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'precatory/ente_devedor/ente_devedor_list.html'


def ente_devedor_em_lote_create(request):
    try:
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
            return render(request, "precatory/ente_devedor/ente_devedor_upload.html", {"form": form})
    except:
        data = {}
        data['msg'] = "Não foi possível carregar os dados"
        data['form'] = CSVUploadForm()
        return render(request, "precatory/ente_devedor/ente_devedor_upload.html", data)


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
    writer.writerow(['nome', 'uuid', 'ativo'])

    users = ente_devedor.objects.all().values_list('nome', 'uuid', 'ativo')
    for user in users:
        writer.writerow(user)

    return response


class unidade_menu(SingleTableView):
    model = unidade
    table_class = unidade_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'precatory/unidade/unidade_list.html'


def unidade_em_lote_create(request):
    try:
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
        return render(request, "precatory/unidade/unidade_upload.html", {"form": form})
    except:
        data = {}
        data['msg'] = "Não foi possível carregar os dados"
        data['form'] = CSVUploadForm()
        return render(request, "precatory/unidade/unidade_upload.html", data)


class unidade_create(CreateView):
    model = unidade
    fields = ['nome', 'rhid', 'ativo']

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
    fields = ['nome', 'rhid', 'ativo']

    def get_success_url(self):
        return reverse_lazy('unidade_menu_alias')


class unidade_delete(DeleteView):
    model = unidade
    fields = ['nome', 'rhid', 'ativo']
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse_lazy('unidade_menu_alias')


def unidade_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="unidades.csv"'

    writer = csv.writer(response)
    writer.writerow(['nome', 'rhid', 'ativo'])

    users = unidade.objects.all().values_list('nome', 'rhid', 'ativo')
    for user in users:
        writer.writerow(user)

    return response


class validacao_menu(SingleTableView):
    model = validacao
    table_class = validacao_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'precatory/validacao/validacao_list.html'


def validacao_em_lote_create(request):
    try:
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["file"].read().decode("utf-8").splitlines()
                reader = csv.DictReader(file)
                for row in reader:
                    validacao.objects.create(
                        data_da_criacao=row["dataDaCriacao"],
                        tipo_de_pessoa=row["tipoDePessoa"],
                        data_de_nascimento=row["dataDeNascimento"] if row["dataDeNascimento"] != "0" else None,
                        classificacao_da_doenca=row["classificacaoDaDoenca"],
                        ente_devedor=ente_devedor.objects.get(uuid=row["enteDevedorId"]),
                        unidade=unidade.objects.get(rhid=row["unidadeId"]),
                        valor=row["valor"],
                        data_da_validacao=row["dataDaValidacao"],
                    )
                return redirect("validacao_menu_alias")
        else:
            form = CSVUploadForm()
        return render(request, "precatory/validacao/validacao_upload.html", {"form": form})
    except:
        data = {}
        data['msg'] = "Não foi possível carregar os dados"
        data['form'] = CSVUploadForm()
        return render(request, "precatory/validacao/validacao_upload.html", data)


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
    template_name = 'precatory/autuacao/autuacao_list.html'


def autuacao_em_lote_create(request):
    try:
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["file"].read().decode("utf-8").splitlines()
                reader = csv.DictReader(file)
                for row in reader:
                    autuacao.objects.create(
                        data_da_criacao=row["dataDaCriacao"],
                        tipo_de_pessoa=row["tipoDePessoa"],
                        data_de_nascimento=row["dataDeNascimento"] if row["dataDeNascimento"] != "0" else None,
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
        return render(request, "precatory/autuacao/autuacao_upload.html", {"form": form})
    except:
        data = {}
        data['msg'] = "Não foi possível carregar os dados"
        data['form'] = CSVUploadForm()
        return render(request, "precatory/autuacao/autuacao_upload.html", data)


class autuacao_create(CreateView):
    model = autuacao
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
              'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
              'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao', 'ativo']

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
              'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao', 'ativo']

    def get_success_url(self):
        return reverse_lazy('autuacao_menu_alias')


class autuacao_delete(DeleteView):
    model = autuacao
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
              'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
              'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao', 'ativo']
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse_lazy('autuacao_menu_alias')


def autuacao_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="autuacaos.csv"'

    writer = csv.writer(response)
    writer.writerow(['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                     'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                     'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao', 'ativo'])

    users = autuacao.objects.all().values_list('data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                               'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                               'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao', 'ativo')
    for user in users:
        writer.writerow(user)

    return response


class baixa_menu(SingleTableView):
    model = baixa
    table_class = baixa_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'precatory/baixa/baixa_list.html'


def baixa_em_lote_create(request):
    try:
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["file"].read().decode("utf-8").splitlines()
                reader = csv.DictReader(file)
                for row in reader:
                    baixa.objects.create(
                        data_da_criacao=row["dataDaCriacao"],
                        tipo_de_pessoa=row["tipoDePessoa"],
                        data_de_nascimento=row["dataDeNascimento"] if row["dataDeNascimento"] != "0" else None,
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
        return render(request, "precatory/baixa/baixa_upload.html", {"form": form})

    except:
        data = {}
        data['msg'] = "Não foi possível carregar os dados"
        data['form'] = CSVUploadForm()
        return render(request, "precatory/baixa/baixa_upload.html", data)


class baixa_create(CreateView):
    model = baixa
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
              'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
              'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao',
              'data_da_baixa', 'ativo']

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
              'data_da_baixa', 'ativo']

    def get_success_url(self):
        return reverse_lazy('baixa_menu_alias')


class baixa_delete(DeleteView):
    model = baixa
    fields = ['data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
              'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
              'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao',
              'data_da_baixa', 'ativo']
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
                     'data_da_baixa', 'ativo'])

    users = baixa.objects.all().values_list('data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
                                            'classificacao_da_doenca', 'ente_devedor', 'unidade', 'valor',
                                            'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao',
                                            'data_da_baixa', 'ativo')
    for user in users:
        writer.writerow(user)

    return response


def train_validacao_model(request):
    # Busca os dados do banco de dados
    dados = validacao.objects.all().values(
        'data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
        'classificacao_da_doenca', 'ente_devedor', 'unidade',
        'valor', 'data_da_validacao'
    )
    df = pd.DataFrame.from_records(dados)

    # Pré-processamento dos dados
    df['data_da_criacao'] = pd.to_datetime(df['data_da_criacao']).astype('int64') / 10 ** 9
    df['data_de_nascimento'] = pd.to_datetime(df['data_de_nascimento']).astype('int64') / 10 ** 9
    df['data_da_validacao'] = pd.to_datetime(df['data_da_validacao']).astype('int64') / 10 ** 9
    df['tipo_de_pessoa'] = df['tipo_de_pessoa'].astype('category').cat.codes
    df['classificacao_da_doenca'] = df['classificacao_da_doenca'].astype('category').cat.codes

    # Removendo linhas com valores nulos na coluna target
    df = df.dropna(subset=['data_da_validacao'])

    # Separando features e target
    X = df.drop('data_da_validacao', axis=1)
    y = df['data_da_validacao']

    # Dividindo os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Configurando o RandomForestRegressor com os melhores parâmetros
    modelo = RandomForestRegressor(
        bootstrap=False,
        max_depth=30,
        max_features='sqrt',
        min_samples_leaf=1,
        min_samples_split=2,
        n_estimators=300,
        random_state=42
    )

    # Treinando o modelo
    modelo.fit(X_train, y_train)

    # Salvar modelo
    model_path = os.path.join(settings.MEDIA_ROOT, 'modelo_validacao_predicao.pkl')
    joblib.dump(modelo, model_path)

    # Fazendo previsões com o melhor modelo
    y_pred = modelo.predict(X_test)

    # Calculando métricas de desempenho
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    # Convertendo os valores numéricos de volta para datas
    y_test_dates = pd.to_datetime(y_test * 10 ** 9)  # Convertendo de segundos para datetime
    y_pred_dates = pd.to_datetime(modelo.predict(X_test) * 10 ** 9)  # Usando o melhor modelo

    # Gerando gráficos com Plotly
    # Gráfico de Linha (Valores Reais vs. Preditos)
    line_real = go.Scatter(
        x=y_test_dates,
        y=y_test_dates,
        mode='lines',
        name='Datas Reais',
        line=dict(color='blue')
    )
    line_pred = go.Scatter(
        x=y_test_dates,
        y=y_pred_dates,
        mode='lines+markers',
        name='Datas Preditas',
        line=dict(color='red', dash='dash')
    )
    layout = go.Layout(
        title='Datas Reais vs. Datas Preditas',
        xaxis=dict(title='Data Real'),
        yaxis=dict(title='Data Predita'),
        showlegend=True
    )
    fig = go.Figure(data=[line_real, line_pred], layout=layout)
    line_plot_html = pyo.plot(fig, output_type='div', include_plotlyjs=False)

    # Renderizando a página com os resultados
    return render(request, 'precatory/validacao/validacao_modelo_create.html', {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2,
        'line_plot_html': line_plot_html,
        'model_path': model_path
    })

def download_validacao_model(request):
    model_path = os.path.join(settings.MEDIA_ROOT, 'modelo_validacao_predicao.pkl')
    with open(model_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="modelo_validacao_predicao.pkl"'
        return response


def train_autuacao_model(request):
    # Busca os dados do banco de dados
    dados = autuacao.objects.all().values(
        'data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
        'classificacao_da_doenca', 'ente_devedor', 'unidade',
        'valor', 'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao'
    )
    df = pd.DataFrame.from_records(dados)

    # Pré-processamento dos dados
    df['data_da_criacao'] = pd.to_datetime(df['data_da_criacao']).astype('int64') / 10 ** 9
    df['data_de_nascimento'] = pd.to_datetime(df['data_de_nascimento']).astype('int64') / 10 ** 9
    df['data_da_validacao'] = pd.to_datetime(df['data_da_validacao']).astype('int64') / 10 ** 9
    df['data_da_autuacao'] = pd.to_datetime(df['data_da_autuacao']).astype('int64') / 10 ** 9
    df['tipo_de_pessoa'] = df['tipo_de_pessoa'].astype('category').cat.codes
    df['classificacao_da_doenca'] = df['classificacao_da_doenca'].astype('category').cat.codes

    # Removendo linhas com valores nulos na coluna target
    df = df.dropna(subset=['data_da_autuacao'])

    # Separando features e target
    X = df.drop('data_da_autuacao', axis=1)
    y = df['data_da_autuacao']

    # Dividindo os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Configurando o RandomForestRegressor com os melhores parâmetros
    modelo = RandomForestRegressor(
        bootstrap=False,
        max_depth=20,
        max_features='sqrt',
        min_samples_leaf=2,
        min_samples_split=10,
        n_estimators=200,
        random_state=42
    )

    # Treinando o modelo
    modelo.fit(X_train, y_train)

    # Salvar modelo
    model_path = os.path.join(settings.MEDIA_ROOT, 'modelo_autuacao_predicao.pkl')
    joblib.dump(modelo, model_path)

    # Fazendo previsões com o melhor modelo
    y_pred = modelo.predict(X_test)

    # Calculando métricas de desempenho
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    # Convertendo os valores numéricos de volta para datas
    y_test_dates = pd.to_datetime(y_test * 10 ** 9)  # Convertendo de segundos para datetime
    y_pred_dates = pd.to_datetime(modelo.predict(X_test) * 10 ** 9)  # Usando o melhor modelo

    # Gerando gráficos com Plotly
    # Gráfico de Linha (Valores Reais vs. Preditos)
    line_real = go.Scatter(
        x=y_test_dates,
        y=y_test_dates,
        mode='lines',
        name='Datas Reais',
        line=dict(color='blue')
    )
    line_pred = go.Scatter(
        x=y_test_dates,
        y=y_pred_dates,
        mode='lines+markers',
        name='Datas Preditas',
        line=dict(color='red', dash='dash')
    )
    layout = go.Layout(
        title='Datas Reais vs. Datas Preditas',
        xaxis=dict(title='Data Real'),
        yaxis=dict(title='Data Predita'),
        showlegend=True
    )
    fig = go.Figure(data=[line_real, line_pred], layout=layout)
    line_plot_html = pyo.plot(fig, output_type='div', include_plotlyjs=False)

    # Renderizando a página com os resultados
    return render(request, 'precatory/autuacao/autuacao_modelo_create.html', {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2,
        'line_plot_html': line_plot_html,
        'model_path': model_path
    })

def download_autuacao_model(request):
    model_path = os.path.join(settings.MEDIA_ROOT, 'modelo_autuacao_predicao.pkl')
    with open(model_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="modelo_autuacao_predicao.pkl"'
        return response


def train_baixa_model(request):
    # Busca os dados do banco de dados
    dados = baixa.objects.all().values(
        'data_da_criacao', 'tipo_de_pessoa', 'data_de_nascimento',
        'classificacao_da_doenca', 'ente_devedor', 'unidade',
        'valor', 'data_da_validacao', 'ano_de_orcamento', 'data_da_autuacao',
        'data_da_baixa'
    )
    df = pd.DataFrame.from_records(dados)

    # Pré-processamento dos dados
    df['data_da_criacao'] = pd.to_datetime(df['data_da_criacao']).astype('int64') / 10 ** 9
    df['data_de_nascimento'] = pd.to_datetime(df['data_de_nascimento']).astype('int64') / 10 ** 9
    df['data_da_validacao'] = pd.to_datetime(df['data_da_validacao']).astype('int64') / 10 ** 9
    df['data_da_autuacao'] = pd.to_datetime(df['data_da_autuacao']).astype('int64') / 10 ** 9
    df['data_da_baixa'] = pd.to_datetime(df['data_da_baixa']).astype('int64') / 10 ** 9
    df['tipo_de_pessoa'] = df['tipo_de_pessoa'].astype('category').cat.codes
    df['classificacao_da_doenca'] = df['classificacao_da_doenca'].astype('category').cat.codes

    # Removendo linhas com valores nulos na coluna target
    df = df.dropna(subset=['data_da_baixa'])

    # Separando features e target
    X = df.drop('data_da_baixa', axis=1)
    y = df['data_da_baixa']

    # Dividindo os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Configurando o RandomForestRegressor com os melhores parâmetros
    modelo = RandomForestRegressor(
        bootstrap=False,
        max_depth=20,
        max_features='sqrt',
        min_samples_leaf=1,
        min_samples_split=2,
        n_estimators=300,
        random_state=42
    )

    # Treinando o modelo
    modelo.fit(X_train, y_train)

    # Salvar modelo
    model_path = os.path.join(settings.MEDIA_ROOT, 'modelo_baixa_predicao.pkl')
    joblib.dump(modelo, model_path)

    # Fazendo previsões com o melhor modelo
    y_pred = modelo.predict(X_test)

    # Calculando métricas de desempenho
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    # Convertendo os valores numéricos de volta para datas
    y_test_dates = pd.to_datetime(y_test * 10 ** 9)  # Convertendo de segundos para datetime
    y_pred_dates = pd.to_datetime(modelo.predict(X_test) * 10 ** 9)  # Usando o melhor modelo

    # Gerando gráficos com Plotly
    # Gráfico de Linha (Valores Reais vs. Preditos)
    line_real = go.Scatter(
        x=y_test_dates,
        y=y_test_dates,
        mode='lines',
        name='Datas Reais',
        line=dict(color='blue')
    )
    line_pred = go.Scatter(
        x=y_test_dates,
        y=y_pred_dates,
        mode='lines+markers',
        name='Datas Preditas',
        line=dict(color='red', dash='dash')
    )
    layout = go.Layout(
        title='Datas Reais vs. Datas Preditas',
        xaxis=dict(title='Data Real'),
        yaxis=dict(title='Data Predita'),
        showlegend=True
    )
    fig = go.Figure(data=[line_real, line_pred], layout=layout)
    line_plot_html = pyo.plot(fig, output_type='div', include_plotlyjs=False)

    # Renderizando a página com os resultados
    return render(request, 'precatory/baixa/baixa_modelo_create.html', {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2,
        'line_plot_html': line_plot_html,
        'model_path': model_path
    })

def download_baixa_model(request):
    model_path = os.path.join(settings.MEDIA_ROOT, 'modelo_baixa_predicao.pkl')
    with open(model_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="modelo_baixa_predicao.pkl"'
        return response


def predicao_data_baixa(request):
    # Carregar os registros de ente_devedor e unidade
    entes_devedores = ente_devedor.objects.filter(ativo=True).order_by('nome')
    unidades = unidade.objects.filter(ativo=True).order_by('nome')

    if request.method == 'POST':
        # Carregar os modelos treinados
        caminho_modelo_validacao = os.path.join(settings.MEDIA_ROOT, 'modelo_validacao_predicao.pkl')
        if not os.path.exists(caminho_modelo_validacao):
            return HttpResponse("Modelo de validação não encontrado. Treine o modelo primeiro.", status=404)
        modelo_validacao = joblib.load(caminho_modelo_validacao)

        caminho_autuacao_baixa = os.path.join(settings.MEDIA_ROOT, 'modelo_autuacao_predicao.pkl')
        if not os.path.exists(caminho_autuacao_baixa):
            return HttpResponse("Modelo de autuação não encontrado. Treine o modelo primeiro.", status=404)
        modelo_autuacao = joblib.load(caminho_autuacao_baixa)

        caminho_modelo_baixa = os.path.join(settings.MEDIA_ROOT, 'modelo_baixa_predicao.pkl')
        if not os.path.exists(caminho_modelo_baixa):
            return HttpResponse("Modelo de baixa não encontrado. Treine o modelo primeiro.", status=404)
        modelo_baixa = joblib.load(caminho_modelo_baixa)

        # Coletar os dados do formulário
        dados_formulario = {
            'data_da_criacao': pd.to_datetime(request.POST['data_da_criacao']).timestamp(),
            'tipo_de_pessoa': request.POST['tipo_de_pessoa'],
            'data_de_nascimento': pd.to_datetime(request.POST['data_de_nascimento']).timestamp(),
            'classificacao_da_doenca': request.POST['classificacao_da_doenca'],
            'ente_devedor': int(request.POST['ente_devedor_id']),  # Usar o nome correto da feature
            'unidade': int(request.POST['unidade_id']),  # Usar o nome correto da feature
            'valor': float(request.POST['valor'])
        }

        # Fazer a predição da data de validação
        df = create_df(dados_formulario)
        predicao_timestamp = modelo_validacao.predict(df)[0]
        data_da_validacao = datetime.fromtimestamp(predicao_timestamp)

        # Fazer a predição da data de autuação
        dados_formulario['data_da_validacao'] = data_da_validacao.strftime('%Y-%m-%d')
        dados_formulario['ano_de_orcamento'] = data_da_validacao.year
        df = create_df(dados_formulario)
        predicao_timestamp = modelo_autuacao.predict(df)[0]
        data_da_autuacao = datetime.fromtimestamp(predicao_timestamp)

        # Fazer a predição da data de baixa
        dados_formulario['data_da_autuacao'] = data_da_autuacao.strftime('%Y-%m-%d')
        df = create_df(dados_formulario)
        predicao_timestamp = modelo_baixa.predict(df)[0]
        predicao_data_baixa = datetime.fromtimestamp(predicao_timestamp).strftime('%Y-%m-%d')

        # Renderizar a página com o resultado
        return render(request, 'precatory/resultado_predicao.html', {
            'predicao_data': predicao_data_baixa
        })

    # Renderizar o formulário com os registros carregados
    return render(request, 'precatory/predicao_data_baixa.html', {
        'entes_devedores': entes_devedores,
        'unidades': unidades,
    })

def create_df(dados_formulario):
    # Criar um DataFrame com os dados do formulário
    df = pd.DataFrame([dados_formulario])
    # Aplicar o mesmo pré-processamento usado no treinamento
    df['data_da_criacao'] = pd.to_datetime(df['data_da_criacao']).astype('int64') / 10 ** 9
    df['data_de_nascimento'] = pd.to_datetime(df['data_de_nascimento']).astype('int64') / 10 ** 9
    if 'data_da_validacao' in df.columns: df['data_da_validacao'] = pd.to_datetime(df['data_da_validacao']).astype('int64') / 10 ** 9
    if 'data_da_autuacao' in df.columns: df['data_da_autuacao'] = pd.to_datetime(df['data_da_autuacao']).astype('int64') / 10 ** 9
    return df