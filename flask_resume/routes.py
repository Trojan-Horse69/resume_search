from flask import Blueprint, render_template, request, jsonify, current_app

bp = Blueprint('resume', __name__)

@bp.route("/home")
def index():
    return render_template('index.html') 

@bp.route('/search', methods=['POST'])
def search():
    data = request.get_json()

    if not data or 'user_input' not in data:
        return jsonify(error='Invalid request'), 400

    user_input = data.get('user_input')

    try:
        vectorstore = current_app.vectorstore

        docs = vectorstore.similarity_search(user_input, k=3)
        
        sources = [doc.metadata.get("source") for doc in docs if doc.metadata.get("source")]
        unique_sources = list(set(sources))
        
        output = "These are the top resumes that meet your needs: " + ", ".join(unique_sources)

        # Log the unique sources for debugging
        current_app.logger.info(output)
        
        return jsonify({"response": True, "message": output})
    
    except Exception as e:
        error_message = f'An error occurred: {str(e)}'
        current_app.logger.error(error_message)
        return jsonify({"response": False, "message": error_message})
