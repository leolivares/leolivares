class ResponcesController < ApplicationController
  before_action :authenticate_user!

  def new
    @survey = Survey.find(params[:survey_id])
    @question = Question.find(params[:question_id])
    @responce = @question.responces.build
  end

  def create
    @question = Question.find(params[:question_id])
    @responce = Responce.new(responce_params)

    if @survey.save
      redirect_to @survey, notice: 'Successfully created'
    else
      render :new
    end
  end

  private

  def question_params
    params.require(:responce).permit(:option, :question_id, :user_id)
  end
end
