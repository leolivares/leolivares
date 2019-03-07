class AddReferencesToHotelPost < ActiveRecord::Migration[5.1]
  def change
  	remove_column :hotel_posts, :hotel_id
  	add_reference :hotel_posts, :post, foreign_key: true
    add_reference :hotel_posts, :survey, foreign_key: true
  end
end
