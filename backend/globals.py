# CharFields Lengths
VID_LENGTH=10
MARKETPLACE_CHOICES=[("NVX","Nevix"),("AMZ","Amazon"),("EBY","Ebay"),("RKT","Rakuten"),("MNM","ManoMano")]
COUNTRY_CHOICES=[("IT","Italy"),("UK","United Kingdom"),("FR","France"),("DE","Germany"),("ES","Spain")]
LANGUAGES_CHOICES=[("IT","Italian"),("EN","English"),("DE","German"),("FR","French"),("ES","Spanish")]


SKU_LENGTH=25
PRODUCT_TYPE_CHOICES=[("S","Semplice"),("C","Configurabile"),("B","Misto"),("D","Digitale"),("M","Multiplo")]
GTIN_CHOICES=[("EAN","European Article Number"),("ISBN","Identifier Standard Book Nation"),("NOGTIN",'GTIN Exemption')]
GTIN_LENGTH=10
ORDER_STATUS_CHOICES=[("N","Nuovo"),("PP","In attesa di pagamento"),("F","Fallito"),("P","In Elaborazione"),("C","Completato"),("S","Spedito"),("OH","Bloccato"),("D","Cancellato"),("R","Rimborsato"),("PR","Parzialmente rimborsato")]

# SHIPPING_CHOICES=[("BRT","Bartolini"),("SDA","SDA Express Courier"),("GLS","Global Logistic Service")]

# NAME_LENGTH=20
# TITLE_LENGTH=80
# DESCRIPTION_LENGTH=5000
# SHORT_DESCRIPTION_LENGTH=20
# NID_LENGTH=15
# ORDER_LENGTH=50
# ADDRESS_NUMBER_LENGTH=5
# #PERSONS
# FIRST_NAME_LENGTH=30
# SECOND_NAME_LENGTH=30
# LAST_NAME_LENGTH=30
# ADDRESS_LENGTH=80
# PIVA_LENGTH=15
# SDI_LENGTH=11
# TOWN_LENGTH=20
# PROVINCE_LENGTH=20
# REGION_LENGTH=20
# USER_TYPE_LENGTH=2
# PHONE_LENGTH=15
# MARKETPLACE_CHOICES_LENGTH=3
# SHIPPING_CHOICES_LENGTH=5
# COUNTRY_CHOICES_LENGTH=2
# PRODUCT_TYPE_LENGTH=1
# CURRENCY_LENGTH=3


# # Choices





# CURRENCY_CHOICES=[("EUR","Euro")]

# PRODUCT_FIELDS={"sku":"SKU","gtin":"GTIN","gtin_type":"Tipo GTIN","asin":"ASIN","draftType":"Tipo prodotto","title":"Titolo","html":"Descrizione HTML","ean":"EAN",
# "short_description":"Descrizione breve","brand":"Marca","keywords":"Parole chiave","manufacturer":"Produttore","browse_node":"Nodo di navigazione",
# "bullet_point_1":"Bullet Point1","bullet_point_2":"Bullet Point2","bullet_point_3":"Bullet Point3","bullet_point_4":"Bullet Point4","bullet_point_5":"Bullet Point5","bullet_point_6":"Bullet Point6","bullet_point_7":"Bullet Point7","bullet_point_8":"Bullet Point8",
# "images0":"Immagine principale","images1":"Altra Immagine (1)","images2":"Altra Immagine (2)","images3":"Altra Immagine (3)","images4":"Altra Immagine (4)","images5":"Altra Immagine (5)","images6":"Altra Immagine (6)","images7":"Altra Immagine (7)","images8":"Altra Immagine (8)","images9":"Miniatura"}
# OFFERS_FIELDS={"sku":"SKU","title":"Titolo","price":"Prezzo","qty":"Quantità","status":"Stato"}
# FIELDS_EAV_UNIQUE=[("brand","Marca"),("manufacturer","Produttore"),("manufacturer","Produttore"),("country_of_origin","Nazione produttrice")]
# FIELDS_EAV=[("asin","ASIN"),("title","Titolo"),("description","Descrizione"),("html","Descrizione HTML"),("short_description","Descrizione breve"),
# ("keywords","Parole chiave"),("bullet_point_1","Bullet Point1"),("bullet_point_2","Bullet Point2"),("bullet_point_3","Bullet Point3"),("bullet_point_4","Bullet Point4"),("bullet_point_5","Bullet Point5"),("bullet_point_6","Bullet Point6"),("bullet_point_7","Bullet Point7"),("bullet_point_8","Bullet Point8"),
# ("images0","Immagine principale"),("images1","Altra Immagine (1)"),("images2","Altra Immagine (2)"),("images3","Altra Immagine (3)"),("images4","Altra Immagine (4)"),("images5","Altra Immagine (5)"),("images6","Altra Immagine (6)"),("images7","Altra Immagine (7)"),("images8","Altra Immagine (8)"),("images9","Miniatura"),
# ("price","Prezzo")]
# # ATTRIBUTE_DIMENSION_FIELDS=[("radius_mm","Raggio (mm)"),("radius_cm","Raggio (cm)"),("radius_m","Raggio (m)"),
# # ("diameter_mm","Diametro (mm)"),("diameter_cm","Diametro (cm)"),("diameter_m","Diametro (m)"),
# # ("height_mm","Altezza (mm)"),("height_cm","Altezza (cm)"),("height_m","Altezza (m)"),
# # ("width_mm","Larghezza (mm)"),("width_cm","Larghezza (cm)"),("width_m","Larghezza (m)"),
# # ("length_mm","Lunghezza (mm)"),("length_cm","Lunghezza (cm)"),("length_m","Lunghezza (m)"),
# # ("weight_g","Peso (g)"),("weight_kg","Peso (kg)")]
# # ATTRIBUTES_FIELDS=[("color","Colore"),("material","Materiale"),("finishing","Finitura")]+ATTRIBUTE_DIMENSION_FIELDS

# ATTRIBUTES_TYPE_CHOICES=[("OPT","Optional"),("MAN","Main"),("DIM","Dimension"),("LOG","Logistic"),("PRX","Price")]
# ATTRIBUTES_TYPE_CHOICES_LENGTH=3