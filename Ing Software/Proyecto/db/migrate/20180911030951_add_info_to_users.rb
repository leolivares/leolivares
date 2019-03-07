class AddInfoToUsers < ActiveRecord::Migration[5.1]
  def change
    add_column :users, :name, :string, :null => false
    add_column :users, :reputation, :integer, :null => false, :default => 0
  end
end
