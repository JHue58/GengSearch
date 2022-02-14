## GengSearch

本插件的运行基于<code>mirai-api-http</code>，使用前请先下载[mirai-api-http](https://github.com/project-mirai/mirai-api-http)并完成配置

在<code>data.json</code>文件中填入<code>mirai-api-http</code>的配置信息，请使用<code>http adapter</code>，并确保<code>singleMode</code>为<code>false</code>

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



由于<code>小鸡词典</code>在访问次数过多后需要登录，请先至[官网](https://jikipedia.com/)注册并登录后获取cookie字符串填入<code>cookie.txt</code>文件中



Windows用户点击<code>GengSearch.exe</code>运行

Linux用户可通过执行<code>GengSearch.py</code>脚本运行



<code>seting.json</code>文件说明：

```c++
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
},
"tritext":  //触发文本
{
"searchtext":["梗查询 "],  //查询的触发文本，有多个用,隔开(文本必须带上双引号！！)
"randomtext":["来点梗"]  //随机梗的触发文本，有多个用,隔开(文本必须带上双引号！！)
    					//例：["梗查询 ","查梗 "]
},
"rescontrol":   //冷却时间设置（单位秒，0秒则不开启）
{
"group":"10",   //群冷却时间
"member":"30",  //群成员冷却时间
"grouptext":"让我休息一下嘛！",  //群冷却时间时的反馈文本
"membertext":"你搜的太快啦！{}秒后再来试试吧"  //群成员冷却时间时的反馈文本（程序会将{}符号替换为剩余的冷却时间，不出现{}则不显示剩余时间）
}
}
```



### Linux用户注意事项

- 通过<code>pip install lxml</code>指令安装<code>lxml</code>库（已安装的可以跳过此步）
- 在[wkhtmltopdf官网](https://wkhtmltopdf.org/downloads.html)下载对应系统的<code>rpm</code>文件，并安装
- 将安装好后在**user/local/bin**找到**wkhtmltoimage**文件，并将他移动至目录下
- 使用<code>chmod 777</code>指令给予**wkhtmltoimage**文件权限
- 在运行时可能会出现缺少**wkhtmltoimage**所需**运行库**的问题(libxxxx not found)，可以通过<code>yum</code>指令安装缺少的**运行库**

- 若出现**文字乱码或方块**的现象，请下载[字体库](https://www.yii666.com/Uploads/wkhtmltopdf_fonts.zip)并解压至**/usr/share/fonts**目录下
