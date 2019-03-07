class HotelPostsController < ApplicationController
  before_action :set_hotel_post, only: %i[show edit update destroy]

  # GET /hotel_posts
  # GET /hotel_posts.json
  def index
    @hotel_posts = HotelPost.all
  end

  # GET /hotel_posts/1
  # GET /hotel_posts/1.json
  def show; end

  # GET /hotel_posts/new
  def new
    @hotel_post = HotelPost.new
  end

  # GET /hotel_posts/1/edit
  def edit; end

  # POST /hotel_posts
  # POST /hotel_posts.json
  def create
    @hotel_post = HotelPost.new(hotel_post_params)

    respond_to do |format|
      if @hotel_post.save
        format.html { redirect_to @hotel_post, notice: 'Hotel post was successfully created.' }
        format.json { render :show, status: :created, location: @hotel_post }
      else
        format.html { render :new }
        format.json { render json: @hotel_post.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /hotel_posts/1
  # PATCH/PUT /hotel_posts/1.json
  def update
    respond_to do |format|
      if @hotel_post.update(hotel_post_params)
        format.html { redirect_to @hotel_post, notice: 'Hotel post was successfully updated.' }
        format.json { render :show, status: :ok, location: @hotel_post }
      else
        format.html { render :edit }
        format.json { render json: @hotel_post.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /hotel_posts/1
  # DELETE /hotel_posts/1.json
  def destroy
    @hotel_post.destroy
    respond_to do |format|
      format.html { redirect_to hotel_posts_url, notice: 'Hotel post was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_hotel_post
    @hotel_post = HotelPost.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def hotel_post_params
    params.require(:hotel_post).permit(:hotel_id)
  end
end
