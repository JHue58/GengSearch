## GengSearch

本插件的运行基于<code>mirai-api-http</code>，使用前请先下载[mirai-api-http](https://github.com/project-mirai/mirai-api-http)并完成配置

在<code>data.json</code>文件中填入<code>mirai-api-http</code>的配置信息，请使用<code>http adapter</code>

```json
{
 "Key": "xxxxx", //在mirai-api-http中设置的密钥
 "host": "127.0.0.1:8080", //mirai-api-http中设置的地址（若设置成0.0.0.0，请填写127.0.0.1）
 "port": "8080", //mirai-api-httpmirai-api-http中设置的端口
 "qq": "xxx",  //所登录mirai的QQ号
 "session": "xxx" //任意，由程序自动获取
}
```

请确保插件目录下的<code>wkhtmltopdf</code>组件的完整性



由于<code>小鸡词典</code>在访问次数过多后需要登录，请先至[官网](https://jikipedia.com/)注册并登录后获取cookie字符串填入<code>cookie.txt</code>文件中，没有cookie插件将无法运行



Windows用户点击<code>GengSearch.exe</code>运行

Linux用户可通过执行<code>GengSearch.py</code>脚本运行



<code>seting.json</code>文件说明：

```json
{
"senddaily":  //每日发送
{
"switch":"0",  //1为开启
"hour":"8",   //发送小时(整点)
"sendlist":[],  //发送的群，有多个群用,隔开
"text":"每日一梗，带你了解新知识！" //前置文本
},
"blacklist":  //黑名单
{
"switch":"0", //1为开启
"group":[],   //黑名单群，有多个群用,隔开
"member":[]   //黑名单QQ号，有多个用,隔开
}
}
```

