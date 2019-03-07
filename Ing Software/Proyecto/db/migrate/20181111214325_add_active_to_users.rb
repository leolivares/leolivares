class AddActiveToUsers < ActiveRecord::Migration[5.1]
  def change
  	add_column :users, :active, :integer, :default => 1
  end
end
