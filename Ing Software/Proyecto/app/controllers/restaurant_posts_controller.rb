class RestaurantPostsController < ApplicationController
  before_action :set_restaurant_post, only: %i[show edit update destroy]

  # GET /restaurant_posts
  # GET /restaurant_posts.json
  def index
    @restaurant_posts = RestaurantPost.all
  end

  # GET /restaurant_posts/1
  # GET /restaurant_posts/1.json
  def show; end

  # GET /restaurant_posts/new
  def new
    @restaurant_post = RestaurantPost.new
  end

  # GET /restaurant_posts/1/edit
  def edit; end

  # POST /restaurant_posts
  # POST /restaurant_posts.json
  def create
    @restaurant_post = RestaurantPost.new(restaurant_post_params)

    respond_to do |format|
      if @restaurant_post.save
        format.html { redirect_to @restaurant_post, notice: 'Restaurant post was successfully created.' }
        format.json { render :show, status: :created, location: @restaurant_post }
      else
        format.html { render :new }
        format.json { render json: @restaurant_post.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /restaurant_posts/1
  # PATCH/PUT /restaurant_posts/1.json
  def update
    respond_to do |format|
      if @restaurant_post.update(restaurant_post_params)
        format.html { redirect_to @restaurant_post, notice: 'Restaurant post was successfully updated.' }
        format.json { render :show, status: :ok, location: @restaurant_post }
      else
        format.html { render :edit }
        format.json { render json: @restaurant_post.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /restaurant_posts/1
  # DELETE /restaurant_posts/1.json
  def destroy
    @restaurant_post.destroy
    respond_to do |format|
      format.html { redirect_to restaurant_posts_url, notice: 'Restaurant post was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_restaurant_post
    @restaurant_post = RestaurantPost.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def restaurant_post_params
    params.require(:restaurant_post).permit(:restaurant_id)
  end
end
