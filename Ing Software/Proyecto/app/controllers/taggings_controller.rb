class TaggingsController < ApplicationController
  def searching
    @posts = Tagging.search(params[:search])
  end
end
