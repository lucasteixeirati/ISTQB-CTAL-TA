# app/routes/__init__.py

def register_routes(app):
    # Importar e registrar apenas blueprints existentes
    from .simulado import simulado_bp
    from .flashcards import flashcards_bp
    from .arquivos import arquivos_bp
    from .geracoes import geracoes_bp

    app.register_blueprint(simulado_bp)
    app.register_blueprint(flashcards_bp)
    app.register_blueprint(arquivos_bp)
    app.register_blueprint(geracoes_bp)
