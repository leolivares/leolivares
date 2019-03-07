class AnswersController < ApplicationController
  def create
    @answer = Answer.new(answer_params)
    @answer.save
    redirect_to survey_check_result_path survey_id: params[:survey_id]
  end

  def answer_params
    params.permit(:user_id, :responce_id)
  end
end
