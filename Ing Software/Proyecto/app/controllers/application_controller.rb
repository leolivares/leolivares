class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  layout 'application'
  def hello
    render html: 'Hello World!'
  end

  def liked_arrow
    if @liked_exists
      'color:red'
    else
      'color:'
    end
  end

  def authenticate_any!
    if admin_signed_in?
      true
    else
      authenticate_user!
    end
  end

  helper_method :liked_arrow
end
