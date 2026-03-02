from flask import Blueprint, jsonify

flashcards_bp = Blueprint('flashcards', __name__, url_prefix='/flashcards')

@flashcards_bp.route('/', methods=['GET'])
def get_flashcards():
    # Endpoint básico de teste
    return jsonify({'message': 'Flashcards endpoint funcionando!'})
