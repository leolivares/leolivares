class AddReferencesToTuristicSpotPost < ActiveRecord::Migration[5.1]
  def change
  	remove_column :turistic_spot_posts, :turistic_post_id
  	remove_column :turistic_spot_posts, :turistic_spot_id
  	add_reference :turistic_spot_posts, :post, foreign_key: true
    add_reference :turistic_spot_posts, :turistic_spot, foreign_key: true
  end
end
