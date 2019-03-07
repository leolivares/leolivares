class CreateHotels < ActiveRecord::Migration[5.1]
  def change
    create_table :hotels do |t|
      t.text :nombre
      t.float :reputation, default: 0

      t.timestamps
    end
  end
end
