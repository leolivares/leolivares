class CommentariesController < ApplicationController
  before_action :authenticate_user!, except: [:index]
  before_action :authenticate_admin!, only: [:index]

  # GET /commentaries
  # GET /commentaries.json
  def index
    @commentaries = Commentary.all
  end

  # GET /commentaries/1
  # GET /commentaries/1.json
  def show; end

  # GET /commentaries/new
  def new
    @commentary = Commentary.new
  end

  # GET /commentaries/1/edit
  def edit; end

  # POST /commentaries
  # POST /commentaries.json
  def create
    @commentary = Commentary.new(commentary_params)

    respond_to do |format|
      if @commentary.save
        format.html { redirect_to @commentary, notice: 'Commentary was successfully created.' }
        format.json { render :show, status: :created, location: @commentary }
      else
        format.html { render :new }
        format.json { render json: @commentary.errors, status: :unprocessable_entity }
      end
    end
  end

  def comment_post
    comment = Commentary.create(user_id: current_user.id, post_id: params[:post_id], content: params[:comment])
    comment.save

    @commentaries = Commentary.all

    redirect_to post_path(params[:post_id])
  end

  # PATCH/PUT /commentaries/1
  # PATCH/PUT /commentaries/1.json
  def update
    respond_to do |format|
      if @commentary.update(commentary_params)
        format.html { redirect_to @commentary, notice: 'Commentary was successfully updated.' }
        format.json { render :show, status: :ok, location: @commentary }
      else
        format.html { render :edit }
        format.json { render json: @commentary.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /commentaries/1
  # DELETE /commentaries/1.json

  def destroy
    @commentary.destroy
    respond_to do |format|
      format.html { redirect_to @commentary.post, notice: 'Comment was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  # def destroy
  #    @commentary.destroy
  #    respond_to do |format|
  #      format.html { redirect_to commentaries_url, notice: 'Commentary was successfully destroyed.' }
  #      format.json { head :no_content }
  #    end
  #  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_commentary
    @commentary = Commentary.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def commentary_params
    params.require(:commentary).permit(:user_id, :content, :reputation)
  end
end
