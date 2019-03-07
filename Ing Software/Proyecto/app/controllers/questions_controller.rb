class QuestionsController < ApplicationController
  before_action :authenticate_user!

  def new
    @survey = Survey.find(params[:survey_id])
    @question = @survey.questions.build
  end

  def create
    @survey = Survey.find(params[:survey_id])
    @question = Question.new(question_params)

    if @survey.save
      redirect_to @survey, notice: 'Successfully created'
    else
      render :new
    end
  end

  private

  def question_params
    params.require(:question).permit(:title, :survey_id, :user_id)
  end
end
