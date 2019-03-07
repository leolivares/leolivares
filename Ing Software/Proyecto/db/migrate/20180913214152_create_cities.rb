class CreateCities < ActiveRecord::Migration[5.1]
  def change
    create_table :cities do |t|
      t.references :country, foreign_key: true
      t.string :name
      t.text :description
      t.float :latitude
      t.float :longitude

      t.timestamps
    end
  end
end
