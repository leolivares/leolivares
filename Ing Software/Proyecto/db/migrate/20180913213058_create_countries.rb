class CreateCountries < ActiveRecord::Migration[5.1]
  def change
    create_table :countries do |t|
      t.string :name
      t.text :description
      t.integer :subscribers
      t.float :latitude
      t.float :longitude

      t.timestamps
    end
  end
end
