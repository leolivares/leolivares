class CreateFavoriteSpots < ActiveRecord::Migration[5.1]
  def change
    create_table :favorite_spots do |t|
      t.references :turistic_spot,  foreign_key: true
      t.references :user,  foreign_key: true

      t.timestamps
    end
  end
end
