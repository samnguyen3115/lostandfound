from flask import jsonify, request
from flask_login import login_required, current_user
from app.main import main_blueprint as bp_main
from app.main.models import Post, Tag
from app import db
import sqlalchemy as sqla

@bp_main.route('/api/posts', methods=['GET'])
@login_required
def api_get_posts():
    """API endpoint to get posts as JSON."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        color_filter = request.args.get('color')
        building_filter = request.args.get('building')
        status = request.args.get('status', 'lost')
        
        # Build query
        query = sqla.select(Post).where(Post.status == status).order_by(Post.timestamp.desc())
        
        if color_filter:
            query = query.join(Post.color_tag).where(Tag.name == color_filter)
        if building_filter:
            query = query.join(Post.building_tag).where(Tag.name == building_filter)
        
        # Paginate
        posts_pagination = db.paginate(query, page=page, per_page=per_page, error_out=False)
        posts = posts_pagination.items
        
        # Convert to JSON
        posts_data = []
        for post in posts:
            post_data = {
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'timestamp': post.timestamp.isoformat(),
                'status': post.status,
                'color_tag': post.color_tag.name if post.color_tag else None,
                'building_tag': post.building_tag.name if post.building_tag else None,
                'owner': post.writer.username,
                'has_image': post.image is not None
            }
            posts_data.append(post_data)
        
        return jsonify({
            'posts': posts_data,
            'pagination': {
                'page': posts_pagination.page,
                'pages': posts_pagination.pages,
                'per_page': posts_pagination.per_page,
                'total': posts_pagination.total,
                'has_next': posts_pagination.has_next,
                'has_prev': posts_pagination.has_prev
            }
        })
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch posts'}), 500

@bp_main.route('/api/tags', methods=['GET'])
@login_required
def api_get_tags():
    """API endpoint to get all tags."""
    try:
        color_tags = db.session.scalars(
            sqla.select(Tag).where(Tag.category == 'color').order_by(Tag.name)
        ).all()
        
        building_tags = db.session.scalars(
            sqla.select(Tag).where(Tag.category == 'building').order_by(Tag.name)
        ).all()
        
        return jsonify({
            'color_tags': [{'id': tag.id, 'name': tag.name} for tag in color_tags],
            'building_tags': [{'id': tag.id, 'name': tag.name} for tag in building_tags]
        })
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch tags'}), 500
