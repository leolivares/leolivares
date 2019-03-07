class AddMoreReferencesToHotelPost < ActiveRecord::Migration[5.1]
  def change
  	remove_column :hotel_posts, :survey_id
  	add_reference :hotel_posts, :hotel, foreign_key: true
  end
end
