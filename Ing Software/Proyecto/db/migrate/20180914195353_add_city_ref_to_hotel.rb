class AddCityRefToHotel < ActiveRecord::Migration[5.1]
  def change
    add_reference :hotels, :city, foreign_key: true
  end
end
