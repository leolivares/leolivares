class CitiesController < ApplicationController
  include Pagy::Backend
  before_action :set_city, only: %i[show edit update destroy]
  before_action :authenticate_user!, except: %i[manage destroy]
  before_action :authenticate_admin!, only: %i[manage destroy]

  # GET /cities
  # GET /cities.json
  def index
    @cities = City.all.order('name')
  end

  def manage
    @pagy, @cities = pagy(City.all)
  end

  # GET /cities/1
  # GET /cities/1.json
  def show
    preliminar_posts = CityPost.select(:post_id).where(city_id: @city.id).map(&:post_id)
    @pagy, @posts = pagy(Post.where(id: preliminar_posts))
    @comments = pagy(Commentary.joins(:user).where(post_id: preliminar_posts).order('created_at DESC'))
    @likes = Like.distinct.where(post_id: preliminar_posts).count
    @dislikes = Dislike.distinct.where(post_id: preliminar_posts).count
    @points = @likes - @dislikes

    @post = Post.new
  end

  # GET /cities/new
  def new
    @city = City.new
  end

  def new_post
    @post = Post.create(title: params[:title], content: params[:content],
                        type_post: params[:type_post], reputation: 0, user_id: current_user.id,
                        upvote: 0, downvote: 0, image: params[:image])

    @city_post = CityPost.create(post_id: @post.id, city_id: params[:id])

    redirect_to city_path(params[:id])
  end

  # GET /cities/1/edit
  def edit; end

  # POST /cities
  # POST /cities.json
  def create
    @city = City.new(city_params)

    respond_to do |format|
      if @city.save
        format.html { redirect_to @city, notice: 'City was successfully created.' }
        format.json { render :show, status: :created, location: @city }
      else
        format.html { render :new }
        format.json { render json: @city.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /cities/1
  # PATCH/PUT /cities/1.json
  def update
    respond_to do |format|
      if @city.update(city_params)
        format.html { redirect_to @city, notice: 'City was successfully updated.' }
        format.json { render :show, status: :ok, location: @city }
      else
        format.html { render :edit }
        format.json { render json: @city.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /cities/1
  # DELETE /cities/1.json
  def destroy
    @city.destroy
    respond_to do |format|
      format.html { redirect_to cities_url, notice: 'City was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_city
    @city = City.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def city_params
    params.require(:city).permit(:country_id, :name, :description, :latitude, :longitude)
  end
end
