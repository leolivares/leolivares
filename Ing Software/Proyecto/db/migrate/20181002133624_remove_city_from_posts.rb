class RemoveCityFromPosts < ActiveRecord::Migration[5.1]
  def change
    remove_column :posts, :city_id
  end
end
