class AddCountryToUsers < ActiveRecord::Migration[5.1]
  def change
    add_reference :users, :country, foreign_key: true
  end
end
