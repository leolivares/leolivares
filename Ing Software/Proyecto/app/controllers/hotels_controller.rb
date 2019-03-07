class HotelsController < ApplicationController
  include Pagy::Backend
  before_action :set_hotel, only: %i[show edit update destroy]
  before_action :authenticate_user!, except: %i[manage destroy]
  before_action :authenticate_admin!, only: %i[manage destroy]

  # GET /hotels
  # GET /hotels.json
  def index
    @hotels = Hotel.all.order('nombre')
  end

  def manage
    @pagy, @hotels = pagy(Hotel.all)
  end

  # GET /hotels/1
  # GET /hotels/1.json
  def show
    preliminar_posts = HotelPost.select(:post_id).where(hotel_id: @hotel.id).map(&:post_id)
    @pagy, @posts = pagy(Post.where(id: preliminar_posts))
    @comments = pagy(Commentary.joins(:user).where(post_id: preliminar_posts).order('created_at DESC'))
    @likes = Like.distinct.where(post_id: preliminar_posts).count
    @dislikes = Dislike.distinct.where(post_id: preliminar_posts).count
    @points = @likes - @dislikes

    @post = Post.new
  end

  # GET /hotels/new
  def new
    @hotel = Hotel.new
  end

  def new_post
    @post = Post.create(title: params[:title], content: params[:content],
                        type_post: params[:type_post], reputation: 0, user_id: current_user.id,
                        upvote: 0, downvote: 0, image: params[:image])

    @hotel_post = HotelPost.create(post_id: @post.id, hotel_id: params[:id])

    redirect_to hotel_path(params[:id])
  end

  # GET /hotels/1/edit
  def edit; end

  # POST /hotels
  # POST /hotels.json
  def create
    @hotel = Hotel.new(hotel_params)

    respond_to do |format|
      if @hotel.save
        format.html { redirect_to @hotel, notice: 'Hotel was successfully created.' }
        format.json { render :show, status: :created, location: @hotel }
      else
        format.html { render :new }
        format.json { render json: @hotel.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /hotels/1
  # PATCH/PUT /hotels/1.json
  def update
    respond_to do |format|
      if @hotel.update(hotel_params)
        format.html { redirect_to @hotel, notice: 'Hotel was successfully updated.' }
        format.json { render :show, status: :ok, location: @hotel }
      else
        format.html { render :edit }
        format.json { render json: @hotel.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /hotels/1
  # DELETE /hotels/1.json
  def destroy
    @hotel.destroy
    respond_to do |format|
      format.html { redirect_to hotels_url, notice: 'Hotel was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_hotel
    @hotel = Hotel.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def hotel_params
    params.require(:hotel).permit(:city_id, :nombre, :reputation)
  end
end
