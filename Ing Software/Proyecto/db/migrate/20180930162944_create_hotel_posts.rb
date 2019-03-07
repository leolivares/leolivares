class CreateHotelPosts < ActiveRecord::Migration[5.1]
  def change
    create_table :hotel_posts do |t|
      t.integer :hotel_id
      t.references :hotel, foreign_key: true

      t.timestamps
    end
  end
end
