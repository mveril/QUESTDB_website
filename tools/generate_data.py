#!/usr/bin/env python3

import os
import os.path
import json



def main():

    baseURL = "/"
    with open("config.toml","r") as f:
      for line in f.readlines():
        if line.startswith("baseURL"):
          baseURL = line.split('=')[1].strip()[1:-1]
          break
    if baseURL.startswith("http"):
        baseURL = '/'+baseURL.split('/')[3]+'/'
    print (baseURL)

    d = {}
    os.chdir("static")
    try:
        os.remove(os.path.join("data","database.json"))
    except FileNotFoundError:
        pass
    for root, dirs, files in os.walk('data'):
        for name in files:
            filename = os.path.join(root,name)
            with open(filename,'r',encoding="utf8") as f:
                try:
                    d[baseURL+filename] = f.read()
                except UnicodeDecodeError:
                    pass

    with open(os.path.join("data","database.json"),'w') as f:
        f.write(json.dumps(d,indent=1))


if __name__ == "__main__":
    main()
