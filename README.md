# YoungCha

### HOW TO
Follow the example lines for the first try

### clone repository
```
git clone https://github.com/choij1589/YoungCha.git
```
### make your own test branch
```
git branch $YOUR_OWN_BRANCH
git checkout $YOUR_OWN_BRANCH
# or shortly
git checkout -b $YOUR_OWN_BRANCH
# example
git checkout -b TestBranch
git checkout main
```
### pull: get files from github
```
git pull $REMOTE $BRANCH
# example
git pull origin main
```
### add & commmit & push
```
git status
git add $FILE_NAME
# add all
git add .
git commit -m "message"
git push $REMOTE $BRANCH

# example
git status -s
git add .
git commit "regular backup"
git push origin main
```
