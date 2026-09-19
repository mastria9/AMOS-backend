categories=[{"id": 1,"title": "Scarpe","parent": {"id": 4}},
            {"id": 4,"title": "Abbigliamento","parent": {"id": 3}},
            {"id": 2,"title": "Pantaloni","parent": {"id":4}},
            {"id": 3,"title": "Armadio","parent": None}
        ]
        

#voglio che siano:
tree=[]
# tree=[{"id":3,
#         "childs":[{"id":4,"childs":[
#                         {"id":2,"childs":None},
#                         {"id":1,"childs":None}
#                     ]
#             }
#         ]
# }
# ]
import time
def find_parent(tree,id):
    i=0
    while i<len(tree):
        if tree[i]["id"]==id:
            return tree[i]
        else:
            if tree[i]["childs"] is not None:
                obj=find_parent(tree[i]["childs"],id)
                if obj!=None:
                    return obj
        i+=1
    return None

            
i=0
while len(categories)>0:
    print("i="+str(i)+",lenCategories="+str(len(categories)))
    print(tree)
    if categories[i]["parent"] is None:
        print("Parent è None")
        tree.append({"id":categories[i]["id"],"childs":[]})
        categories.pop(i)
        i=0
    else:
        parent=find_parent(tree,categories[i]["parent"]["id"])
        print("find",categories[i]["parent"]["id"])
        if parent is not None:
            print("Parent trovato")
            parent["childs"].append({"id":categories[i]["id"],"childs":[]})
            categories.pop(i)
            i=0
        else:
            print("Parent non trovato")
            i+=1
print(tree)

        
# se non lo trovo sarà in coda  