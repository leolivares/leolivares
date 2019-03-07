class TuristicSpotsController < ApplicationController
  include Pagy::Backend
  before_action :set_turistic_spot, only: %i[show edit update destroy]
  before_action :authenticate_user!, except: %i[manage destroy]
  before_action :authenticate_admin!, only: %i[manage destroy]

  # GET /turistic_spots
  # GET /turistic_spots.json

  def index
    @turistic_spots = TuristicSpot.all.order('nombre')
  end

  def manage
    @pagy, @turistic_spots = pagy(TuristicSpot.all)
  end

  # GET /turistic_spots/1
  # GET /turistic_spots/1.json
  def show
    preliminar_posts = TuristicSpotPost.select(:post_id).where(turistic_spot_id: @turistic_spot.id).map(&:post_id)
    @pagy, @posts = pagy(Post.where(id: preliminar_posts))
    @comments = pagy(Commentary.joins(:user).where(post_id: preliminar_posts).order('created_at DESC'))
    @likes = Like.distinct.where(post_id: preliminar_posts).count
    @dislikes = Dislike.distinct.where(post_id: preliminar_posts).count
    @points = @likes - @dislikes

    @post = Post.new
  end

  # GET /turistic_spots/new
  def new
    @turistic_spot = TuristicSpot.new
  end

  def new_post
    @post = Post.create(title: params[:title], content: params[:content], type_post: params[:type_post],
                        reputation: 0, user_id: current_user.id,
                        upvote: 0, downvote: 0, image: params[:image])

    @turistic_spot_post = TuristicSpotPost.create(post_id: @post.id, turistic_spot_id: params[:id])

    redirect_to turistic_spot_path(params[:id])
  end

  # GET /turistic_spots/1/edit
  def edit; end

  # POST /turistic_spots
  # POST /turistic_spots.json
  def create
    @turistic_spot = TuristicSpot.new(turistic_spot_params)

    respond_to do |format|
      if @turistic_spot.save
        format.html { redirect_to @turistic_spot, notice: 'Turistic spot was successfully created.' }
        format.json { render :show, status: :created, location: @turistic_spot }
      else
        format.html { render :new }
        format.json { render json: @turistic_spot.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /turistic_spots/1
  # PATCH/PUT /turistic_spots/1.json
  def update
    respond_to do |format|
      if @turistic_spot.update(turistic_spot_params)
        format.html { redirect_to @turistic_spot, notice: 'Turistic spot was successfully updated.' }
        format.json { render :show, status: :ok, location: @turistic_spot }
      else
        format.html { render :edit }
        format.json { render json: @turistic_spot.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /turistic_spots/1
  # DELETE /turistic_spots/1.json
  def destroy
    @turistic_spot.destroy
    respond_to do |format|
      format.html { redirect_to turistic_spots_url, notice: 'Turistic spot was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_turistic_spot
    @turistic_spot = TuristicSpot.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def turistic_spot_params
    params.require(:turistic_spot).permit(:city_id, :nombre, :reputation)
  end
end
