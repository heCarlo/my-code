# -*- coding: utf-8 -*-
import os, sys, traceback, logging, configparser
import xlsxwriter
from datetime import datetime, timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

def main(argv):
    greetings()

    # melhoria: substitur prints por logs estruturados
    print('press crtl+{0} to exit'.format('break' if os.name == 'nt' else 'c'))

    app = Flask(__name__)

    handler = RotatingFileHandler(
        'bot.log', maxBytes=10000, backupCount=1
    )  # maxbytes pode ser insuficiente para muitos logs, considerar aumentar o valor
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # url do banco de dados exposta diretamente no código. use variáveis de ambiente para melhorar a segurança
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'postgresql+psycopg2://postgres:123mudar@127.0.0.1:5432/bot_db'
    )  # substitua credenciais hardcoded por variáveis de ambiente
    db = SQLAlchemy(app)

    # o caminho do arquivo de configuração está fixo. isso pode causar problemas em outros ambientes
    config = configparser.ConfigParser()
    config.read(
        os.getenv('CONFIG_PATH', '/tmp/bot/settings/config.ini')
    )  # substitua por variável de ambiente

    try:
        var1 = int(config.get('scheduler', 'IntervalInMinutes'))
    except (configparser.Error, ValueError):
        app.logger.error("erro ao ler 'IntervalInMinutes' do arquivo de configuração")
        sys.exit(1)

    app.logger.warning(
        'intervalo entre as execuções do processo: {}'.format(var1)
    )

    scheduler = BlockingScheduler()

    # problema: task1 está sendo chamada imediatamente ao invés de ser agendada
    # correção: usar uma função lambda para passar a tarefa corretamente
    scheduler.add_job(lambda: task1(db), 'interval', id='task1_job', minutes=var1)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        app.logger.info('scheduler encerrado pelo usuário')
    except Exception as e:
        app.logger.error('erro inesperado: {}'.format(e), exc_info=True)

def greetings():
    # melhoria: substitur prints por logs estruturados
    print('             ##########################')
    print('             # - acme - tasks robot - #')
    print('             # - v 1.0 - 2020-07-28 - #')
    print('             ##########################')

def task1(db):
    # nome da função genérico, renomear para algo mais descritivo, como 'export_users_to_excel'
    file_name = 'data_export_{0}.xlsx'.format(datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"))
    file_path = os.path.join(os.path.curdir, file_name)

    workbook = None
    try:
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()

        # consulta sql crua é vulnerável a sql injection e pode ser substituída por orm com sqlalchemy
        orders = db.session.execute('SELECT * FROM users;')

        index = 0  # ajustar para usar índices numéricos

        headers = ['id', 'name', 'email', 'password', 'role id', 'created at', 'updated at']
        for col_num, header in enumerate(headers):
            worksheet.write(index, col_num, header)

        for order in orders:
            index += 1
            for col_num, value in enumerate(order):
                worksheet.write(index, col_num, value)

        workbook.close()
        print('job executed!') # melhoria: substitur prints por logs estruturados
    except Exception as e:
        logging.error("erro ao exportar dados: {}".format(e), exc_info=True)
    finally:
        if workbook and not workbook.fileclosed:
            workbook.close()

if __name__ == '__main__':
    main(sys.argv)
