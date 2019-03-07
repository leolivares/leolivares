class AddFkToPostSurveys < ActiveRecord::Migration[5.1]
  def change
    add_reference :post_surveys, :post, foreign_key: true
    add_reference :post_surveys, :survey, foreign_key: true
  end
end
