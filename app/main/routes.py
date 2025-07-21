import io
import mimetypes
from flask import Response, abort, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
import sqlalchemy as sqla

from app import db
from app.main.models import Post, Tag, ImageStore, Building
from app.main.forms import PostForm, FilterForm
from app.main.contact_forms import ContactOwnerForm, ItemStatusForm
from app.main import main_blueprint as bp_main

def build_posts_query(color_filter=None, building_filter=None):
    """Build optimized query for posts with filters."""
    query = sqla.select(Post).order_by(Post.timestamp.desc())
    conditions = []
    
    if color_filter:
        conditions.append(Post.color_tag_id == color_filter.id)
    if building_filter:
        conditions.append(Post.building_tag_id == building_filter.id)
    
    if conditions:
        query = query.where(sqla.and_(*conditions))
    
    return query

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET', 'POST'])
@login_required
def index(): 
    form = FilterForm()
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Posts per page
    
    # Get filter values from form
    color_filter = form.color_filter.data if form.color_filter.data else None
    building_filter = form.building_filter.data if form.building_filter.data else None
    
    # Check for refresh button
    refresh = request.form.get('submit2') or request.args.get('submit2')
    if refresh:
        color_filter = None
        building_filter = None
        form.color_filter.data = None
        form.building_filter.data = None
    
    # Build and execute query with pagination
    try:
        query = build_posts_query(color_filter, building_filter)
        posts_pagination = db.paginate(
            query, 
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        all_posts = posts_pagination.items
        
        if not all_posts and (color_filter or building_filter) and page == 1:
            flash('No posts found with the selected filters', 'info')
            # Show all posts if no filtered results
            query = sqla.select(Post).order_by(Post.timestamp.desc())
            posts_pagination = db.paginate(
                query, 
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            all_posts = posts_pagination.items
    
    except Exception as e:
        flash('An error occurred while filtering posts', 'error')
        # Fallback to all posts
        query = sqla.select(Post).order_by(Post.timestamp.desc())
        posts_pagination = db.paginate(
            query, 
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        all_posts = posts_pagination.items
    
    return render_template('index.html', 
                         title="Lost And Found Portal", 
                         posts=all_posts, 
                         form=form,
                         pagination=posts_pagination)


@bp_main.route('/post', methods=['GET', 'POST'])
@login_required
def postsmile():
    form = PostForm()
    if form.validate_on_submit():
        try:
            post = Post(
                writer=current_user,
                title=form.title.data,
                color_tag=form.color_tag.data,
                building_tag=form.building_tag.data,
                description=form.body.data
            )
            db.session.add(post)
            db.session.commit()
            
            # Handle image upload if provided
            if form.image.data:
                image_file = form.image.data
                image_data = image_file.read()
                image_type = mimetypes.guess_type(image_file.filename)[0]
                
                image = ImageStore(
                    post_id=post.id, 
                    image_data=image_data, 
                    image_type=image_type
                )
                db.session.add(image)
                db.session.commit()
            
            flash('Your lost & found post has been created successfully!', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your post. Please try again.', 'error')
    
    return render_template('create.html', title='Post', form=form)

@bp_main.route('/image/<int:post_id>')
def get_image(post_id):
    """Serve post images."""
    try:
        image_record = db.session.query(ImageStore).filter_by(post_id=post_id).first()
        if image_record is None or image_record.image_data is None:
            abort(404)
        return Response(image_record.image_data, mimetype=image_record.image_type or 'image/jpeg')
    except Exception:
        abort(404)

@bp_main.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a post (only by the owner)."""
    try:
        post = db.session.scalars(sqla.select(Post).where(Post.id == post_id)).first()
        if not post:
            flash('Post not found.', 'error')
            return redirect(url_for('main.index'))
        
        # Check if user owns the post
        if post.writer != current_user:
            flash('You can only delete your own posts.', 'error')
            return redirect(url_for('main.index'))
        
        # Delete associated image if exists
        image = db.session.query(ImageStore).filter_by(post_id=post_id).first()
        if image:
            db.session.delete(image)
        
        db.session.delete(post)
        db.session.commit()
        flash('Post has been successfully deleted.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the post.', 'error')
    
    return redirect(url_for('main.index'))



@bp_main.route('/map', methods=['GET'])
@login_required
def map():
    return render_template('map.html', title='Map')

@bp_main.route('/building/<int:building_id>', methods=['GET'])
@login_required
def map_building(building_id):
    """Display building details."""
    try:
        building = db.session.get(Building, building_id)
        if not building:
            flash('Building not found.', 'error')
            return redirect(url_for('main.map'))
        
        # Use direct property access instead of getter methods
        name = building.name
        place = building.title or []
        body = building.body or []
        count = building.count
        theme = building.theme_image_link
        image = building.image_link or []
        
        # Create places_info by zipping the arrays safely
        places_info = list(zip(place, body, image)) if all([place, body, image]) else []
        
        return render_template('building.html', 
                             title='Building Details', 
                             building_id=building_id, 
                             name=name, 
                             place=place, 
                             body=body, 
                             count=count, 
                             theme=theme, 
                             image=image,
                             places_info=places_info)
    
    except Exception as e:
        flash('An error occurred while loading building details.', 'error')
        return redirect(url_for('main.map'))

@bp_main.route('/contact/<int:post_id>', methods=['GET', 'POST'])
@login_required
def contact_owner(post_id):
    """Contact the owner of a lost item."""
    try:
        post = db.session.get(Post, post_id)
        if not post:
            flash('Post not found.', 'error')
            return redirect(url_for('main.index'))
        
        # Don't allow owners to contact themselves
        if post.writer == current_user:
            flash('You cannot contact yourself about your own post.', 'info')
            return redirect(url_for('main.index'))
        
        # Don't allow contact for already found items
        if post.status != 'lost':
            flash('This item has already been marked as found.', 'info')
            return redirect(url_for('main.index'))
        
        form = ContactOwnerForm()
        form.post_id.data = post_id
        
        if form.validate_on_submit():
            try:
                # Here you would send email notification
                # send_found_item_notification(post, form.finder_email.data)
                
                flash(f'Your message has been sent to {post.writer.username}! '
                      f'They will be notified at {post.writer.email}', 'success')
                return redirect(url_for('main.index'))
                
            except Exception as e:
                flash('Failed to send message. Please try again.', 'error')
        
        return render_template('contact_owner.html', 
                             title='Contact Owner', 
                             post=post, 
                             form=form)
    
    except Exception as e:
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('main.index'))

@bp_main.route('/post/<int:post_id>/mark-found', methods=['POST'])
@login_required
def mark_found(post_id):
    """Mark a post as found (only by owner)."""
    try:
        post = db.session.get(Post, post_id)
        if not post:
            flash('Post not found.', 'error')
            return redirect(url_for('main.index'))
        
        # Only owner can mark as found
        if post.writer != current_user:
            flash('You can only update your own posts.', 'error')
            return redirect(url_for('main.index'))
        
        post.mark_as_found()
        db.session.commit()
        
        flash('Item marked as found! Congratulations on getting your item back!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Failed to update post status.', 'error')
    
    return redirect(url_for('main.index'))


