### nginx
```
server {
    listen  80;
    server_name 2217admin.zonst.org;
    root    /Users/zhangyuwei/2217/admin/admin/dist;
    location / {
        try_files $uri $uri @router;    # 需要指向下面的@router否则会出现vue的路由在nginx中刷新出现404
        index   index.html;
    }
    location @router{
        rewrite ^.*$ /index.html last;
    }
}

server {
    listen  80;
    server_name 2217adminapi.zonst.org;
    root    /Users/zhangyuwei/2217/admin;
    location / {
        proxy_pass  http://0.0.0.0:5002;
    }
}
```
### hosts:
```
0.0.0.0 2217adminapi.zonst.org 2217admin.zonst.org
```