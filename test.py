mydict = {
    "user":1,
    "content": "hello"
}

new_dict = {"user":2, "content":"new content","chaos":3}


for key in new_obj.keys():
    if key in old_obj:
        old_obj[key] = new_obj[key]


print(mydict)
