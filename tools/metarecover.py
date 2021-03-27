#!/usr/bin/env python3
from git import Repo,Git
import io
r=Repo(path=".")
l=[item for item in r.index.diff("HEAD") if item.a_path.endswith(".dat") and item.change_type=="M"]
for i in l:
  print(i.a_path)
  g=Git(Repo.git_dir)
  with io.StringIO(g.execute(["git" ,"--no-pager", "show", f"HEAD~1:{i.a_path}"])) as old:
    with open(i.a_path,mode="r+") as new:
      with io.StringIO(new.read()) as copy:
        new.seek(0)
        line=old.readline()
        while line and line.startswith("#"):
          new.write(line)
          line=old.readline()
        line=copy.readline()
        end=False
        while line:
          if not end and not line.startswith("#"):
            end=True
          if end:
            new.write(line)
          line=copy.readline()
      new.truncate()