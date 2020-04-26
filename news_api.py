from flask import jsonify, Blueprint, request
from data import db_session, users, news

blueprint = Blueprint("news_api", __name__, template_folder="templates")


@blueprint.route("/api/news")
def get_news():
    session = db_session.create_session()
    new = session.query(news.News).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=("title", "content", "user.name")) for item in new]
        }
    )


@blueprint.route("/api/news/<int:news_id>", methods=["GET"])
def get_one_news(news_id):
    session = db_session.create_session()
    new = session.query(news.News).get(news_id)
    if not new:
        return jsonify({"error": "Not found"})
    return jsonify(
        {
            "news": new.to_dict(only=("title", "content", "user_id", "is_private"))
        }
    )


@blueprint.route("/api/news", methods=["POST"])
def create_news():
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(key in request.json for key in ["title", "content", "user_id", "is_private"]):
        return jsonify({"error": "Bad request"})
    session = db_session.create_session()
    new = news.News(
        title=request.json['title'],
        content=request.json["content"],
        user_id=request.json["user_id"],
        is_private=request.json["is_private"]
    )
    session.add(new)
    session.commit()
    return jsonify({"success": "OK"})


@blueprint.route("/api/news/<int:id>", methods=["DELETE"])
def delete_news(news_id):
    session = db_session.create_session()
    new = session.query(news.News).get(news_id)
    if not new:
        return jsonify({"error": "Not found"})
    session.delete(new)
    session.commit()
    return jsonify({"success": "OK"})