# file_watcher
Run bash commands when files change


## Alternative

I just found about `entr`, so we could probably just completely replace thies project with that. ie)

```
find . -path ./.venv -prune -o -type f -name '*.py' | entr -s "make test"
```
