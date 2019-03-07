class CreateTuristicSpotPosts < ActiveRecord::Migration[5.1]
  def change
    create_table :turistic_spot_posts do |t|
      t.integer :turistic_post_id
      t.references :turistic_spot, foreign_key: true

      t.timestamps
    end
  end
end
