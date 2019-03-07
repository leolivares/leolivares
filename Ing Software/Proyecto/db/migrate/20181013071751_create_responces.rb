class CreateResponces < ActiveRecord::Migration[5.1]
  def change
    create_table :responces do |t|
      t.string :option

      t.timestamps
    end
  end
end
