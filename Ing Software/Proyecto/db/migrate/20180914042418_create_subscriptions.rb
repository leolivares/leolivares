class CreateSubscriptions < ActiveRecord::Migration[5.1]
  def change
    create_table :subscriptions do |t|
      t.references  :follower
      t.references  :followed

      t.timestamps
    end
    add_foreign_key :subscriptions, :users, column: :follower_id, primary_key: :id
    add_foreign_key :subscriptions, :users, column: :followed_id, primary_key: :id
  end
end
