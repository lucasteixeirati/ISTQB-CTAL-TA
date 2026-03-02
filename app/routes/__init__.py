# app/routes/__init__.py

def register_routes(app):
    """Registra blueprints.

    Nota: o projeto tem rotas "fonte de verdade" em `app.py` (páginas e APIs principais).
    Aqui mantemos apenas o blueprint realmente usado pelo frontend atual: `/api/geracoes`.

    Blueprints legados (não usados / inconsistentes com o contrato atual) foram deixados
    desregistrados para evitar conflitos e manutenção confusa.
    """

    from .geracoes import geracoes_bp

    app.register_blueprint(geracoes_bp)

    # Legado (não registrar):
    # from .simulado import simulado_bp
    # from .flashcards import flashcards_bp
    # from .arquivos import arquivos_bp
    # app.register_blueprint(simulado_bp)
    # app.register_blueprint(flashcards_bp)
    # app.register_blueprint(arquivos_bp)
