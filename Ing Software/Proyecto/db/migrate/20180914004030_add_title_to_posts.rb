class AddTitleToPosts < ActiveRecord::Migration[5.1]
  def change
    add_column :posts, :title, :text
    add_reference :posts, :city, foreign_key: true
  end
end
