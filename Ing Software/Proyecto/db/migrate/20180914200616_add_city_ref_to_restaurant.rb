class AddCityRefToRestaurant < ActiveRecord::Migration[5.1]
  def change
    add_reference :restaurants, :city, foreign_key: true
  end
end
