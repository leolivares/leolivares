class FavoriteSpotsController < ApplicationController
  before_action :set_favorite_spot, only: %i[show edit update destroy]

  # GET /favorite_spots
  # GET /favorite_spots.json
  def index
    @favorite_spots = FavoriteSpot.all
  end

  # GET /favorite_spots/1
  # GET /favorite_spots/1.json
  def show; end

  # GET /favorite_spots/new
  def new
    @favorite_spot = FavoriteSpot.new
  end

  # GET /favorite_spots/1/edit
  def edit; end

  # POST /favorite_spots
  # POST /favorite_spots.json
  def create
    @favorite_spot = FavoriteSpot.new(favorite_spot_params)

    respond_to do |format|
      if @favorite_spot.save
        format.html { redirect_to @favorite_spot, notice: 'Favorite spot was successfully created.' }
        format.json { render :show, status: :created, location: @favorite_spot }
      else
        format.html { render :new }
        format.json { render json: @favorite_spot.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /favorite_spots/1
  # PATCH/PUT /favorite_spots/1.json
  def update
    respond_to do |format|
      if @favorite_spot.update(favorite_spot_params)
        format.html { redirect_to @favorite_spot, notice: 'Favorite spot was successfully updated.' }
        format.json { render :show, status: :ok, location: @favorite_spot }
      else
        format.html { render :edit }
        format.json { render json: @favorite_spot.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /favorite_spots/1
  # DELETE /favorite_spots/1.json
  def destroy
    @favorite_spot.destroy
    respond_to do |format|
      format.html { redirect_to favorite_spots_url, notice: 'Favorite spot was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_favorite_spot
    @favorite_spot = FavoriteSpot.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def favorite_spot_params
    params.require(:favorite_spot).permit(:user_id, :turistic_spot_id)
  end
end
