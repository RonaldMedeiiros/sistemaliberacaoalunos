from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.models import Usuario, Aluno
from app.forms import LoginForm, CadastroForm
from app import db
import base64

# Criação do blueprint
bp = Blueprint('main', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Bem-vindo, {user.username}!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        # Verificar se o usuário já existe
        existing_user = Usuario.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('O username já está em uso. Escolha outro.', 'danger')
            return redirect(url_for('main.cadastro'))
        
        # Criar um novo usuário
        new_user = Usuario(
            username=form.username.data,
            role=form.role.data
        )
        new_user.set_password(form.password.data)  # Criptografar a senha
        db.session.add(new_user)
        db.session.commit()
        
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('cadastro.html', form=form)

@bp.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html', username=session['username'])
    else:
        flash('Você precisa fazer login primeiro.', 'warning')
        return redirect(url_for('main.login'))

@bp.route('/cadastrar_aluno', methods=['GET'])
def cadastrar_aluno():
    return render_template('cadastro_aluno.html')


@bp.route('/buscar', methods=['GET'])
def buscar_aluno():
    termo_busca = request.args.get('nome_aluno', '').strip()
    print(f"Termo buscado: {termo_busca}")  # Log para depuração
    
    if not termo_busca:
        flash('Por favor, insira um nome ou RA para buscar.', 'warning')
        return redirect(url_for('main.home'))
    
    # Busca pelo nome ou RA
    alunos = Aluno.query.filter(
        (Aluno.nome_completo.ilike(f'%{termo_busca}%')) | (Aluno.ra.ilike(f'%{termo_busca}%'))
    ).all()
    print(f"Alunos encontrados: {alunos}")  # Log para verificar o retorno da consulta
    
    if not alunos:
        flash(f'Nenhum aluno encontrado para "{termo_busca}".', 'warning')
        return redirect(url_for('main.home'))

    return render_template('resultado_busca.html', alunos=alunos)



@bp.route('/salvar_aluno', methods=['POST'])
def salvar_aluno():
    nome_completo = request.form.get('nome_completo', '').strip()
    ra = request.form.get('ra', '').strip()
    email = request.form.get('email', '').strip()
    matricula = request.form.get('matricula', '').strip()
    turno = request.form.get('turno', '').strip()
    foto = request.files.get('foto')  # Arquivo de foto

    # Validações básicas
    if not nome_completo or not ra:
        flash('Nome completo e RA são obrigatórios.', 'danger')
        return redirect(url_for('main.cadastrar_aluno'))

    # Verificar se o RA já existe
    if Aluno.query.filter_by(ra=ra).first():
        flash(f'Já existe um aluno cadastrado com o RA {ra}.', 'danger')
        return redirect(url_for('main.cadastrar_aluno'))

    # Processar a foto (se existir)
    foto_bytes = None
    if foto:
        foto_bytes = foto.read()  # Converte o arquivo para bytes

    # Salvar no banco de dados
    novo_aluno = Aluno(
        nome_completo=nome_completo,
        ra=ra,
        email=email,
        foto=foto_bytes,
        matricula=matricula,
        turno=turno
    )
    db.session.add(novo_aluno)
    db.session.commit()

    flash('Aluno cadastrado com sucesso!', 'success')
    return redirect(url_for('main.home'))


@bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('main.login'))