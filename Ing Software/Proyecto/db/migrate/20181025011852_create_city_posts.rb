class CreateCityPosts < ActiveRecord::Migration[5.1]
  def change
    create_table :city_posts do |t|
      t.references :city, foreign_key: true
      t.references :post, foreign_key: true

      t.timestamps
    end
  end
end
