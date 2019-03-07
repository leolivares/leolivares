Rails.application.routes.draw do
  resources :moderators
  #resources :requests
  resources :requests do
    member do
    get "aceptar" => "requests#aceptar"
    end
  end

  get 'countries/manage' => 'countries#manage'
  get 'cities/manage' => 'cities#manage'
  get 'restaurants/manage' => 'restaurants#manage'
  get 'turistic_spots/manage' => 'turistic_spots#manage'
  get 'hotels/manage' => 'hotels#manage'
  resources :restaurant_posts
  resources :turistic_spot_posts
  resources :hotel_posts
  devise_for :admins
  resources :surveys do
    get 'check_result'
  end
  resources :questions
  resources :answers, defaults: { format: 'json' }
  get 'user_status/index'

  resources :favorite_spots

  resources :subscriptions
  resources :turistic_spots
  resources :restaurants
  resources :hotels
  resources :cities
  resources :countries
  resources :commentaries
  resources :hotel_posts
  resources :restaurant_posts
  resources :turistic_spot_posts
  resources :posts
  resources :answers, only: [:create]

  devise_for :users, :controllers => { registrations: 'registrations' }

  get 'users/new'



  get 'welcome/index'
  get 'user_status/index'

  get 'admin' => 'admin#home'
  get 'admin/users'
  get 'admin/stats'

  get 'searching' => 'posts#searching', as: 'search_posts'

  get '/posts/tag/:name', to:'posts#tags'

  get 'searching' => 'posts#searching_tags', as: 'search_tags'

  get '/users' => 'welcome#index', as: 'index'

  get  '/users' => 'posts#destroy', as: 'deleting'

  get 'users/:id' => 'users#show', as: :show_profile
  get 'likes' => 'likes#show', as: :show_likes
  get 'dislikes' => 'dislikes#show', as: :show_dislikes
  get 'favorites' => 'favorite_posts#show', as: :show_favorites
  post 'like/users/:user_id/posts/:post_id' => 'likes#update', as: :update_likes
  post 'dislike/users/:user_id/posts/:post_id' => 'dislikes#update', as: :update_dislikes
  post 'favorite/users/:user_id/posts/:post_id' => 'favorite_posts#update', as: :update_fav

  post 'comment/post/:post_id/users/:user_id' => 'commentaries#comment_post', as: :make_comment
  post 'like/comment/:user_id/:comment_id' => 'comment_likes#update', as: :update_comment_likes
  post 'dislike/comment/:user_id/:comment_id' => 'comment_dislikes#update', as: :update_comment_dislikes

  post 'countries/:id' => 'countries#new_post', as: :country_new_post
  post 'cities/:id' => 'cities#new_post', as: :city_new_post
  post 'hotels/:id' => 'hotels#new_post', as: :hotel_new_post
  post 'restaurants/:id' => 'restaurants#new_post', as: :restaurant_new_post
  post 'turistic_spots/:id' => 'turistic_spots#new_post', as: :turistic_spot_new_post

  post 'ban/:id' => 'admin#ban_user', as: :ban_user
  post 'unban/:id' => 'admin#unban_user', as: :unban_user

  post 'subscribe/:id' => 'followers#subscribe', as: :subscribe

  post 'delete/post/:id/:country_id' => 'posts#delete', as: :delete_post

  post 'admin/select/:id' => 'posts#admin_select', as: :admin_select

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  root 'welcome#index'
  # root to: "home#index"

end
