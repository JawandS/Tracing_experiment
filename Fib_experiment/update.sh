find . -size +99M | cat >> ../.gitignore
git commit -m "update .gitignore"
git add .
git commit -m "$1"
git push
