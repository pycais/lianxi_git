# 猜

git clone

git add 

git commit

git push

git pull

git init



git diff 查看文件与修改之前的区别

git log git的日志

git remote 远端

git reset 

git branch 分支

git merge 合并

git fetch





~~~~
2190  git init
 2191  ls -al
 2192  git remote add origin git@github.com:whoareyou0401/hz1807.git
 2193  git remote -v
 2194  git remote remove origin
 2195  git remote -v
 2196  git remote add origin git@github.com:whoareyou0401/hz1807.git
 2197  ls
 2198  git pull origin master
 2199  ls
 2200  git status
 2201  git add .
 2202  git status
 2203  git commit -m "第八天代码"
 2204  git push origin master
 2205  git log
 2206  git status
 2207  git diff t08/views.py
 2208  git diff 
 2209  git add .
 2210  git commit -m "diff的修改演示"
 2211  git status
 2212  git branch dev
 2213  git status
 2214  git branch
 2215  ls
 2216  git checkout dev
 2217  ls
 2218  git branch
 2219  vim a.txt
 2220  ls
 2221  git add a.txt 
 2222  git commit -m "添加一个a.txt"
 2223  git branch master
 2224  ls
 2225  git checkout master
 2226  ls
 2227  git merge dev
 2228  ls
 2229  git branch
 2230  git push origin master 
 2231  git log
 2232  git reset 9b62c253a69ee49996e0c95fab
 2233  ls
 2234  git status
 2235  git log
 2236  git reset --hard 9b62c253a69ee49996e0c95fab
 2237  ls
 2238  git log
 2239  git status
 2240  rm a.txt 
 2241  git status
 2242  git merge dev
 2243  ls
 2244  git reset --hard 9b62c253a69ee49996e0c95fab
 2245  ls
 2246  vim t08/views.py 
 2247  git add t08/views.py 
 2248  git commit -m "呵呵呵"
 2249  git pull origin master 
 2250  vim t08/views.py 
 2251  git add t08/views.py 
 2252  git commit -m "fix conflict"
 2253  git push origin master 
 2254  history

~~~~



