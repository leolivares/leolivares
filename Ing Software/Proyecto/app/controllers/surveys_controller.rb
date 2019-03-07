class SurveysController < ApplicationController
  before_action :authenticate_user!, except: %i[show index]

  def index
    @surveys = Survey.all
  end

  def show
    @survey = Survey.find(params[:id])
  end

  def edit; end

  def update
    @survey = @user.surveys.find(params[:id])
    if @survey.update(survey_params)
      redirect_to @survey, notice: 'Edit successful'
    else
      render :edit
    end
  end

  def new
    @survey = Survey.new
  end

  def create
    @survey = current_user.surveys.build(survey_params)
    if @survey.save
      @survey.post.update_content(@survey.id)
      redirect_to @survey, notice: 'Successfully created'
    else
      render :new

    end
  end

  def check_result
    @vote_count ||= []

    @survey = Survey.find(params[:survey_id])
    @questions = Question.where('survey_id = ?', params[:survey_id])
    @questions.each do |question|
      @responces = Responce.where('question_id = ?', question.id)
      @responces.each do |responce|
        vote_n = Answer.where('responce_id = ?', responce.id).count
        @vote_count << vote_n
      end
    end
  end

  def destroy
    @survey = Survey.find(params[:id]).destroy
    redirect_to surveys_path, notice: 'successfully deleted'
  end

  private

  def survey_params
    params.require(:survey).permit(:post_id,
                                   questions_attributes: [:id, :title,
                                                          responces_attributes: %i[id option]])
  end
end
