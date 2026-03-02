from flask import Flask

# Inicialização do app Flask
app = Flask(__name__)

# Importação das rotas (serão criadas em seguida)
from app.routes import register_routes
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
