class AddFkToSurveys < ActiveRecord::Migration[5.1]
  def change
    add_reference :surveys, :post, foreign_key: true
  end
end
