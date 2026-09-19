"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings
import profiles.views
import authentications.views
import companies.views
import marketplaces.views
import products.views

import messages.views
import orders.views
import shippings.views
import imports.views
import imports.test
import offers.views
import warehouses.views
# import stocks.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('admin/', permanent=False)),

    
    #Test
    path('test/imports/', imports.test.TestImport.as_view(),name='test-import'),
    


    path('api/login/', authentications.views.LoginView.as_view(),name='login'),
    path('api/logout/', authentications.views.LogoutView.as_view(),name='logout'),
    
    # Companies api urls
    
    path('api/users/', profiles.views.user_list, name ='users'),
    path('api/users/<int:pk>/', profiles.views.user_detail,name="user"),
    
    # Companies api urls
    path('api/companies/', companies.views.company_list, name ='companies'),
    path('api/companies/<int:pk>/', companies.views.company_detail,name="company"),
    path('api/authorizations/', companies.views.authorizations_list,name="authorizations"),
    path('api/authorizations/<int:pk>/', companies.views.authorization_detail,name="authorization"),
    path('api/me/',profiles.views.user_me_detail,name="me"),
    path('api/me/authorizations/', companies.views.my_authorizations_list,name="my_authorizations"),
    # Marketplaces api urls
    path('api/marketplaces/', marketplaces.views.marketplace_list, name ='marketplaces'),
    path('api/marketplaces/<int:pk>/', marketplaces.views.marketplace_detail, name ='marketplace'),

    # Companies api urls
    path('api/products/simple/', products.views.product_simple_list, name ='products_simple'),
    path('api/products/simple/<int:pk>/', products.views.product_simple_detail,name="product_simple"),
    path('api/products/categories/', products.views.categories_list, name ='categories'),
    path('api/products/categories/<int:pk>/', products.views.category_detail,name="category"),
    path('api/simplify/products/categories/',products.views.categories_simplify_list, name ='categories_simplify'),
    path('api/simplify/products/configurable/combinations/',products.views.SimplifyConfigurableCombinations.as_view(), name ='simplify_combinations'),
    path('api/simplify/products/category/<int:pk>/',products.views.CategoryProductAddDelete.as_view(), name ='categories_add_delete_product'),
    

    path('api/warehouses/', warehouses.views.warehouse_list, name ='warehouses'),
    path('api/warehouses/<int:pk>/', warehouses.views.warehouse_detail,name="warehouse"),
    path('api/warehouse/items/', warehouses.views.items_list, name='items_list'),
    path('api/warehouse/items/<int:pk>/', warehouses.views.items_detail,name="items_detail"),
    path('api/warehouse/items_qty/', warehouses.views.items_qty_list, name ='items_qty_list'),
    path('api/warehouse/items_qty/<int:pk>/', warehouses.views.items_qty_detail,name="items_qty_detail"),
    path('api/warehouse/files/', warehouses.views.item_info_files_list, name ='item_info_files_list'),
    
    
    # path('api/stocks/multiple/', stocks.views.stocks_multiple_list, name ='stocks_multiple'),
    # path('api/stocks/multiple/<int:pk>/', stocks.views.stock_multiple_detail,name="stock_multiple"),
    # path('api/stocks/bulk/', stocks.views.stocks_bulk_list, name ='stocks_bulk'),
    # path('api/stocks/bulk/<int:pk>/', stocks.views.stock_bulk_detail,name="stock_bulk"),
    
    path('api/abstract/configurable/', products.views.abstract_product_configurable_list, name ='abstract_product_configurable_list'),
    path('api/abstract/simple/', products.views.abstract_product_simple_list, name ='abstract_product_simple_list'),
    path('api/abstract/multiple/', products.views.abstract_product_multiple_list, name ='abstract_product_multiple_list'),
    path('api/abstract/bulk/', products.views.abstract_product_bulk_list, name ='abstract_product_bulk_list'),
    path('api/abstract/category/simple/', products.views.abstract_product_for_category_simple_list, name ='abstract_product_for_category_simple_list'),
    path('api/abstract/category/configurable/', products.views.abstract_product_for_category_configurable_list, name ='abstract_product_for_category_configurable_list'),
    path('api/abstract/category/multiple/', products.views.abstract_product_for_category_multiple_list, name ='abstract_product_for_category_multiple_list'),
    path('api/abstract/category/bulk/', products.views.abstract_product_for_category_bulk_list, name ='abstract_product_for_category_bulk_list'),


    path('api/auth/', companies.views.auth_create,name="auth"),

    path('api/products/configurable/', products.views.product_configurable_list, name ='products_configurable'),
    path('api/products/configurable/<int:pk>/', products.views.product_configurable_detail,name="product_configurable"),

    path('api/products/bulk/', products.views.product_bulk_list, name ='products_bulk'),
    path('api/products/bulk/<int:pk>/', products.views.product_bulk_detail,name="product_bulk"),

    path('api/products/multiple/', products.views.product_multiple_list, name ='products_multiple'),
    path('api/products/multiple/<int:pk>/', products.views.product_multiple_detail,name="product_multiple"),

    # path('api/products/bulk_bulk/', products.views.product_bulk_of_bulk_list, name ='products_bulk_of_bulk'),
    # path('api/products/bulk_bulk/<int:pk>/', products.views.product_bulk_of_bulk_detail,name="product_bulk_of_bulk"),

    # path('api/products/bulk_multiple/', products.views.product_bulk_of_multiple_list, name ='products_bulk_of_multiple'),
    # path('api/products/bulk_multiple/<int:pk>/', products.views.product_bulk_of_multiple_detail,name="product_bulk_of_multiple"),


    # path('api/products/multiple_multiple/', products.views.product_multiple_of_multiple_list, name ='products_multiple_of_multiple'),
    # path('api/products/multiple_multiple/<int:pk>/', products.views.product_multiple_of_multiple_detail,name="product_multiple_of_multiple"),

    # path('api/products/multiple_bulk/', products.views.product_multiple_of_bulk_list, name ='products_multiple_of_bulk'),
    # path('api/products/multiple_bulk/<int:pk>/', products.views.product_multiple_of_bulk_detail,name="product_multiple_of_bulk"),

    # path('api/products/configurable_bulk/', products.views.product_configurable_of_bulk_list, name ='products_configurable_of_bulk'),
    # path('api/products/configurable_bulk/<int:pk>/', products.views.product_configurable_of_bulk_detail,name="product_configurable_of_bulk"),

    # path('api/products/configurable_bulk/', products.views.product_configurable_of_bulk_list, name ='products_configurable_of_bulk'),
    # path('api/products/configurable_bulk/<int:pk>/', products.views.product_configurable_of_bulk_detail,name="product_configurable_of_bulk"),
    # path('api/products/categories/', products.views.categories_list, name ='categories'),
    # path('api/products/categories/<int:pk>/', products.views.category_detail,name="category"),
    path('api/products/attributes/', products.views.attributes_list, name ='attributes'),
    path('api/products/attributes/<int:pk>/', products.views.attribute_detail,name="attribute"),
    path('api/products/custom_attributes/', products.views.custom_attributes_list, name ='custom_attributes'),
    path('api/products/custom_attributes/<int:pk>/', products.views.custom_attribute_detail,name="custom_attribute"),

    
    
    path('api/copy/to/simple/',products.views.CopyToSimple.as_view(),name="copy_to_simple"),
    path('api/copy/from/simple/',products.views.CopyFromSimple.as_view(),name="copy_from_simple"),

    path('api/offers/simple/', offers.views.product_simple_offers_list, name ='product_simple_offers'),
    path('api/offers/simple/<int:pk>/', offers.views.product_simple_offer_detail,name="product_simple_offer"),
    path('api/offers/multiple/', offers.views.product_multiple_offers_list, name ='product_multiple_offers'),
    path('api/offers/multiple/<int:pk>/', offers.views.product_multiple_offer_detail,name="product_multiple_offer"),
    path('api/offers/bulk/', offers.views.product_bulk_offers_list, name ='product_bulk_offers'),
    path('api/offers/bulk/<int:pk>/', offers.views.product_bulk_offer_detail,name="product_bulk_offer"),

    path('api/simplify/offers/',offers.views.OffersView.as_view(), name ='get_simplify_offers'),

    path('api/ivas/', offers.views.iva_list, name ='iva_list'),
    path('api/ivas/<int:pk>/', offers.views.iva_detail,name="iva_detail"),

    path('api/messages/', messages.views.message_list, name ='messages'),
    path('api/messages/<int:pk>/', messages.views.message_detail,name="message"),

    path('api/orders/', orders.views.order_list, name ='orders'),
    path('api/orders/<int:pk>/', orders.views.order_detail,name="order"),
    path('api/orders_detail/', orders.views.order_detail_list, name ='orders_detail'),
    path('api/orders_detail/<int:pk>/', orders.views.order_detail_detail,name="order_detail"),

    path('api/shippings/', shippings.views.shipping_list, name ='shippings'),
    path('api/shippings/<int:pk>/', shippings.views.shipping_detail,name="shipping"),

    path('api/couriers/', shippings.views.courier_list, name ='couriers'),
    path('api/couriers/<int:pk>/', shippings.views.courier_detail,name="courier"),

    path('api/imports/', imports.views.import_list, name ='imports'),
    path('api/imports/<int:pk>/', imports.views.import_detail,name="import"),

    
    path('api/files/imports/<int:pk>/',imports.views.import_file,name="import_file"),
    
    # path('api/abstract/variations/',products.views.AbstractVariationsView.as_view(),name="abstract_variations"),
    # path('api/abstract/products/',products.views.AbstractProductsListView.as_view(),name="abstract_products_list"),
    
    # path('api/products/save/',products.views.ProductSave.as_view(),name="product_save"),
    # path('api/products/delete/',products.views.ProductDelete.as_view(),name="product_delete"),

    
    # path('api/products/eav/url/<str:sku>/', products.views.product_url_eav_list, name ='products_url_eav'),
    # path('api/products/eav/url/<str:sku>/<str:attribute>/', products.views.product_url_eav_detail,name="product_url_eav"),

    # path('api/products/eav/char/<str:sku>/', products.views.product_char_eav_list, name ='products_char_eav'),
    # path('api/products/eav/char/<str:sku>/<str:attribute>/', products.views.product_char_eav_detail,name="product_char_eav"),

    # path('api/products/eav/int/<str:sku>/', products.views.product_int_eav_list, name ='products_int_eav'),
    # path('api/products/eav/int/<str:sku>/<str:attribute>/', products.views.product_int_eav_detail,name="product_int_eav"),

    # path('api/products/eav/decimal/<str:sku>/', products.views.product_decimal_eav_list, name ='products_decimal_eav'),
    # path('api/products/eav/decimal/<str:sku>/<str:attribute>/', products.views.product_decimal_eav_detail,name="product_decimal_eav"),

    # path('api/products/eav/boolean/<str:sku>/', products.views.product_boolean_eav_list, name ='products_boolean_eav'),
    # path('api/products/eav/boolean/<str:sku>/<str:attribute>/', products.views.product_boolean_eav_detail,name="product_boolean_eav"),

    # path('api/products/eav/text/<str:sku>/', products.views.product_text_eav_list, name ='products_text_eav'),
    # path('api/products/eav/text/<str:sku>/<str:attribute>/', products.views.product_text_eav_detail,name="product_text_eav"),
    
    #path('api/token/refresh/',token_views.refresh_auth_token),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

