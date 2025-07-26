from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Definição do modelo de dados
class Tasks(db.Model): #db.Model é criar modelo de banco de dados
    id = db.Column(db.Integer, primary_key = True) 
    description = db.Column(db.String(100), unique=True, nullable=False)


# cRud
@app.route('/')
def index():
    tasks = Tasks.query.all() #retorna todos os itens salvos na tabela
    return render_template('index.html', tasks=tasks) 

#Crud
@app.route('/create', methods=["POST"]) #captura infos do formulario description, cadastra no bd, redireciona p tela inicial 
def create_Task():
    description = request.form['description']

    #valida se a tarefa foi cadastrada
    existing_task = Tasks.query.filter_by(description = description).first()
    if existing_task:
        return 'Erro: Essa task já existe! Tente um outro nome :)', 400

    new_task = Tasks(description = description)
    db.session.add(new_task) #adicionar nova linha no bd
    db.session.commit() #cadastrar realmente no bd
    return redirect('/')

# cruD
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_Task(task_id):
    task = Tasks.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

#crUd
@app.route('/update/<int:task_id>', methods=['POST'])
def update_Task(task_id):
    task = Tasks.query.get(task_id)

    if task:
        task.description = request.form['description']
        db.session.commit()
    return redirect('/')


if __name__ == '__main__': 
    with app.app_context():
        db.create_all() #criar o bd q ja foi definido no modelo de db.Model

    app.run(debug=True, port=5153) 
