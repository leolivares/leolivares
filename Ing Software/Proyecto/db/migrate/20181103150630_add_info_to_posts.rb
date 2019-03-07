class AddInfoToPosts < ActiveRecord::Migration[5.1]
  def change
    add_column :posts, :info, :text
  end
end
