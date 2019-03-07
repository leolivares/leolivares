class CreateRestaurantPosts < ActiveRecord::Migration[5.1]
  def change
    create_table :restaurant_posts do |t|
      t.integer :restaurant_id
      t.references :restaurant, foreign_key: true
      t.timestamps
    end
  end
end
