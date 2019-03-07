class AddFkToCountryPost < ActiveRecord::Migration[5.1]
  def change
    add_reference :country_posts, :post, foreign_key: true
    add_reference :country_posts, :country, foreign_key: true
  end
end
