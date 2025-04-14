from django.urls import path
from . import views


urlpatterns = [
    path('home', views.home ,name='home'),
    path('cart/', views.cart ,name='cart'),
    path('signup/', views.signup, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tickets/', views.tickets ,name='tickets'),
    path('merchandise/', views.merchandise ,name='merchandise'),
    path('album/', views.album ,name='album'),
    path('checkout/', views.checkout ,name='checkout'),
    path('wishlist/', views.wishlist ,name='wishlist'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('merchandise/<int:merchandise_id>/', views.merchandise_detail, name='merchandise_detail'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('cart/delete_item/<int:item_id>/', views.cart_delete_item, name='cart_delete_item'),

    # Admin panel and add views
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/add-news/', views.add_news, name='add_news'),
    path('admin-panel/add-ticket/', views.add_ticket, name='add_ticket'),
    path('admin-panel/add-merchandise/', views.add_merchandise, name='add_merchandise'),
    path('admin-panel/add-album/', views.add_album, name='add_album'),
    path('admin-signup/', views.admin_signup, name='admin_signup'),
    path('admin-login/', views.admin_login, name='admin_login'),

]
