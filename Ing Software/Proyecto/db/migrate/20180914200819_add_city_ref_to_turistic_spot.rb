class AddCityRefToTuristicSpot < ActiveRecord::Migration[5.1]
  def change
    add_reference :turistic_spots, :city, foreign_key: true
  end
end
