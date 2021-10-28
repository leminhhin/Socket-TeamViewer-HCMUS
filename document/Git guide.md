# Git

---

## Cơ bản

git status: check trạng thái các file (coi có sửa đổi, tạo, xóa gì mới)

git add <file name>: track thay đổi (kiểm tra file có thay đổi không)

- git add test.py
- git add .

git commit -m "some message": commit 1 lần sửa đổi (giống kiểu save game)

git checkout <commit hash>: quay lại commit đó (load game)

git pull: download từ remote (github) về local (máy)

git push: upload từ local lên remote 

---

## Branch (nhánh)

git checkout -b <branch name>: tạo và di chuyển đến 1 branch mới

git checkout <branch name>: đi đến 1 branch nào đó

git merge <branch name>: hợp nhất branch mục tiêu với branch hiện tại (chỉ merge vào main khi branch ổn định)

---

## Quy trình:

main 

- git checkout <branch> để tới/tạo branch để làm chức năng mới
- git pull để cập nhật dữ liệu mới nhất từ trên remote về máy (áp dụng khi trên main có thay đổi mới thì nên pull về máy để đỡ bị đụng độ dữ liệu)
- sau khi tạo/sửa file -> git add -> git commit -> git push lên branch của mình
- test kĩ chức năng -> họp nhóm -> git merge vào main