class PostsController < ApplicationController
  protect_from_forgery with: :exception

  before_action :authenticate_any!, only: %i[edit update]
  before_action :require_permission, only: [:edit]
  before_action :authenticate_user!, except: %i[show edit delete index update]
  before_action :authenticate_admin!, only: [:index]
  before_action :set_post, only: %i[show edit update destroy]
  include Pagy::Backend

  def require_permission
    if current_user != Post.find(params[:id]).user
      unless admin_signed_in?
        redirect_to root_path
      end
    end
  end

  # GET /posts
  # GET /posts.json
  def index
    @posts = Post.all

    admins_pick = AdminPost.order('created_at DESC').limit(3).pluck(:post_id)
    @admin_posts = Post.where(id: admins_pick)
  end

  def searching
    @posts = Post.search(params[:search])
  end

  def searching_tags
    @posts = Post.search_tag(params[:search])
  end

  def tags
    tag = Tag.find_by(name: params[:name])
    @posts = tag.posts
  end

  # GET /posts/1
  # GET /posts/1.json
  def show
    @post = Post.where(id: params[:id])[0]
    if @post.info == ''
      @source_id = nil
    else
      @source_p = @post.info.split(': ')
      if @source_p[0] == 'Country'
        @source_id = CountryPost.where(post_id: @post.id).first.country_id
      elsif @source_p[0] == 'City'
        @source_id = CityPost.where(post_id: @post.id).first.city_id
      elsif @source_p[0] == 'Restaurant'
        @source_id = RestaurantPost.where(post_id: @post.id).first.restaurant_id
      elsif @source_p[0] == 'Hotel'
        @source_id = HotelPost.where(post_id: @post.id).first.hotel_id
      elsif @source_p[0] == 'POI'
        @source_id = TuristicSpotPost.where(post_id: @post.id).first.turistic_spot_id
      else
        @source_id = nil
      end
    end
    @survey = Survey.find(@post.content) if @post.type_post == 3

    @likes = Like.distinct.where(post_id: @post.id).count
    @dislikes = Dislike.distinct.where(post_id: @post.id).count
    @points = @likes - @dislikes

    @pagy_post, @comments = pagy(Commentary.joins(:user).where(post_id: @post.id).order('created_at DESC'))
    @comments_qty = Commentary.where(post_id: @post.id).count

    @comment_points = {}
    @comments.each do |com|
      @comments_likes = CommentLike.distinct.where(commentary_id: com.id).count
      @comments_dislikes = CommentDislike.distinct.where(commentary_id: com.id).count
      @comment_points[com.id] = @comments_likes - @comments_dislikes
    end
  end

  def new
    @post = Post.new
  end

  def admin_select
    @selected_posts = AdminPost.order('created_at DESC').limit(3)
    post_id = params[:id]

    already = false
    @selected_posts.each do |post|
      if post.post_id == post_id
        already = true
      end
    end

    unless already
      AdminPost.create(post_id: post_id)
    end
    redirect_to posts_path
  end

  def edit; end

  def create
    if current_user && current_user.active == 0
      render(:banned) && return
    end

    @post = Post.create(title: params[:post][:title], content: params[:post][:content],
                        type_post: params[:post][:type_post], reputation: 0,
                        user_id: current_user.id, image: params[:post][:image],
                        all_tags: params[:post][:all_tags], info: params[:post][:info])
    if @post.save
      if params[:post][:country_id].present?
        @country_post = CountryPost.create(post_id: @post.id, country_id: params[:post][:country_id])
        if params[:post][:type_post] == '3'
          redirect_to(new_survey_path(post_id: @post.id)) && return
        else
          redirect_to(country_path(params[:post][:country_id])) && return
        end

      elsif params[:post][:city_id].present?
        @city_post = CityPost.create(post_id: @post.id, city_id: params[:post][:city_id])
        if params[:post][:type_post] == '3'
          redirect_to(new_survey_path(post_id: @post.id)) && return
        else
          redirect_to(city_path(params[:post][:city_id])) && return
        end

      elsif params[:post][:hotel_id].present?
        @hotel_post = HotelPost.create(post_id: @post.id, hotel_id: params[:post][:hotel_id])
        if params[:post][:type_post] == '3'
          redirect_to(new_survey_path(post_id: @post.id)) && return
        else
          redirect_to(hotel_path(params[:post][:hotel_id])) && return
        end

      elsif params[:post][:restaurant_id].present?
        @restaurant_post = RestaurantPost.create(post_id: @post.id, restaurant_id: params[:post][:restaurant_id])
        if params[:post][:type_post] == '3'
          redirect_to(new_survey_path(post_id: @post.id)) && return
        else
          redirect_to(restaurant_path(params[:post][:restaurant_id])) && return
        end

      elsif params[:post][:turistic_spot_id].present?
        @turistic_spot_post = TuristicSpotPost.create(post_id: @post.id,
                                                      turistic_spot_id: params[:post][:turistic_spot_id])
        if params[:post][:type_post] == '3'
          redirect_to(new_survey_path(post_id: @post.id)) && return
        else
          redirect_to(turistic_spot_path(params[:post][:turistic_spot_id])) && return
        end
      else
        redirect_to(post_path(id: @post.id)) && return
      end

    else
      render(:new) && return

    end
  end

  def update
    respond_to do |format|
      if @post.update(post_params)
        format.html { redirect_to @post, notice: 'Post was successfully updated.' }
        format.json { render :show, status: :ok, location: @post }
      else
        format.html { render :edit }
        format.json { render json: @post.errors, status: :unprocessable_entity }
      end
    end
  end

  def delete
    post_id = params[:id]
    @post = Post.find(post_id)
    @post.destroy
    redirect_to country_path(params[:country_id])
  end

  def destroy
    @post.destroy
    respond_to do |format|
      format.html { redirect_to welcome_index_path, notice: 'Post was successfully destroyed.' }
      format.json { head :no_content }
    end
  end
  # end

  private

  def set_post
    @post = Post.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def post_params
    params.require(:post).permit(:user_id, :title, :content, :type_post,
                                 :reputation, :info, :image, :all_tags, :country_id, :created_at)
  end
end
