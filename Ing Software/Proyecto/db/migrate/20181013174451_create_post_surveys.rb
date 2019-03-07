class CreatePostSurveys < ActiveRecord::Migration[5.1]
  def change
    create_table :post_surveys do |t|
      
      t.timestamps
    end
  end
end
