class CreateRequests < ActiveRecord::Migration[5.1]
  def change
    create_table :requests do |t|
      t.references :user, foreign_key: true
      t.references :country, foreign_key: true
      t.string :state
      t.string :reason

      t.timestamps
    end
  end
end
