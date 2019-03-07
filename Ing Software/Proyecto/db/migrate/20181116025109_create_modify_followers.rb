class CreateModifyFollowers < ActiveRecord::Migration[5.1]
  def change
    create_table :modify_followers do |t|
      
      remove_column :followers, :follower_id
      add_column :followers, :follower_id, :bigint
      t.timestamps
    end
  end
end
