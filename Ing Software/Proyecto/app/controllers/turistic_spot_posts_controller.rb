class TuristicSpotPostsController < ApplicationController
  before_action :set_turistic_spot_post, only: %i[show edit update destroy]

  # GET /turistic_spot_posts
  # GET /turistic_spot_posts.json
  def index
    @turistic_spot_posts = TuristicSpotPost.all
  end

  # GET /turistic_spot_posts/1
  # GET /turistic_spot_posts/1.json
  def show; end

  # GET /turistic_spot_posts/new
  def new
    @turistic_spot_post = TuristicSpotPost.new
  end

  # GET /turistic_spot_posts/1/edit
  def edit; end

  # POST /turistic_spot_posts
  # POST /turistic_spot_posts.json
  def create
    @turistic_spot_post = TuristicSpotPost.new(turistic_spot_post_params)

    respond_to do |format|
      if @turistic_spot_post.save
        format.html { redirect_to @turistic_spot_post, notice: 'Turistic spot post was successfully created.' }
        format.json { render :show, status: :created, location: @turistic_spot_post }
      else
        format.html { render :new }
        format.json { render json: @turistic_spot_post.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /turistic_spot_posts/1
  # PATCH/PUT /turistic_spot_posts/1.json
  def update
    respond_to do |format|
      if @turistic_spot_post.update(turistic_spot_post_params)
        format.html { redirect_to @turistic_spot_post, notice: 'Turistic spot post was successfully updated.' }
        format.json { render :show, status: :ok, location: @turistic_spot_post }
      else
        format.html { render :edit }
        format.json { render json: @turistic_spot_post.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /turistic_spot_posts/1
  # DELETE /turistic_spot_posts/1.json
  def destroy
    @turistic_spot_post.destroy
    respond_to do |format|
      format.html { redirect_to turistic_spot_posts_url, notice: 'Turistic spot post was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_turistic_spot_post
    @turistic_spot_post = TuristicSpotPost.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def turistic_spot_post_params
    params.require(:turistic_spot_post).permit(:turistic_post_id)
  end
end
