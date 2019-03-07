class AddFKtoSurveys < ActiveRecord::Migration[5.1]
  def change
    add_reference :responces, :question, foreign_key: true
    add_reference :questions, :survey, foreign_key: true
    add_reference :surveys, :user, foreign_key: true
    add_reference :answers, :user, foreign_key: true
    add_reference :answers, :responce, foreign_key: true
  end
end
