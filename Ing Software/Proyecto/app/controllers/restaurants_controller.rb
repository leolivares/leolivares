class RestaurantsController < ApplicationController
  include Pagy::Backend
  before_action :set_restaurant, only: %i[show edit update destroy]
  before_action :authenticate_user!, except: %i[manage destroy]
  before_action :authenticate_admin!, only: %i[manage destroy]

  # GET /restaurants
  # GET /restaurants.json
  def index
    @restaurants = Restaurant.all.order('nombre')
  end

  def manage
    @pagy, @restaurants = pagy(Restaurant.all)
  end

  # GET /restaurants/1
  # GET /restaurants/1.json
  def show
    preliminar_posts = RestaurantPost.select(:post_id).where(restaurant_id: @restaurant.id).map(&:post_id)
    @pagy, @posts = pagy(Post.where(id: preliminar_posts))
    @comments = pagy(Commentary.joins(:user).where(post_id: preliminar_posts).order('created_at DESC'))
    @likes = Like.distinct.where(post_id: preliminar_posts).count
    @dislikes = Dislike.distinct.where(post_id: preliminar_posts).count
    @points = @likes - @dislikes

    @post = Post.new
  end

  # GET /restaurants/new
  def new
    @restaurant = Restaurant.new
  end

  def new_post
    @post = Post.create(title: params[:title], content: params[:content],
                        type_post: params[:type_post], reputation: 0, user_id: current_user.id,
                        upvote: 0, downvote: 0, image: params[:image])

    @restaurant_post = RestaurantPost.create(post_id: @post.id, restaurant_id: params[:id])

    redirect_to restaurant_path(params[:id])
  end

  # GET /restaurants/1/edit
  def edit; end

  # POST /restaurants
  # POST /restaurants.json
  def create
    @restaurant = Restaurant.new(restaurant_params)

    respond_to do |format|
      if @restaurant.save
        format.html { redirect_to @restaurant, notice: 'Restaurant was successfully created.' }
        format.json { render :show, status: :created, location: @restaurant }
      else
        format.html { render :new }
        format.json { render json: @restaurant.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /restaurants/1
  # PATCH/PUT /restaurants/1.json
  def update
    respond_to do |format|
      if @restaurant.update(restaurant_params)
        format.html { redirect_to @restaurant, notice: 'Restaurant was successfully updated.' }
        format.json { render :show, status: :ok, location: @restaurant }
      else
        format.html { render :edit }
        format.json { render json: @restaurant.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /restaurants/1
  # DELETE /restaurants/1.json
  def destroy
    @restaurant.destroy
    respond_to do |format|
      format.html { redirect_to restaurants_url, notice: 'Restaurant was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_restaurant
    @restaurant = Restaurant.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def restaurant_params
    params.require(:restaurant).permit(:city_id, :nombre, :reputation)
  end
end
