class AddTypeAndReputation < ActiveRecord::Migration[5.1]
  def change
    add_column :posts, :type_post, :integer, default: 0
    add_column :posts, :reputation, :float, default: 0
  end
end
