class AddReferencesToRestaurantPost < ActiveRecord::Migration[5.1]
  def change
  	remove_column :restaurant_posts, :restaurant_id
  	add_reference :restaurant_posts, :post, foreign_key: true
    add_reference :restaurant_posts, :restaurant, foreign_key: true
  end
end
