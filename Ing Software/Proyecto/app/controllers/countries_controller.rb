require 'rspotify'
require 'twitter'

# #PONER ESTO EN EL CONTROLER DE CADA TIPO DE POST
RSpotify.authenticate('41f0d4e46705491385b9912284775b99', '69be724bcfda406cba08620ebcc9ea02')
class CountriesController < ApplicationController
  include Pagy::Backend
  before_action :set_country, only: %i[show edit update destroy]
  before_action :authenticate_user!, except: %i[manage destroy]
  before_action :authenticate_admin!, only: %i[manage destroy]

  # GET /countries
  # GET /countries.json
  def index
    @countries = Country.all.order('name')
    if current_user
      @user_posts = Post.distinct.where(user_id: current_user.id).pluck(:id)
      @likes_p = Like.distinct.where(post_id: @user_posts).count
      @dislikes_p = Dislike.distinct.where(post_id: @user_posts).count
      @reputation = (@likes_p + @dislikes_p).zero? ? 0 : ((@likes_p.to_f / (@likes_p + @dislikes_p)) * 5).round(2)

      @complete_stars = @reputation.to_i
      @extra = (@reputation - @complete_stars)
      @half_star = @extra >= 0.5 && @complete_stars < 5 ? 1 : 0
      @empty_stars = 5 - (@complete_stars + @half_star)
    end
  end

  def manage
    @pagy, @countries = pagy(Country.all.order('name'))
  end

  # GET /countries/1
  # GET /countries/1.json
  def show
    preliminar_posts = CountryPost.select(:post_id).where(country_id: @country.id).map(&:post_id)
    @pagy, @posts = pagy(Post.where(id: preliminar_posts))
    @comments = pagy(Commentary.joins(:user).where(post_id: preliminar_posts).order('created_at DESC'))
    @likes = Like.distinct.where(post_id: preliminar_posts).count
    @dislikes = Dislike.distinct.where(post_id: preliminar_posts).count
    @points = @likes - @dislikes

    @client = Twitter::REST::Client.new do |config|
      config.consumer_key        = 'nhqxaRN8WpKGb1l1vJVuLYEhH'
      config.consumer_secret     = 'i0Edj9ySLUzCuNbHloSh16adsqR6E9rZjiBEEIhPLe1JlteUAm'
      config.access_token        = '1063801258987978752-uPj662UsJ67NXeWERjWqpXnvDico3b'
      config.access_token_secret = 'uPq1TnH19RsFFPfrbjo2BkpI7LvflhvA1Ra7iCRjT4siW'
    end

    # @playlists = RSpotify::Playlist.search('Indie')
    # @tracks = RSpotify::Track.search(@country.name)
    musica = "instrumental #{@country.name}"
    @tracks = RSpotify::Track.search(musica)
    @track = @tracks.first
    unless @track
      @tracks = RSpotify::Track.search('instrumental')
      @track = @tracks.first
    end

    @track.audio_features.danceability #=> 0.605
    @track.audio_features.energy #=> 0.768
    @track.audio_features.tempo #=> 100.209

    @moderator = false
    if current_user && current_user.category == 'moderator' && current_user.country_id == @country.id
      @moderator = true
    end

    @post = Post.new
  end

  # GET /countries/new
  def new
    @country = Country.new
  end

  # GET /countries/1/edit
  def edit; end

  # POST /countries
  # POST /countries.json
  def create
    @country = Country.new(country_params)

    respond_to do |format|
      if @country.save
        format.html { redirect_to @country, notice: 'Country was successfully created.' }
        format.json { render :show, status: :created, location: @country }
      else
        format.html { render :new }
        format.json { render json: @country.errors, status: :unprocessable_entity }
      end
    end
  end

  def new_post
    @post = Post.create(title: params[:title], content: params[:content],
                        type_post: params[:type_post], reputation: 0, user_id: current_user.id,
                        upvote: 0, downvote: 0, image: params[:image])
    @country_post = CountryPost.create(post_id: @post.id, country_id: params[:id])

    redirect_to country_path(params[:id])
  end

  # PATCH/PUT /countries/1
  # PATCH/PUT /countries/1.json
  def update
    respond_to do |format|
      if @country.update(country_params)
        format.html { redirect_to @country, notice: 'Country was successfully updated.' }
        format.json { render :show, status: :ok, location: @country }
      else
        format.html { render :edit }
        format.json { render json: @country.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /countries/1
  # DELETE /countries/1.json
  def destroy
    @country.destroy
    respond_to do |format|
      format.html { redirect_to countries_url, notice: 'Country was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_country
    @country = Country.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def country_params
    params.require(:country).permit(:name, :description, :subscribers, :latitude, :longitude)
  end
end
